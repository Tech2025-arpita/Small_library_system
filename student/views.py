from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from .models import Student
from .serializers import StudentSerializer
import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


logger = logging.getLogger(__name__)

class StudentListCreateView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):

        stdt_id = request.query_params.get("stdt_id")
        stdt_name = request.query_params.get("stdt_name")

        allowed_params = [
            "stdt_id",
            "stdt_name"
        ]

        for param in request.query_params:
            if param not in allowed_params:
                return Response(
                    {
                        "message": "Invalid Parameter"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        if stdt_id:
            queryset = self.get_queryset().filter(stdt_id=stdt_id)

        elif stdt_name:
            queryset = self.get_queryset().filter(stdt_name__iexact=stdt_name)

        else:
            queryset = self.get_queryset()

        if not queryset.exists():
            return Response(
                {
                    "message": "No student found matching your search criteria."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if stdt_id or stdt_name:
            serializer = self.get_serializer(queryset.first())

        else:
            serializer = self.get_serializer(queryset,many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        logger.info("Request Data : %s",request.data) #NOSONAR

        response = {}

        try:
            if Student.objects.filter(stdt_name__iexact=request.data.get("stdt_name")).exists():
                response["message"] = "Student already exists"
                return Response(response,status=status.HTTP_400_BAD_REQUEST)

            return self.create(request,*args,**kwargs)

        except Exception as exp:
            logger.exception(exp)
            response["message"] = "Something went wrong" #NOSONAR
            return Response(response,status=status.HTTP_400_BAD_REQUEST)


class StudentUpdateView(
    mixins.UpdateModelMixin,
    GenericAPIView
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def put(self, request, *args, **kwargs):

        logger.info("Request Data : %s",request.data)
        response = {}
        stdt_id = kwargs["pk"]
        try:
            student_objs = Student.objects.filter(stdt_name__iexact=request.data.get("stdt_name"))
            if student_objs.exclude( stdt_id=stdt_id).exists():
                response["message"] = "Student Name Already Exists"
                return Response(response,status=status.HTTP_400_BAD_REQUEST)

            kwargs["partial"] = True
            return self.update(request,*args,**kwargs)

        except Exception as exp:
            logger.exception(exp)
            response["message"] = "Something went wrong"
            return Response(response,status=status.HTTP_400_BAD_REQUEST)


class StudentDestroyView(
    mixins.DestroyModelMixin,
    GenericAPIView
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def delete(self, request, *args, **kwargs):

        logger.info("Request Data : %s",request.data)
        response = {}
        stdt_id = kwargs["pk"]

        try:
            student = self.get_queryset().filter(stdt_id=stdt_id)

            if not student.exists():

                response["message"] = "Student not found"

                return Response(response,status=status.HTTP_404_NOT_FOUND)

            self.destroy(request,*args,**kwargs)
            response["message"] = "Student deleted successfully"
            return Response(response,status=status.HTTP_200_OK)

        except Exception as exp:
            logger.exception(exp)
            response["message"] = "Something went wrong"
            return Response(response,status=status.HTTP_400_BAD_REQUEST)