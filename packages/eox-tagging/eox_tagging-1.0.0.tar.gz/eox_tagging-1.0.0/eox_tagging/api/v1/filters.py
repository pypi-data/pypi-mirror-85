"""Filter module for tags."""
from django_filters import rest_framework as filters

from eox_tagging.constants import AccessLevel
from eox_tagging.models import Tag

PROXY_MODEL_NAME = "opaquekeyproxymodel"


class TagFilter(filters.FilterSet):
    """Filter class for tags."""

    course_id = filters.CharFilter(method="filter_by_target_object")
    username = filters.CharFilter(method="filter_by_target_object")
    enrollments = filters.CharFilter(method="filter_by_target_object")
    target_type = filters.CharFilter(method="filter_target_types")
    created_at = filters.DateTimeFromToRangeFilter()
    activation_date = filters.DateTimeFromToRangeFilter()
    access = filters.CharFilter(method="filter_access_type")

    class Meta:  # pylint: disable=old-style-class, useless-suppression
        """Meta class."""
        model = Tag
        fields = ['key', 'status']

    def filter_by_target_object(self, queryset, name, value):
        """Filter that returns the tags associated with target."""
        TARGET_TYPES = {
            "course_id": "courseoverview",
            "username": "user",
            "enrollment": "courseenrollment",
        }
        if value:
            TARGET_IDENTIFICATION = {
                "enrollment": {
                    "username": self.request.user.username,
                    "course_id": str(value),
                },
            }
            DEFAULT = {
                name: str(value),
            }
            try:
                filter_params = {
                    "target_type": TARGET_TYPES.get(name),
                    "target_id": TARGET_IDENTIFICATION.get(name, DEFAULT),
                }
                queryset = queryset.find_all_tags_for(**filter_params)
            except Exception:  # pylint: disable=broad-except
                return queryset.none()

        return queryset

    def filter_target_types(self, queryset, name, value):  # pylint: disable=unused-argument
        """Filter that returns targets by their type."""
        if value:
            try:
                queryset = queryset.find_all_tags_by_type(str(value))
            except Exception:  # pylint: disable=broad-except
                return queryset.none()

        return queryset

    def filter_access_type(self, queryset, name, value):  # pylint: disable=unused-argument
        """Filters targets by their access type."""
        if value:
            value_map = {v.lower(): k for k, v in AccessLevel.choices()}
            access = value_map.get(value.lower())
            queryset = queryset.filter(access=access) if access else queryset.none()

        return queryset
