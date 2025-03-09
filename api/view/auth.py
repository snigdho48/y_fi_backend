
from rest_framework_simplejwt.views import TokenObtainPairView
from api.serializer import MyTokenObtainPairSerializer, MyTokenObtainPartnerPairSerializer,PartnerProfileSerializer,CustomPartnerProfileSerializerRegister
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse,OpenApiExample
from api.models import CustomUser
from django.contrib.auth.models import Group
from rest_framework_simplejwt.tokens import RefreshToken




class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
  

class PartnerTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPartnerPairSerializer
    
    
    
class PartnerRegistrationView(APIView):
    authentication_classes = []
    permission_classes = []
    @extend_schema(
        request=PartnerProfileSerializer,
        responses={200: OpenApiResponse(response=MyTokenObtainPartnerPairSerializer),400: OpenApiResponse(response={
            "type": "object",
            "properties": {
                "error": {"type": "string"}
            }
        },
            examples=[
                OpenApiExample(
                    name="User already exists",
                    value={"error": "User already exists"},
                    response_only=True
                ),
                OpenApiExample(
                    name="Invalid credentials",
                    value={"error": "Invalid credentials"},
                    response_only=True
                )
            ]
        )}  
        
    
    )
    def post(self, request):
        if not request.data.get('email') or not request.data.get('userpassword'):
            return Response({"error": " Email and Password are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = CustomUser.objects.get(email=request.data.get('email'))
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:

            user = CustomUser.objects.create_user(
                    username=request.data.get('username', ''),
                    email=request.data.get('email'),
                    password=request.data.get('userpassword')  # Fix field name
                )
            group, _ = Group.objects.get_or_create(name='partner')
            user.groups.add(group)
            user.save()
            
            
            request.data['user']=user.id
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST   )
        
        request.data.pop('username')
        serializer = CustomPartnerProfileSerializerRegister(data=request.data)
        if serializer.is_valid():
            serializer.save()
            refresh = RefreshToken.for_user(user)
            data = {
                'token': str(refresh.access_token),
                'username': user.username,
                'email': user.email,
                'user_group': user.groups.first().name if user.groups.exists() else None,
            }
            return Response(data, status=status.HTTP_200_OK)
        
        user.delete()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        

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