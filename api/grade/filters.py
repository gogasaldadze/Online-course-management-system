from django_filters import FilterSet, CharFilter, NumberFilter, RangeFilter
from content.models import Grade


class GradeFilter(FilterSet):
    submission_uuid = CharFilter(field_name="submission__uuid", lookup_expr="exact")

    min_points = NumberFilter(field_name="points", lookup_expr="gte")

    max_points = NumberFilter(field_name="points", lookup_expr="lte")

    points_range = RangeFilter(field_name="points", label="Points Range")

    class Meta:
        model = Grade
        fields = ["submission_uuid", "min_points", "max_points", "points_range"]
