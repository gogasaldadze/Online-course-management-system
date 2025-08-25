from django_filters import FilterSet, CharFilter, NumberFilter
from content.models import Courses


class CourseFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains", label="course name")
    teacher_name = CharFilter(field_name="teacher__name", lookup_expr="icontains")

    class Meta:
        model = Courses
        fields = ["name", "teacher_name"]


class TeacherCourseFilter(FilterSet):

    student_name = CharFilter(field_name="student__name", lookup_expr="icontains")
    helper_id = NumberFilter(field_name="helpers__id")

    class Meta:
        model = Courses
        fields = ["student_name", "helper_id"]
