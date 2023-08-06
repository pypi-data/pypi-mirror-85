=============
eox_tagging
=============

Features
=========

Place your plugin features list.

Installation
============


Open edX devstack
------------------

- Clone this repo in the src folder of your devstack.
- Open a new Lms/Devstack shell.
- Install the plugin as follows: pip install -e /path/to/your/src/folder
- Restart Lms/Studio services.


Usage
======

Important notes:
----------------

* All the comparison with string objects are case insensitive.
* validate_<FIELD_VALUE> meaning:

  * The FIELD_VALUE must be a Tag field, if not an exception will be raised.
  * If this is defined in EOX_TAGGING_DEFINITIONS as one of the tag definitions:

    ``validate_<FIELD_VALUE_1>: <VALIDATIONS>``

    * The application will expect that <VALIDATIONS> is a dictionary of validations or a string.

    * This dictionary has for keys the validations you want to perform and for values, the values allowed for the field. In case it is a string, the field must be equal to that string.

    * If a key or value is not defined then an exception will be raised. In case that is a string, the field must be equal to that string.

  * If this is defined:

    ``<FIELD_VALUE>: <VALIDATIONS>``

    * The application will expect just a string as a validation. This is also a way to define the required fields.

    * The settings for EOX_TAGGING_DEFINITIONS can be a combination of dictionary validations and strings.

  * If a key in the settings dictionary has as prefix `validate` it means that the <key, value> can have a dictionary of validations as value. If not, is assume that
      value is a string.

* force_<FIELD_VALUE> meaning:

    * This allows to set a value to a field without running validations or directly specifying it in the tag object.

* The validations available are:

+---------------+-------+-----------------------------------------------+----------------------------------------------------------------+
| Name          | Description                                           | Example                                                        |
+===============+=======================================================+================================================================+
| ``in``        | the field must be equal to one of the strings defined | ``validate_tag_value : {"in": ["tag_value_1", "tag_value_2"]}``|
|               | inside the array                                      |                                                                |
+---------------+-------------------------------------------------------+----------------------------------------------------------------+
| ``exists``    | the field must be different to None                   |  ``validate_tag_value : {"exists": true}``                     |
+---------------+-------------------------------------------------------+----------------------------------------------------------------+
|  ``equals``   | the field must be equal to the dictionary value       |  ``validate_tag_value : {"equals": "tag_value"}``              |
+---------------+-------------------------------------------------------+----------------------------------------------------------------+
|  ``regex``    | the field must match the pattern defined              |  ``validate_tag_value : {"regex": ".+eduNEXT"}``               |
+---------------+-------------------------------------------------------+----------------------------------------------------------------+
|``opaque_key`` | the field must be an opaque key                       |  ``validate_tag_value : {"opaque_key": "CourseKey"}``          |
+---------------+-------------------------------------------------------+----------------------------------------------------------------+
| ``between``   | the field must be greater than the first member of    |  ``validate_expiration_date : {"between": [DATE_1, DATE_2]}``  |
|               | the list and less than the last member. Or can be     |                                                                |
|               | equal to one of the two. The list must be sorted.     |                                                                |
+---------------+-------------------------------------------------------+----------------------------------------------------------------+


* The available objects to tag and validate are: User, Site, CourseOverview and CourseEnrollment

* If an owner is not defined, then it is assumed to be the site.

Examples
--------

**Example 1:**

.. code-block:: JSON

        {
            "validate_tag_value":{
                "in":[
                    "example_tag_value",
                    "example_tag_value_1"
                ]
            },
            "validate_access":{
                "equals":"PRIVATE"
            },
            "validate_target_object":"OpaqueKeyProxyModel",
            "owner_object":"User",
            "tag_type":"tag_by_example"
        }

This means that:

* Tag value must be in the array
* The field access must be equal to `private`
* The target type must be equal to `CourseOverview`
* The owner type must be equal to `User`
* Tag_type must be equal to `tag_by_example`

**Example 2:**

.. code-block:: JSON

        {
            "validate_tag_value":{
                "exist":true
            },
            "validate_access":"Public",
            "validate_target_object":"User",
            "tag_type":"tag_by_edunext"
        }

This means that:

* The tag value must exist, it can take any value.
* The field access must be equal to `public`.
* The target type must be equal to `User`.
* Tag type must be equal to tag_by_edunext.

**Example 3:**

.. code-block:: JSON

        {
            "validate_tag_value":"tag_value",
            "validate_access":{
                "in":[
                    "Private",
                    "Public"
                ]
            },
            "validate_target_object":"CourseEnrollment",
            "tag_type":"tag_by_edunext",
            "validate_activation_date":{
                "exist":true,
                "in":[
                    "Dec 04 2020 10:30:40",
                    "Oct 19 2020 10:30:40"
                ]
            }
        }

This means that:

* The tag value must be equal to tag_value.
* The field access can be `private` or `public`.
* The target type must be equal to `CourseEnrollment`
* Tag type must be equal to tag_by_edunext.
* The tag activation date must exist and be between the values defined in the array. This means: value_1 <= activation_date <= value_2.
  The array must be sorted or a validation error will be raised.

Tagging REST API
================

Get list of tags
----------------

**Request**

``curl -H 'Accept: application/json' -H "Authorization: Bearer AUTHENTICATION_TOKEN" http://BASE_URL_SITE/eox_tagging/api/v1/tags/``

**Response**

.. code-block:: JSON

        {
            "count": 2,
            "next": null,
            "previous": null,
            "results": [
                {
                    "meta": {
                        "created_at": "2020-07-10T13:25:54.057846Z",
                        "target_id": 2,
                        "target_type": "User",
                        "inactivated_at": null,
                        "owner_type": "User",
                        "owner_id": 7
                    },
                    "key": "55a20579-ce8e-4f0b-830e-78fe79adac46",
                    "tag_value": "tag_value",
                    "tag_type": "tag_by_edunext",
                    "access": "PUBLIC",
                    "activation_date": "2020-12-04T15:20:30Z",
                    "expiration_date": null,
                    "status": "ACTIVE"
                },
                {
                    "meta": {
                        "created_at": "2020-07-10T13:33:44.277374Z",
                        "target_id": 2,
                        "target_type": "User",
                        "inactivated_at": null,
                        "owner_type": "Site",
                        "owner_id": 1
                    },
                    "key": "2bec10f5-a9e0-4e42-9c24-f9643bb13537",
                    "tag_value": "tag_value",
                    "tag_type": "tag_by_edunext",
                    "access": "PUBLIC",
                    "activation_date": "2020-12-04T15:20:30Z",
                    "expiration_date": null,
                    "status": "ACTIVE"
                },
            ]
        }

Create tag
----------

**Request**

``curl -H 'Accept: application/json' -H "Authorization: Bearer AUTHENTICATION_TOKEN" --data TAG_DATA http://BASE_URL_SITE/eox_tagging/api/v1/tags/``

Where TAG_DATA:

.. code-block:: JSON

        {
            "tag_type": "tag_by_edunext",
            "tag_value": "tag_value",
            "target_type": "user",
            "target_id": "edx",
            "access": "public",
            "owner_type": "user",
            "activation_date": "2020-12-04 10:20:30"
        }


**Response**:

``Status 201 Created``

.. code-block:: JSON

        {
            "meta": {
                "created_at": "2020-07-10T13:25:54.057846Z",
                "target_id": 2,
                "target_type": "User",
                "inactivated_at": null,
                "owner_type": "User",
                "owner_id": 7
            },
            "key": "55a20579-ce8e-4f0b-830e-78fe79adac46",
            "tag_value": "tag_value",
            "tag_type": "tag_by_edunext",
            "access": "PUBLIC",
            "activation_date": "2020-12-04T10:20:30-05:00",
            "expiration_date": null,
            "status": "ACTIVE"
        }

Delete tag
----------

**Request**

``curl -X DELETE  http://BASE_URL_SITE/eox_tagging/api/v1/tags/EXISTING_KEY_TAG/``

**Response**

``Status 204 No Content``


Filters example usage:
----------------------

``/eox_tagging/api/v1/tags/?target_type=MODEL_TYPE``

``/eox_tagging/api/v1/tags/?course_id=COURSE_ID``

``/eox_tagging/api/v1/tags/?username=USERNAME``

``/eox_tagging/api/v1/tags/?access=ACCESS_TYPE``

``/eox_tagging/api/v1/tags/?enrollments=COURSE_ID``

##Contributing

Add your contribution policy. (If required)
