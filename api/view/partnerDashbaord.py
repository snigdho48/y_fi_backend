import requests
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.models import PartnerProfile
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

class PartnerDashboardView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "partner": {"type": "string"}
                }
            }
        }
    )
    @extend_schema(
        responses={
            200: {
                "description": "Dashboard data retrieved successfully",
                "content": {"application/json": {"schema": {"type": "object"}}}
            },
            400: {
                "description": "Bad request"
            },
            500: {
                "description": "Internal server error"
            }
        }
    )
    
    def get(self, request):
        user = request.user
        partner = PartnerProfile.objects.get(user=user)
        venue_name = partner.venue_name
        url = 'https://venudata.in/api/partner/dashboard'
        payload ={
            'partner': venue_name
        },
        try:
            resp = requests.post(url, json=payload)
            status_code = resp.status_code
            resp_text = resp.text
            if status_code in [200, 201]:
                return Response(resp_text)
            else:
                return Response(status_code)
                        # Delete the history entry if sent successfully
               
        except Exception as e:
            return Response(e)
            
        
        

