from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from .models import BookReview
from .serializers import BookIssueSerializer
import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


logger = logging.getLogger(__name__)


class BookReviewListCreateView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = BookReview.objects.all()
    serializer_class = BookIssueSerializer

    def get(self, request, *args, **kwargs):

        review_id = request.query_params.get("review_id")
        book = request.query_params.get("book")
        author = request.query_params.get("author")
        stdt = request.query_params.get("stdt")

        allowed_params = [
            "review_id",
            "book",
            "author",
            "stdt"
        ]

        for param in request.query_params:
            if param not in allowed_params:
                return Response(
                    {
                        "message": "Invalid Parameter"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        if review_id:
            queryset = self.get_queryset().filter(review_id=review_id)

        elif book:
            queryset = self.get_queryset().filter(book=book)

        elif author:
            queryset = self.get_queryset().filter(author=author)

        elif stdt:
            queryset = self.get_queryset().filter(stdt=stdt)

        else:
            queryset = self.get_queryset()

        if not queryset.exists():
            return Response(
                {
                    "message": "No book review found matching your search criteria."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if review_id or book or author or stdt:
            serializer = self.get_serializer(queryset.first())

        else:
            serializer = self.get_serializer(queryset,many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        logger.info("Request Data : %s",request.data) #NOSONAR
        response = {}
        try:
            return self.create(request, *args,**kwargs)

        except Exception as exp:
            logger.exception(exp)
            response["message"] = "Something went wrong" #NOSONAR
            return Response(response,status=status.HTTP_400_BAD_REQUEST)


class BookReviewUpdateView(
    mixins.UpdateModelMixin,
    GenericAPIView
):
    """Book Review update"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = BookReview.objects.all()
    serializer_class = BookIssueSerializer

    def put(self, request, *args, **kwargs):

        logger.info("Request Data : %s",request.data)
        response = {}
        review_id = kwargs["pk"]
        try:
            review = self.get_queryset().filter(review_id=review_id)
            if not review.exists():
                response["message"] = "No Review Found"
                return Response(response,status=status.HTTP_404_NOT_FOUND)

            kwargs["partial"] = True

            return self.update(request, *args,**kwargs)

        except Exception as exp:
            logger.exception(exp)
            response["message"] = "Something went wrong"
            return Response(response,status=status.HTTP_400_BAD_REQUEST)


class BookReviewDestroyView(
    mixins.DestroyModelMixin,
    GenericAPIView
):
    """Book Review Delete"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = BookReview.objects.all()
    serializer_class = BookIssueSerializer

    def delete(self, request, *args, **kwargs):

        logger.info("Request Data : %s",request.data)
        response = {}
        review_id = kwargs["pk"]

        try:
            review = self.get_queryset().filter(review_id=review_id)

            if not review.exists():
                response["message"] = "Book review not found"

                return Response(response,status=status.HTTP_404_NOT_FOUND)

            self.destroy(request,*args,**kwargs)

            response["message"] = "Book review deleted successfully"

            return Response(response,status=status.HTTP_200_OK)

        except Exception as exp:

            logger.exception(exp)

            response["message"] = "Something went wrong"

            return Response(response,status=status.HTTP_400_BAD_REQUEST)