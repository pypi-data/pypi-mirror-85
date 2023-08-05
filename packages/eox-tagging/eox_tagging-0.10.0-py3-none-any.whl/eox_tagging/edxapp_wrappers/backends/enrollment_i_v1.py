"""
Backend CourseEnrollments file, here is the method to access enrollments
objects.
"""


def get_enrollment_object():
    """Backend to get enrollment object."""
    try:
        from student.models import CourseEnrollment
    except ImportError:
        CourseEnrollment = object
    return CourseEnrollment
