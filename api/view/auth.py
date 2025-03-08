
from rest_framework_simplejwt.views import TokenObtainPairView
from api.serializer import MyTokenObtainPairSerializer, MyTokenObtainPartnerPairSerializer,PartnerProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class PartnerTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPartnerPairSerializer
    
class PartnerRegistrationView(APIView):
    authentication_classes = []
    permission_classes = []
    @extend_schema(
        request=PartnerProfileSerializer,
        responses=PartnerProfileSerializer
    )
    def post(self,request):
        serializer = PartnerProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Partner registered successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)   
    
        

class LogoutAPIView(APIView):
    def get(self, request, format=None):
        refresh_token = request.headers.get('Authorization')

        if refresh_token:
            try:
                token = RefreshToken(refresh_token.split(' ')[1])
                token.blacklist() 
                return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Refresh token not found"}, status=status.HTTP_400_BAD_REQUEST)