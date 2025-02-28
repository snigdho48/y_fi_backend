from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.serializer import PartnerProfileSerializer
from api.models import PartnerProfile,CustomUser
from django.contrib.auth.models import Group



class VenueDataView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request={
            "application/json": {
                "example": {
                    "code": "code2"
                }
            }
        },
        responses={200: OpenApiResponse(response=PartnerProfileSerializer)}
    )
    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response({"error": "Venu Code is required"}, status=status.HTTP_400_BAD_REQUEST)
        partner = PartnerProfile.objects.filter(code=code).first()
        if not partner:
            return Response({"error": "Venu Not Found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PartnerProfileSerializer(partner)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CreatePartnerProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=PartnerProfileSerializer,
        responses={200: OpenApiResponse(response=PartnerProfileSerializer)}
    )
    def post(self, request):
        if not request.user.groups.filter(name='admin').exists():
            return Response({"error": "You do not have permission to create a partner profile"}, status=status.HTTP_403_FORBIDDEN)
        user= CustomUser.objects.create_user(username=request.data.get('username',' '), email=request.data.get('email'), password=request.data.get('password'))
        group, _ = Group.objects.get_or_create(name='partner')
        user.groups.add(group)
        user.save()
        
        
        request.data['user_id']=user.id
        
        

        serializer = PartnerProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)