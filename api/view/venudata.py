from drf_spectacular.utils import extend_schema, OpenApiResponse,OpenApiExample
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.serializer import PartnerProfileSerializer,CustomPartnerProfileSerializerRegister,VenudataViewSerializer
from api.models import PartnerProfile



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
        responses={200: OpenApiResponse(response=PartnerProfileSerializer),400: OpenApiResponse(response={
            "type": "object",
            "properties": {
                "error": {"type": "string"}
            }
        },
            examples=[
                OpenApiExample(
                    name="Venu Not Found",
                    value={"error": "Venu Not Found"},
                    response_only=True
                ),
                OpenApiExample(
                    name="Venu Code not found",
                    value={"error": "Venu Code is required"},
                    response_only=True
                )
            ]
        )
        }
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
    
class AddVenuWifiDataView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "ssid": {"type": "string"},
                    "password": {"type": "string"}
                }
            }
        },
        responses={
            200: OpenApiResponse(
                response=VenudataViewSerializer(many=True),
               
            ),
            400: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "detail": {"type": "string"}
                    }
                },
                examples=[
                    OpenApiExample(
                        name="SSID or password not found",
                        value={"detail": "SSID and password are required."},
                        response_only=True
                    ),
                    OpenApiExample(
                        name="Invalid credentials",
                        value={"detail": "Unauthorized"},
                        response_only=True
                    )
                ]
            )
        }
    )
    def post(self, request):
        
        user = request.user
        group = user.groups.first()
        if group.name != 'partner':
                return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        partner = PartnerProfile.objects.filter(user=user).first()
        if not partner:
            return Response({"error": "Partner not found"}, status=status.HTTP_400_BAD_REQUEST)
        venu_routers = PartnerProfile.objects.filter(user=user).count()
        venu_name = partner.venue_name
        address = partner.address   
        phone_number = partner.phone_number
        
        request.data['venue_name'] = venu_name
        request.data['address'] = address
        request.data['phone_number'] = phone_number
        request.data['user'] = user.id
        request.data['code'] = genrate_Unique_code(venu_name=venu_name,wifi_routers_length=venu_routers+1)
        
        
        serializer = CustomPartnerProfileSerializerRegister(data=request.data)
        if serializer.is_valid():
            serializer.save()
            all_wifi_routers = PartnerProfile.objects.filter(user=user)
            data= all_wifi_routers.exclude(ssid=None).exclude(password=None).exclude(code=None).exclude(ssid='').exclude(password='').exclude(code='')
            serializer_data = VenudataViewSerializer(data, many=True)
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteVenueDataView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "code": {"type": "string"}
                }
            }
        },
        responses={
            200: OpenApiResponse(
                response=VenudataViewSerializer(many=True),
               
            ),
            400: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "detail": {"type": "string"}
                    }
                },
                examples=[
                    OpenApiExample(
                        name="Code not found",
                        value={"detail": "Code is required."},
                        response_only=True
                    ),
                    OpenApiExample(
                        name="Invalid credentials",
                        value={"detail": "Unauthorized"},
                        response_only=True
                    ),
                    OpenApiExample(
                        name="Venu not found",
                        value={"detail": "Venue not found"},
                        response_only=True
                    )
                ]
            )
        }
    )
    def post(self, request):
        user = request.user
        group = user.groups.first()
        if group.name != 'partner':
                return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        code = request.data.get('code')
        if not code:
            return Response({"error": "Code is required"}, status=status.HTTP_400_BAD_REQUEST)
        partner = PartnerProfile.objects.filter(code=code).first()
        if not partner:
            return Response({"error": "Venue not found"}, status=status.HTTP_400_BAD_REQUEST)
        partner.delete()
        all_wifi_routers = PartnerProfile.objects.filter(user=user)
        data= all_wifi_routers.exclude(ssid=None).exclude(password=None).exclude(code=None).exclude(ssid='').exclude(password='').exclude(code='')
        serializer_data = VenudataViewSerializer(data, many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)
    
class UpdateVenueDataView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "code": {"type": "string"},
                    "ssid": {"type": "string"},
                    "password": {"type": "string"},
                    
                }
            }
        },
        responses={
            200: OpenApiResponse(
                response=VenudataViewSerializer(many=True),
               
            ),
            400: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "detail": {"type": "string"}
                    }
                },
                examples=[
                 
                    OpenApiExample(
                        name="Invalid credentials",
                        value={"detail": "Unauthorized"},
                        response_only=True
                    ),
                    OpenApiExample(
                        name="No Venue Found",
                        value={"detail": "Venue not found"},
                        response_only=True
                    ),
                    OpenApiExample(
                        name="SSID not found",
                        value={"detail": "SSID is required"},
                        response_only=True
                    ),
                    OpenApiExample(
                        name="Password not found",
                        value={"detail": "Password is required"},
                        response_only=True
                    ),
                    OpenApiExample(
                        name="Code not found",
                        value={"detail": "Code is required"},
                        response_only=True
                    )
                ]
            )
            
        }
    )
    def post(self, request):
        user = request.user
        group = user.groups.first()
        if group.name != 'partner':
                return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        code = request.data.get('code')
        if not code:
            return Response({"error": "Code is required"}, status=status.HTTP_400_BAD_REQUEST)
        ssid = request.data.get('ssid')
        if not ssid:
            return Response({"error": "SSID is required"}, status=status.HTTP_400_BAD_REQUEST)
        password = request.data.get('password')
        if not password:
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)
        partner = PartnerProfile.objects.filter(code=code).first()
        if not partner:
            return Response({"error": "Venue not found"}, status=status.HTTP_400_BAD_REQUEST)
        partner.ssid = ssid
        partner.password = password
        partner.save()
        all_wifi_routers = PartnerProfile.objects.filter(user=user)
        data= all_wifi_routers.exclude(ssid=None).exclude(password=None).exclude(code=None).exclude(ssid='').exclude(password='').exclude(code='')
        serializer_data = VenudataViewSerializer(data, many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)
    
class GetAllVenueDataView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=VenudataViewSerializer(many=True),
               
            ),
            400: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "detail": {"type": "string"}
                    }
                },
                examples=[
                    OpenApiExample(
                        name="Invalid credentials",
                        value={"detail": "Unauthorized"},
                        response_only=True
                    )
                ]
            )
        }
    )
    def get(self, request):
        user = request.user
        group = user.groups.first()
        if group.name != 'partner':
                return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        all_wifi_routers = PartnerProfile.objects.filter(user=user)
        data= all_wifi_routers.exclude(ssid=None).exclude(password=None).exclude(code=None).exclude(ssid='').exclude(password='').exclude(code='')
        
        serializer_data = VenudataViewSerializer(data, many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)


def genrate_Unique_code(venu_name,wifi_routers_length):
    venu_name = venu_name.replace(' ','_')
    code = venu_name.upper() + str(wifi_routers_length)
    return code
    