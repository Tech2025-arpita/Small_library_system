from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from django.db.models import Count
from .models import BookIssue
from .serializers import BookIssueSerializer
import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


logger = logging.getLogger(__name__)

class BookIssueListCreateView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = BookIssue.objects.all()
    serializer_class = BookIssueSerializer

    def get(self, request, *args, **kwargs):
        issue_id = request.query_params.get("issue_id")
        book = request.query_params.get("book")
        student = request.query_params.get("student")

        allowed_params = [
            "issue_id",
            "book",
            "student"
        ]

        for param in request.query_params:
            if param not in allowed_params:
                return Response(
                    {
                        "message": "Invalid Parameter"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        if issue_id:
            queryset = self.get_queryset().filter(issue_id=issue_id)

            if not queryset.exists():
                return Response(
                    {
                        "message": "Book issue not found" #NOSONAR
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = self.get_serializer(
                queryset.first()
            )

            return Response(serializer.data)

        queryset = self.get_queryset()

        if book:
            queryset = queryset.filter(book=book)

        if student:
            queryset = queryset.filter(student=student)

        issue_count = (
            queryset
            .values("book", "student")
            .annotate(issue_count=Count("issue_id")).order_by("book", "student")
        )

        if not issue_count.exists():
            return Response(
                {"message": "No book issue found"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(issue_count)

    def post(self, request, *args, **kwargs):

        logger.info("Request Data : %s", request.data) #NOSONAR

        response = {}

        try:
            return self.create(request,*args,**kwargs)

        except Exception as exp:
            logger.exception(exp)
            response["message"] = "Something went wrong" #NOSONAR
            return Response(response,status=status.HTTP_400_BAD_REQUEST)


class BookIssueUpdateView(
    mixins.UpdateModelMixin,
    GenericAPIView
):
    """Book Issue update"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = BookIssue.objects.all()
    serializer_class = BookIssueSerializer

    def put(self, request, *args, **kwargs):

        logger.info("Request Data : %s", request.data)

        response = {}

        issue_id = kwargs["pk"]

        try:
            issue = self.get_queryset().filter(issue_id=issue_id)

            if not issue.exists():
                response["message"] = "Book issue not found"
                return Response(response,status=status.HTTP_404_NOT_FOUND)
            kwargs["partial"] = True

            return self.update(request,*args,**kwargs)

        except Exception as exp:
            logger.exception(exp)
            response["message"] = "Something went wrong"
            return Response(response,status=status.HTTP_400_BAD_REQUEST)


class BookIssueDestroyView(
    mixins.DestroyModelMixin,
    GenericAPIView
):
    """Book Issue Delete"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = BookIssue.objects.all()
    serializer_class = BookIssueSerializer

    def delete(self, request, *args, **kwargs):

        logger.info("Request Data : %s", request.data)
        response = {}
        issue_id = kwargs["pk"]

        try:
            issue = self.get_queryset().filter(issue_id=issue_id)

            if not issue.exists():
                response["message"] = "Book issue not found"
                return Response(response,status=status.HTTP_404_NOT_FOUND)

            self.destroy(request,*args,**kwargs)
            response["message"] = "Book issue deleted successfully"
            return Response(response,status=status.HTTP_200_OK)

        except Exception as exp:
            logger.exception(exp)
            response["message"] = "Something went wrong"
            return Response(response,status=status.HTTP_400_BAD_REQUEST)