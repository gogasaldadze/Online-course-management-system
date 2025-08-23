from django_filters import FilterSet, CharFilter, NumberFilter
from content.models import Lecture


class TeacherLectureFilter(FilterSet):

    topic = CharFilter(field_name="topic", lookup_expr="icontains")
    course_name = CharFilter(field_name="course__name", lookup_expr="icontains")

    class Meta:
        model = Lecture
        fields = ["topic", "course_name"]


class LectureFilter(FilterSet):

    topic = CharFilter(field_name="topic", lookup_expr="icontains")
    id = NumberFilter(field_name="id", lookup_expr="exact")

    class Meta:
        model = Lecture
        fields = ["topic", "id"]
