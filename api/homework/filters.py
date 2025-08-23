from django_filters import FilterSet, CharFilter, NumberFilter
from content.models import Homework


class HomeworkFilter(FilterSet):

    lecture_name = CharFilter(field_name="lecture__topic", lookup_expr="icontains")
    homework_title = CharFilter(field_name="title", lookup_expr="icontains")
    homework_id = NumberFilter("id", lookup_expr="exact")

    class Meta:
        model = Homework
        fields = []
