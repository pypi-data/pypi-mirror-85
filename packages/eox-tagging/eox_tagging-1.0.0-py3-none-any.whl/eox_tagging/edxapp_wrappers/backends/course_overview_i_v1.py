"""
Backend CourseOverview file, here are all the methods from
openedx.core.djangoapps.content.course_overviews.
"""


def get_course_overview():
    """Backend to get course overview."""
    try:
        from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
    except ImportError:
        CourseOverview = object
    return CourseOverview
