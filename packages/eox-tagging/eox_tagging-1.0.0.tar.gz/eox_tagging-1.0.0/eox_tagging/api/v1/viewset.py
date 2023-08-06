"""
Viewset for Tags.
"""
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication

from eox_tagging.api.v1.filters import TagFilter
from eox_tagging.api.v1.pagination import TagApiPagination
from eox_tagging.api.v1.permissions import EoxTaggingAPIPermission
from eox_tagging.api.v1.serializers import TagSerializer
from eox_tagging.edxapp_accessors import get_site
from eox_tagging.edxapp_wrappers.bearer_authentication import BearerAuthentication
from eox_tagging.models import Tag


class TagViewSet(viewsets.ModelViewSet):
    """Viewset for listing and creating Tags."""

    serializer_class = TagSerializer
    authentication_classes = (BearerAuthentication, SessionAuthentication)
    permission_classes = (EoxTaggingAPIPermission,)
    pagination_class = TagApiPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = TagFilter
    lookup_field = "key"
    http_method_names = ["get", "post", "delete", "head"]

    def get_queryset(self):
        """Restricts the returned tags."""
        queryset = Tag.objects.all()

        queryset = self.__get_objects_by_status(queryset)

        queryset = self.__get_objects_by_owner(queryset)

        return queryset

    def __get_objects_by_status(self, queryset):
        """Method that returns queryset filtered by tag status."""
        include_inactive = self.request.query_params.get("include_inactive")

        if "key" in self.request.query_params or self.action == "retrieve":
            include_inactive = "true"

        if not include_inactive or include_inactive.lower() not in ["true", "1"]:
            queryset = queryset.active()

        return queryset

    def __get_objects_by_owner(self, queryset):
        """Method that returns queryset filtered by tag owner"""
        owner_type = self.request.query_params.get("owner_type")
        owner_information = self.__get_request_owner(owner_type)

        try:
            queryset_union = queryset.none()
            for owner in owner_information:
                queryset_union |= queryset.find_by_owner(**owner)

            return queryset_union
        except Exception:  # pylint: disable=broad-except
            return queryset.none()

    def __get_request_owner(self, owner_type):
        """Returns the owners of the tag to filter the queryset."""
        site = self.__get_site()
        user = self.__get_user()

        if not owner_type:
            return [site, user]

        if owner_type.lower() == "user":
            return [user]

        if owner_type.lower() == "site":
            return [site]

        return []

    def __get_site(self):
        """Returns the current site."""
        site = get_site()

        return {
            "owner_id": {"id": site.id},
            "owner_type": "site",
        }

    def __get_user(self):
        """Returns the current user."""
        user = self.request.user

        return {
            "owner_id": {"username": user.username},
            "owner_type": "user",
        }
