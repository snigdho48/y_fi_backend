from drf_spectacular.utils import extend_schema, OpenApiResponse,OpenApiExample
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.serializer import CustomConnectedHistorySerializer
import requests
from api.models import PartnerProfile,ConnectedHistory

class DataCollectView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=CustomConnectedHistorySerializer,
        responses={200: OpenApiResponse(response=CustomConnectedHistorySerializer)}
    )
    def post(self, request):
        
        request.data['user'] = request.user.id
        serializer = CustomConnectedHistorySerializer(data=request.data)
        url = 'https://cms.freeyfi.com/api/v1/app_connection_data/'
        
        if serializer.is_valid():
            serializer.save()
            history = ConnectedHistory.objects.get(uuid=serializer.data['uuid'])
            payload = {
                    "user": history.user.username,
                    "partner": history.partner.venue_name,
                    "ip": history.ip,
                    "device_os": history.device_os,
                    "device_name": history.device_name,
                    "device_brand": history.device_brand,
                    "device_id": history.device_id
                }
            
            try:
                    resp =requests.post(url, json=payload)
                    status_code = resp.status_code
                    if status_code in [200, 201]:
                        history.delete()

            except Exception as e:
                    pass
            return Response({"message": "Data sent successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)