from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse

from content.models import GradeComment, Grade
from .serializers import GradeCommentSerializer
from api.permissions import CanCommentGrade


from schema.comments.schemas import grade_comments_list, grade_comment_create


@extend_schema_view(get=grade_comments_list, post=grade_comment_create)
class GradeCommentListCreateView(ListCreateAPIView):
    serializer_class = GradeCommentSerializer
    permission_classes = [IsAuthenticated, CanCommentGrade]

    def get_queryset(self):
        grade_uuid = self.kwargs.get("grade_uuid")
        try:
            grade = Grade.objects.get(uuid=grade_uuid)
        except Grade.DoesNotExist:
            raise NotFound("Grade not found.")
        return GradeComment.objects.filter(grade=grade)

    def perform_create(self, serializer):
        grade_uuid = self.kwargs.get("grade_uuid")
        try:
            grade = Grade.objects.get(uuid=grade_uuid)
        except Grade.DoesNotExist:
            raise NotFound("Grade not found.")

        self.check_object_permissions(self.request, grade)
        serializer.save(author=self.request.user, grade=grade)
