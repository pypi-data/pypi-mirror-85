Change Log
==========

..
   All enhancements and patches to eox-tagging will be documented
   in this file.  It adheres to the structure of http://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).

   This project adheres to Semantic Versioning (http://semver.org/).
.. There should always be an "Unreleased" section for changes pending release.

Unreleased
----------

[0.10.0] - 2020-10-13
--------------------

Added
_______

* Added support for filters in django2.2

[0.9.0] - 2020-10-05
--------------------

Added
_______

* Added support for Django 2.2.

[0.8.0] - 2020-09-30
--------------------

Added
_______

* Adding bearer_authentication to support django-oauth2-provider and django-oauth-toolkit

[0.7.0] - 2020-08-05
--------------------

Changed
_______

* Fixed case sensitive issue in the tag serializer with the fields `target_type` and `owner_type`.

[0.6.0] - 2020-08-03
--------------------

Added
_____

* The user can force a value in a field using the configuration.

Changed
_______

* Fixed datetime filters for activation_date and creation_date.

[0.5.0] - 2020-07-14
--------------------

Changed
_______

* Using - instead of _ for the urls namespace.

[0.4.0] - 2020-07-14
--------------------

Added
_____

* Added eox-tagging plugin documentation.
* Now invalid tags can be return using the `key` filter.
* Added info-view for the plugin.

Changed
_______

* The Technical information for the tag now is returned in a meta field.

[0.3.0] - 2020-07-08
--------------------

Added
_____

* Added validations only for DateTime fields.
* Added custom permissions to access the tag API.

Changed
_______

* Changed Date fields like expiration date and activation date to DateTime fields.
* Changed STATUS from valid/invalid to active/inactive.

[0.2.0] - 2020-06-26
---------------------

* REST API to create, get, filter and delete tags.
* New filters in Tag queryset.

* First PyPI release.

[0.1.0] - 2020-06-23
---------------------

Added
~~~~~

* First Github Release.
