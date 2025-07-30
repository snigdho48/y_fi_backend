from drf_spectacular.utils import extend_schema, OpenApiResponse,OpenApiExample,OpenApiParameter
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response



from api.models import *
from api.serializer import VenuDetailsSerializer,CustomUserSerializer


class VenuDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get venue details",
        description="Retrieve venue details based on user permissions. Partners can see their own venues, Admin/Users can see all venues.",
        responses={
            200: OpenApiResponse(response=VenuDetailsSerializer(many=True)),
            403: OpenApiResponse(response={'error': 'You are not authorized to access this resource'}),
        }
    )
    def get(self, request):
        user = request.user
        if user.groups.filter(name='Partner').exists():
            venu_details = VenuDetails.objects.filter(partner=user)
            serializer = VenuDetailsSerializer(venu_details, many=True)
            return Response(serializer.data,status= status.HTTP_200_OK)
        elif user.groups.filter(name__in=['admin','user']).exists():
            venu_details = VenuDetails.objects.all()
            serializer = VenuDetailsSerializer(venu_details, many=True)
            return Response(serializer.data,status= status.HTTP_200_OK)
        else:
            return Response({"error": "You are not authorized to access this resource"}, status=status.HTTP_403_FORBIDDEN)
        
    @extend_schema(
        summary="Create venue details",
        description="Create new venue details. Partners can create venues for themselves, Admins can create venues for any partner.",
        request=VenuDetailsSerializer,
        responses={
            201: OpenApiResponse(response=VenuDetailsSerializer),
            400: OpenApiResponse(response={'error': 'Invalid data provided'}),
            403: OpenApiResponse(response={'error': 'You are not authorized to access this resource'}),
        }
    )
    def post(self, request):
        user = request.user
        if user.groups.filter(name__in=['partner']).exists():
            data = request.data
            data['partner'] = user.id
            serializer = VenuDetailsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status= status.HTTP_201_CREATED)
            return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)
        elif user.groups.filter(name__in=['admin']).exists():
            data = request.data
            serializer = VenuDetailsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status= status.HTTP_201_CREATED)
            return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You are not authorized to access this resource"}, status=status.HTTP_403_FORBIDDEN)
        
        
class GetPartnersUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get all partner users",
        description="Retrieve all users who belong to the Partner group. Only accessible by Admin users.",
        responses={
            200: OpenApiResponse(response=CustomUserSerializer(many=True)),
            403: OpenApiResponse(response={'error': 'You are not authorized to access this resource'}),
        }
    )
    def get(self, request):
        user = request.user
        if user.groups.filter(name__in=['admin']).exists():
            partners = CustomUser.objects.filter(groups__name='partner')
            serializer = CustomUserSerializer(partners, many=True)
            return Response(serializer.data,status= status.HTTP_200_OK)
        else:
            return Response({"error": "You are not authorized to access this resource"}, status=status.HTTP_403_FORBIDDEN)
        
        
        