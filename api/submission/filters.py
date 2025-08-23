from django_filters import FilterSet, CharFilter, NumberFilter
from content.models import HomeWorkSubmission


class SubmissionFilter(FilterSet):

    uuid = CharFilter(field_name="uuid", lookup_expr="exact")
    status = CharFilter(field_name="status", lookup_expr="exact")
    homework_name = CharFilter(field_name="homework__title", lookup_expr="icontains")

    class Meta:
        model = HomeWorkSubmission
        fields = []
