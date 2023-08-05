"""
Custom API permissions module
"""
from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.db.utils import ProgrammingError
from rest_framework import exceptions, permissions


def load_permissions():
    """
    Helper method to load a custom permission on DB that will be use to give access
    to eox-tagging API.
    """
    if settings.EOX_TAGGING_LOAD_PERMISSIONS:
        try:
            content_type = ContentType.objects.get_for_model(User)
            Permission.objects.get_or_create(
                codename='can_call_eox_tagging',
                name='Can access eox-tagging API',
                content_type=content_type,
            )
        except ProgrammingError:
            # This code runs when the app is loaded, if a migration has not been done a ProgrammingError
            # exception is raised we are bypassing those cases to let migrations run smoothly.
            pass


class EoxTaggingAPIPermission(permissions.BasePermission):
    """
    Defines a custom permissions to access eox-tagging API
    These permissions make sure that a token is created with the client credentials of the same site is being used on.
    """

    def has_permission(self, request, view):
        """
        To grant access, checks if the requesting user either can call eox-tagging API or if it's an admin user.
        """
        try:
            allowed_for_site = request.user.is_staff or request.get_host() in request.auth.client.url
        except Exception:  # pylint: disable=broad-except
            allowed_for_site = False

        if not allowed_for_site:
            # If we get here either someone is using a token created on one site in a different site
            # or there was a missconfiguration of the oauth client.
            # To prevent leaking important information we return the most basic message.
            raise exceptions.NotAuthenticated(detail="Invalid token")

        return request.user.has_perm('auth.can_call_eox_tagging') or request.user.is_staff
