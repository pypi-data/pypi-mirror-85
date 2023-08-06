""" File to define validations for tag model fields.
"""
import datetime
import logging
import re

import crum
import opaque_keys.edx.keys as all_opaque_keys
import six
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from eox_core.edxapp_wrapper.enrollments import get_enrollment
from eox_core.edxapp_wrapper.users import get_edxapp_user
from opaque_keys import InvalidKeyError  # pylint: disable=ungrouped-imports, useless-suppression

log = logging.getLogger(__name__)

try:
    from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
except ImportError:
    CourseOverview = object  # pylint: disable=ungrouped-imports, useless-suppression
try:
    # Python 2: "unicode" is built-in
    unicode  # pylint: disable=undefined-variable, useless-suppression
except NameError:
    unicode = str  # pylint: disable=redefined-builtin, useless-suppression

DATETIME_FORMAT_VALIDATION = "%Y-%m-%d %H:%M:%S"


class TagValidators(object):
    """ Defines all validator methods.
    """

    def __init__(self, instance):
        """
        Attributes:
            instance: instance of the model to validate before saving
            definitions: configuration matching fields to validate
        """
        self.instance = instance
        self.model_validations = {
            'User': self.__validate_user_integrity,
            'OpaqueKeyProxyModel': self.__validate_proxy_model,
            'CourseEnrollment': self.__validate_enrollment_integrity,
            'Site': self.__validate_site_integrity,
        }
        self.__configuration_types = {
            "in": list,
            "equals": six.string_types,
            "regex": six.string_types,
            "exist": bool,
            "opaque_key": six.string_types,
        }
        self.current_tag_definitions = {}
        self.set_configuration()

    def set_configuration(self):
        """Function that sets and validates configuration for model instance."""
        self.validate_no_updating()  # Don't validate if trying to update
        self.__select_configuration()
        self.__force_configuration_values()
        self.__validate_configuration_types()
        self.__validate_configuration()

    def __select_configuration(self):
        """Function that selects the correct configuration for model instance."""
        for tag_def in settings.EOX_TAGGING_DEFINITIONS:
            tag_type = tag_def.get('tag_type')
            if tag_type == self.instance.tag_type:
                self.current_tag_definitions = tag_def
                return
        raise ValidationError("Tag_type '{}' not configured".format(self.instance.tag_type))

    def __force_configuration_values(self):
        """
        Function that sets tag values defined in the configuration.

        For example:
        {
            "force_access": "public"
        }
        Then the access level of the tag must be set tu public, no matter if it had a value before.
        Also, using force the validations are skipped.
        """
        pattern = "force_"
        configurations_copy = dict(self.current_tag_definitions)

        for key, value in configurations_copy.items():
            if key.startswith(pattern):
                try:
                    self.instance.set_attribute(key.replace(pattern, ""), value)
                except Exception:
                    raise ValidationError(u"EOX_TAGGING | The field {} with value `{}` is wrongly configured."
                                          .format(key, value))
                del self.current_tag_definitions[key]

    def __validate_required(self):
        """Function that validates the configuration for the required fields target and owner."""
        required_target_fields = r".*target_object|.*resource_locator"
        required_owner_fields = r".*owner_object"

        if not self.__find_attribute(required_target_fields):
            raise ValidationError("The target object for `tag_type`: '{}' is not configured."
                                  .format(self.instance.tag_type))

        if not self.__find_attribute(required_owner_fields):
            self.current_tag_definitions["validate_owner_object"] = "site"

    def __find_attribute(self, attr_pattern):
        """Function that fiends an attribute in the current tag definitions."""
        for attr in self.current_tag_definitions:
            if re.match(attr_pattern, attr):
                return True
        return False

    # Config validations
    def __validate_configuration(self):
        """
        Function that validates EOX_TAGGING_DEFINITIONS. The validations consist in:
            - Validate available validations
            - Validate field names
            - Check required fields in configuration
        If any error occur a ValidationError will be raised.
        """
        self.__validate_required()  # Validate that the require configs exists
        regex = r"validate_"

        for key, value in self.current_tag_definitions.items():

            # Validate value correctness if it has validations defined
            if re.match(regex, key) and not isinstance(value, six.string_types):
                for _key in value:  # Validations must exist as a class method
                    try:
                        getattr(self, "validate_{}".format(_key))
                    except AttributeError:
                        raise ValidationError(u"EOX_TAGGING | The field {} with value `{}` is wrongly configured."
                                              .format(key, _key))
            # Validate key existence
            clean_key = re.sub(regex, "", key)
            try:
                self.instance.get_attribute(clean_key)
            except AttributeError:
                raise ValidationError(u"EOX_TAGGING | The field `{}` is wrongly configured."
                                      .format(key))

    def __validate_configuration_types(self):
        """Function that validate the correct type for pairs <key, value> in configuration."""

        regex = r"validate_"

        for key, value in self.current_tag_definitions.items():

            if re.match(regex, key) and isinstance(value, dict):

                for key_ in value:

                    value_type = self.__configuration_types.get(key_)
                    field_value = value.get(key_)

                    if value_type and not isinstance(field_value, value_type):
                        raise ValidationError(u"EOX_TAGGING | The validation '{}' for '{}' is wrongly configured."
                                              .format(key_, key))

            elif not isinstance(value, six.string_types):
                raise ValidationError(u"EOX_TAGGING | The field '{}' is wrongly configured.".format(key))

    # GFK validations

    def validate_fields_integrity(self):
        """Helper function that calls for every object that needs integrity validation."""
        fields_to_validate = ["owner_object", "target_object"]
        map(self.__validate_model, fields_to_validate)

    def __validate_model(self, field_name):
        """Function that validates the instances in GFK fields calling the integrity validators."""
        try:
            model_name = self.instance.get_attribute(field_name, name=True)
        except AttributeError:
            raise ValidationError("EOX_TAGGING | The field '{}' is wrongly configured."
                                  .format(field_name))
        try:
            if model_name:
                self.model_validations[model_name](field_name)
        except KeyError:
            raise ValidationError("EOX_TAGGING | Could not find integrity validation for field '{}'"
                                  .format(field_name))

    # Integrity validators
    def __validate_proxy_model(self, object_name):
        """
        Function that validates existence of proxy model.

        Arguments:
            - object_name: name of the object to validate. It can be: target_object or owner_object
        """
        opaque_key = self.instance.get_attribute(object_name).opaque_key
        try:
            CourseOverview.get_from_id(opaque_key)
        except Exception:
            raise ValidationError("EOX_TAGGING | Could not find opaque key: '{key}' for relation '{name}'".format(
                key=opaque_key,
                name=object_name,
            ))

    def __validate_user_integrity(self, object_name):
        """
        Function that validates existence of user.

        Arguments:
            - object_name: name of the object to validate. It can be: target_object or owner_object
        """
        request = crum.get_current_request()
        data = {
            "username": self.instance.get_attribute(object_name).username,  # User needs to have username
            "site": request.site
        }
        try:
            get_edxapp_user(**data)

        except Exception:
            raise ValidationError("EOX_TAGGING | Could not find ID: {id} for relation '{name}'".format(
                id=self.instance.get_attribute(object_name).id,
                name=object_name,
            ))

    def __validate_enrollment_integrity(self, object_name):
        """
        Function that validates existence of the enrollment.

        Arguments:
            - object_name: name of the object to validate. It can be: target_object or owner_object
        """
        object_ = self.instance.get_attribute(object_name)
        data = {
            "username": object_.username,
            "course_id": unicode(object_.course_id),
        }
        try:
            enrollment, _ = get_enrollment(**data)
            if not enrollment:
                raise ValidationError("EOX_TAGGING | Enrollment for user '{}' and courseID '{}' does not exist"
                                      .format(data["username"], data["course_id"]))
        except Exception:
            raise ValidationError("EOX_TAGGING | Error getting enrollment for user '{}' and courseID '{}'"
                                  .format(data["username"], data["course_id"]))

    def __validate_site_integrity(self, object_name):
        """
        Function that validates existence of the site.

        Arguments:
            - object_name: name of the object to validate. It can be: target_object or owner_object
        """
        site_id = self.instance.get_attribute(object_name).id

        try:
            Site.objects.get(id=site_id)
        except ObjectDoesNotExist:
            raise ValidationError("EOX_TAGGING | Site '{}' does not exist".format(site_id))

    # Other validations
    def validate_no_updating(self):
        """Function that validates that the save is not an update."""
        if self.instance.id:
            #  Exception raised when trying to update
            raise ValidationError("EOX_TAGGING | Can't update tag. Tags are immutable by definition")

    def validate_fields(self):
        """ Function that validates all fields for the current definition."""

        regex = r"^validate_"

        for key, value in self.current_tag_definitions.items():

            clean_key = re.sub(regex, "", key)
            if isinstance(value, six.string_types):
                validator_method = getattr(self, "validate_equals")
                validator_method(clean_key, value)
            else:
                for _key, _value in value.items():
                    validator_method = getattr(self, "validate_{}".format(_key))
                    validator_method(clean_key, _value)

    def validate_opaque_key(self, field, value):
        """
        Function that if called validates that that field is value OpaqueKey defined in
        opaque_keys.edx.keys.

        Arguments:
            - field: field to validate
            - value: validations defined for the field
        """
        field_value = self.instance.get_attribute(field)
        try:
            opaque_key_to_validate = getattr(all_opaque_keys, value)
            # Validation method for OpaqueKey: opaque_key_to_validate
            getattr(opaque_key_to_validate, "from_string")(field_value)
        except InvalidKeyError:
            # We don't recognize this key
            raise ValidationError("The key '{}' for '{}' is not an opaque key".format(field_value, field))

    def validate_in(self, field, values):
        """
        Function that validates that the field exists in values.

        Arguments:
            - field: field to validate
            - value: validations defined for the field
        """
        field_value = self.instance.get_attribute(field, name=True)

        if isinstance(field_value, datetime.datetime):
            field_value = str(field_value)

        formatted_values = [item.lower() for item in values]
        formatted_field_value = field_value.lower()

        if formatted_field_value not in formatted_values:
            # Values allowed is list of values (at least one)

            raise ValidationError("EOX_TAGGING | The field '{}' is not in tag definitions.".format(field))

    def validate_exist(self, field, value):  # pylint: disable=unused-argument
        """
        Function that validates that the field exists, this means, is not None.

        Arguments:
            - field: field to validate
            - value: validations defined for the field
        """
        field_value = self.instance.get_attribute(field)

        if not field_value:
            raise ValidationError("EOX_TAGGING | The field '{}' is required.".format(field))

    def validate_equals(self, field, value):
        """
        Function that validates that the field_value is equal to value.

        Arguments:
            - field: field to validate
            - value: validations defined for the field
        """
        field_value = self.instance.get_attribute(field, name=True)

        if isinstance(field_value, datetime.datetime):
            self.__compare_equal_dates(field_value, value)
            return

        if not field_value:
            raise ValidationError("EOX_TAGGING | The field '{}' is required and must be equal to '{}'."
                                  .format(field, value))
        elif field_value.lower() != value.lower():
            raise ValidationError("EOX_TAGGING | The field '{}' must be equal to '{}'.".format(field, value))

    def validate_between(self, field, value):
        """
        Function that checks that a date must be in between two dates.

        Arguments:
            - field: field to validate
            - value: validations defined for the field
        """
        field_value = self.instance.get_attribute(field)
        datetime_obj = []

        for datetime_str in value:
            try:
                datetime_obj.append(datetime.datetime.strptime(datetime_str, DATETIME_FORMAT_VALIDATION))
            except TypeError:
                raise ValidationError("EOX_TAGGING | The DateTime field '{}' must follow the format '{}'."
                                      .format(datetime_str, DATETIME_FORMAT_VALIDATION))

        if field_value < datetime_obj[0] or field_value > datetime_obj[-1]:
            raise ValidationError("EOX_TAGGING | The DateTime field '{}' must be in between '{}' and '{}."
                                  .format(field_value, str(datetime_obj[0]), str(datetime_obj[-1])))

    def __compare_equal_dates(self, field_value, value):
        """
        Function that checks that a date must be equal to another date.

        Arguments:
            - field_value: datetime to validate.
            - value: datetime strings to validate against.
        """
        try:
            datetime_str = datetime.datetime.strptime(value, DATETIME_FORMAT_VALIDATION)
        except TypeError:
            raise ValidationError("EOX_TAGGING | The DateTime field '{}' must follow the format '{}'."
                                  .format(value, DATETIME_FORMAT_VALIDATION))

        if field_value != datetime_str:
            raise ValidationError("EOX_TAGGING | The DateTime field '{}' must be equal to '{}'."
                                  .format(field_value, str(value)))

    def validate_regex(self, field, value):
        """
        Function that validates that the field matches value.
        Arguments:
            - field: field to validate
            - value: validations defined for the field
        """
        field_value = self.instance.get_attribute(field, name=True)

        if not re.search(value, field_value):
            # Values allowed is regex pattern
            raise ValidationError("EOX_TAGGING | The field '{}' is not in tag definitions.".format(field))
