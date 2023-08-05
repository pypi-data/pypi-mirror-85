"""
Model to store tags in the database.
"""
import logging
import re
import uuid
from datetime import datetime

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from opaque_keys.edx.django.models import CourseKeyField
from opaque_keys.edx.keys import CourseKey

from eox_tagging.constants import AccessLevel, Status
from eox_tagging.validators import TagValidators

log = logging.getLogger(__name__)

OPAQUE_KEY_PROXY_MODEL_TARGETS = [
    "CourseOverview",
]

PROXY_MODEL_NAME = "opaquekeyproxymodel"

COURSE_ENROLLMENT_MODEL_NAME = "courseenrollment"


class TagQuerySet(QuerySet):
    """ Tag queryset used as manager."""

    def create_tag(self, **kwargs):
        """Method used to create tags."""
        target = kwargs.pop("target_object", None)
        if target and target.__class__.__name__ in OPAQUE_KEY_PROXY_MODEL_TARGETS:
            kwargs['target_object'], _ = OpaqueKeyProxyModel.objects.get_or_create(opaque_key=target.id)
        else:
            kwargs["target_object"] = target
        instance = self.create(**kwargs)
        return instance

    def active(self):
        """Returns all active tags."""
        return self.filter(inactivated_at=None)

    def inactive(self):
        """Returns all inactive tags."""
        return self.exclude(inactivated_at=None)

    def delete(self):
        """Used to delete a set of tags."""
        return super(TagQuerySet, self).update(inactivated_at=timezone.now(),
                                               status=Status.INACTIVE)

    def find_by_owner(self, owner_type, owner_id):
        """Returns all tags owned by owner_id."""

        try:
            owner, ctype = self.__get_object_for_this_type(owner_type, owner_id)
        except ObjectDoesNotExist:
            return self.none()

        return self.filter(owner_type=ctype, owner_object_id=owner.id,)

    def find_all_tags_for(self, target_type, target_id):
        """Returns all tags defined on an object."""
        target_type = PROXY_MODEL_NAME if target_type in OPAQUE_KEY_PROXY_MODEL_TARGETS else target_type

        try:
            target, ctype = self.__get_object_for_this_type(target_type, target_id)
        except ObjectDoesNotExist:
            return self.none()

        return self.filter(target_type=ctype, target_object_id=target.id,)

    def find_all_tags_by_type(self, object_type):
        """Returns all tags with target_type equals to object_type."""
        return self.filter(target_type__model__exact=object_type)

    def hard_delete(self):
        """ Method for deleting Tag objects"""
        return super(TagQuerySet, self).delete()

    def __get_object_for_this_type(self, object_type, object_id):
        """Function that returns the correct content type given a type."""
        ctype = ContentType.objects.get(model=object_type)

        if object_type == PROXY_MODEL_NAME:
            object_id = object_id.get("course_id")
            object_id = {
                "opaque_key": CourseKey.from_string(object_id),
            }

        if object_type == COURSE_ENROLLMENT_MODEL_NAME:
            object_id = {
                "course_id": CourseKey.from_string(object_id.get("course_id")),
                "user__username": object_id.get("username"),
            }

        object_instance = ctype.get_object_for_this_type(**object_id)

        return object_instance, ctype


@python_2_unicode_compatible
class OpaqueKeyProxyModel(models.Model):
    """Model used to tag objects with opaque keys."""
    opaque_key = CourseKeyField(max_length=255)
    objects = models.Manager()

    def __str__(self):
        """Method that returns the opaque_key string representation."""
        return str(self.opaque_key)


@python_2_unicode_compatible
class Tag(models.Model):
    """
    Model class for tags.

    Overrides save method to validate data entries before saving.
    Also, overrides delete so softDeletion is available.

    Attributes:
        tag_value: unicode value of the tag. Example: free or premium
        tag_type: type of the tag. Example: Subscription tiers
        access: access level of the tag
        activation_date: date to activate the tag
        expiration-date: date to deactivate de tag
        target_object: object to tag
        belongs_to: object to which the tag belongs
        status: status of the tag, valid or invalid
        invalidated_at: date when the tag is soft deleted
    """
    key = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="Public identifier",
    )

    tag_value = models.CharField(max_length=150)
    tag_type = models.CharField(max_length=150)
    access = models.PositiveIntegerField(
        choices=AccessLevel.choices(), default=AccessLevel.PUBLIC,
    )
    activation_date = models.DateTimeField(null=True, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    status = models.PositiveIntegerField(
        choices=Status.choices(), default=Status.ACTIVE, editable=False,
    )

    inactivated_at = models.DateTimeField(blank=True, null=True, editable=False)

    # Generic foreign key for tagged objects
    target_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="%(class)s_type",
        null=True,
        blank=True,
    )
    target_object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    target_object = GenericForeignKey("target_type", "target_object_id")

    # Generic foreign key for `tag belonging to` USER or SITE
    owner_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="owner_%(class)s_type",
        null=True,
        blank=True,
    )
    owner_object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    owner_object = GenericForeignKey("owner_type", "owner_object_id")

    objects = TagQuerySet().as_manager()

    class Meta:  # pylint: disable=old-style-class, useless-suppression
        """Meta class. """
        verbose_name = "tag"
        verbose_name_plural = "tags"
        app_label = "eox_tagging"

    def __str__(self):
        return self.tag_value

    @property
    def target_object_type(self):
        """Obtain the name of the object target by the `Tag`."""
        return self.target_object.__class__.__name__ if self.target_object else None

    @property
    def owner_object_type(self):
        """Obtain the name of the object which the tag belongs to."""
        return self.owner_object.__class__.__name__ if self.owner_object else None

    def set_attribute(self, attr, value):
        """Function that takes a value and sets it to the instance attribute."""
        if attr == "access":
            self.access = AccessLevel.get_access_object(value)
            return

        if attr == "activation_date":
            self.activation_date = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            return

        if attr == "expiration_date":
            self.expiration_date = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            return

        setattr(self, attr, value)

    def get_attribute(self, attr, name=False):
        """
        Function used to format attributes getting them from self object.

        Arguments:
            - name: used if attr is target or owner and want to get the class name.
        """

        if attr and re.match(r".+object$|.+object_type$", attr):
            return self.__get_model(attr, name)

        if attr == 'access':
            return self.__get_field_choice(attr)

        return getattr(self, attr)

    def __get_model(self, attr, name):
        """
        Function that gets the type stored by the proxy model. This function is called when we want
        the actual type of the target object.

        Arguments:
            - attr: name of the attr
            - name: in case we want the class and not the object
        """

        field_value = getattr(self, "{}_type".format(attr))
        if name:
            return field_value
        else:
            return getattr(self, attr)

    def __get_field_choice(self, attr):
        """
        Function that gets the choice of the choice field

        Arguments:
            - attr: name of the attr
            - name: in case we want the class and not the object
        """
        field_value = getattr(self, attr)

        try:
            choice = getattr(field_value, "name")
            return choice
        except AttributeError:
            choice = AccessLevel.get_choice(field_value)
            return choice

    def clean(self):
        """
        Validates inter-field relations
        """
        self.validator.validate_fields()

    def clean_fields(self):  # pylint: disable=arguments-differ
        """
        Validates fields individually
        """
        if getattr(settings, "EOX_TAGGING_SKIP_VALIDATIONS", False):  # Skip these validations while testing
            return
        self.validator.validate_fields_integrity()

    def full_clean(self, exclude=None, validate_unique=False):
        """
        Call clean_fields(), clean(), and validate_unique() -not implemented- on the model.
        Raise a ValidationError for any errors that occur.
        """
        self.validator = TagValidators(self)  # pylint: disable=attribute-defined-outside-init
        self.clean()
        self.clean_fields()

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        self.full_clean()
        super(Tag, self).save(*args, **kwargs)

    def delete(self):  # pylint: disable=arguments-differ
        self.inactivated_at = timezone.now()
        self.status = Status.INACTIVE
        super(Tag, self).save()

    def hard_delete(self):
        """Deletes object from database."""
        super(Tag, self).delete()
