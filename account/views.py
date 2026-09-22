from rest_framework.views import APIView
from .serializers import SignUpSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

class SignUpView(APIView):
    permission_classes = [AllowAny]


    def post(self, request):
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response(
                {
                    "message": "Login successful!",
                    "data": serializer.validated_data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "message": "Error Occurred!!",
                "data": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


