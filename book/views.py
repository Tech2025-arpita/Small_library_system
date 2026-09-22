import logging

from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Book
from .serializers import BookSerializer


logger = logging.getLogger(__name__)

class BookListCreateView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):

        bk_id = request.query_params.get("bk_id")
        bk_name = request.query_params.get("bk_name")

        allowed_params = [
            "bk_id",
            "bk_name"
        ]

        for param in request.query_params:
            if param not in allowed_params:
                return Response(
                    {
                        "message": "Invalid Parameter"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        if bk_id:
            queryset = self.get_queryset().filter(bk_id=bk_id)
            serializer = self.get_serializer(queryset.first())

        elif bk_name:
            queryset = self.get_queryset().filter(bk_name__iexact=bk_name)
            serializer = self.get_serializer(queryset.first())

        else:
            queryset = self.get_queryset()

        if not queryset.exists():
            return Response(
                {
                    "message": "No book found matching your search criteria."
                },
                status=status.HTTP_404_NOT_FOUND
            )
           
        # else:
        #     serializer = self.get_serializer(queryset,
        #         many=True
        #     )

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Book create"""

        logger.info("Request Data : %s",request.data)#NOSONAR
        response = {}

        try:
            if Book.objects.filter(bk_name__iexact=request.data.get("bk_name")).exists():

                response["message"] = "Book already exists"
                return Response(response,status=status.HTTP_400_BAD_REQUEST)

            return self.create(request,*args,**kwargs)

        except Exception as exp:
            logger.exception(exp)
            response["message"] = "Something went wrong" #NOSONAR
            return Response(response,status=status.HTTP_400_BAD_REQUEST)


class BookUpdateView(
    mixins.UpdateModelMixin,
    GenericAPIView
):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def put(self, request, *args, **kwargs):
        """Book update"""

        logger.info("Request Data : %s",request.data)
        response = {}
        bk_id = kwargs["pk"]

        try:
            book_objs = Book.objects.filter(bk_name__iexact=request.data.get("bk_name"))

            if book_objs.exclude(bk_id=bk_id).exists():

                response["message"] = "Book Name Already Exists"

                return Response(response,status=status.HTTP_400_BAD_REQUEST)

            kwargs["partial"] = True

            return self.update(request,*args,**kwargs)

        except Exception as exp:
            logger.exception(exp)
            response["message"] = "Something went wrong"
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

class BookDestroyView(
    mixins.DestroyModelMixin,
    GenericAPIView
):
    """Book Delete"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def delete(self, request, *args, **kwargs):

        logger.info("Request Data : %s",request.data)
        response = {}
        bk_id = kwargs["pk"]

        try:
            book = Book.objects.filter(bk_id=bk_id)

            if not book.exists():
                response["message"] = "Book not found"
                return Response(response,status=status.HTTP_404_NOT_FOUND)

            self.destroy(request,*args,**kwargs)

            response["message"] = "Book deleted successfully"

            return Response(response,status=status.HTTP_200_OK)

        except Exception as exp:
            logger.exception(exp)
            response["message"] = "Something went wrong"
            return Response(response,status=status.HTTP_400_BAD_REQUEST)