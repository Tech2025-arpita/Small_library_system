import logging

from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Author
from .serializers import AuthorSerializer


logger = logging.getLogger(__name__)
request_data_key = "Request Data : %s"

class AuthorListCreateView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get(self, request, *args, **kwargs):
        auth_id = request.query_params.get("auth_id")
        auth_name = request.query_params.get("auth_name")

        allowed_params = [
            "auth_id",
            "auth_name"
        ]

        for param in request.query_params:
            if param not in allowed_params:
                return Response(
                    {
                        "message": "Invalid Parameter"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        if auth_id:
            queryset = self.get_queryset().filter(auth_id=auth_id)
            serializer = self.get_serializer(queryset.first())

        elif auth_name:
            queryset = self.get_queryset().filter(auth_name__iexact=auth_name)
            serializer = self.get_serializer(queryset.first())

        else:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset,many=True)

        if not queryset.exists():
            return Response(
                {
                    "message": "No author Found ."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Author create"""

        logger.info(request_data_key, request.data)
        response = {}

        try:
            if Author.objects.filter(auth_name__iexact=request.data.get("auth_name")).exists():

                response["message"] = "Author already exists"
                return Response(response,status=status.HTTP_400_BAD_REQUEST)

            return self.create(request,*args,**kwargs)

        except Exception as exp:
            logger.exception(exp)
            response["message"] = "Something went wrong" #NOSONAR
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

class AuthorUpdateView(
    mixins.UpdateModelMixin,
    GenericAPIView
):
    """Author update"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def put(self, request, *args, **kwargs):
        """Author update"""

        logger.info(request_data_key, request.data)
        response = {}
        auth_id = kwargs["pk"]

        try:
            auth_obj = Author.objects.filter(auth_name__iexact=request.data.get("auth_name"))

            if auth_obj.exclude(auth_id=auth_id).exists():
                response["message"] = "Author Name Already Exists"
                return Response(response,status=status.HTTP_400_BAD_REQUEST)

            kwargs["partial"] = True

            updt_res = self.update(request,*args,**kwargs)
            return updt_res

        except Exception as exp:
            logger.exception(exp)
            response["message"] = "Something went wrong"
            return Response(response,status=status.HTTP_400_BAD_REQUEST)


class AuthorDestroyView(
    mixins.DestroyModelMixin,
    GenericAPIView
):
    """Author Delete"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def delete(self, request, *args, **kwargs):

        logger.info(request_data_key, request.data)

        response = {}

        auth_id = kwargs["pk"]

        try:
            author = Author.objects.filter(auth_id=auth_id)

            if not author.exists():
                response["message"] = "Author not found"
                return Response(response,status=status.HTTP_404_NOT_FOUND)

            self.destroy(request,*args,**kwargs)

            response["message"] = "Author deleted successfully"

            return Response(response,status=status.HTTP_200_OK)

        except Exception as exp:
            logger.exception(exp)
            response["message"] = "Something went wrong"
            return Response(response,status=status.HTTP_400_BAD_REQUEST)