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
    



