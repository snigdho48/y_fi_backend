from drf_spectacular.utils import extend_schema, OpenApiResponse,OpenApiExample,OpenApiParameter
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.serializer import *
from rest_framework.permissions import AllowAny
from api.models import Adsmodel, AdsViewHistory  # Ensure models are imported
from django.db.models import Sum
from api.serializer import PartnerDashboardDataSerializer

class AdLoadView(APIView):
    permission_classes = [AllowAny] 
    @extend_schema(
        parameters=[
            OpenApiParameter(name='adsize', required=True, type=str, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='location', required=True, type=str, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='partner', required=False, type=int, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='users', required=False, type=str, location=OpenApiParameter.QUERY),

        ],
        responses={
            200: OpenApiResponse(response=AdsViewHistorySerializer),
            400: OpenApiResponse(response={'error': 'Ad size and Ad Location is required'}),
            404: OpenApiResponse(response={'error': 'Ad not found'}),
        }
    )
    def get(self, request):


        adsize = request.GET.get('adsize', None)
        location = request.GET.get('location', None)
        partner = request.GET.get('partner', None)
        users = request.GET.get('users', None)
        if adsize and location:
            ad_qs = Adsmodel.objects.filter(adSize=adsize, location=location, is_active=True)
            if ad_qs.exists():

                # pick a random ad
                ad = ad_qs.order_by('?').first()
                ad_serializer = AdsmodelSerializer(ad)
                ad_view_history = None
                if partner:
                    partner = int(partner)
                    partner_obj = PartnerProfile.objects.get(id=partner)
                    
                    ad_view_history, created = AdsViewHistory.objects.get_or_create(ads=ad,partner=partner_obj)
                    ad_view_history.partner = partner_obj
                else:
                    ad_view_history, created = AdsViewHistory.objects.get_or_create(ads=ad, partner__isnull=True)
                ad_view_history.count += 1
                if users:
                    user_obj, _ = Adusers.objects.get_or_create(device_id=users)
                    if user_obj not in ad_view_history.users.all():
                        ad_view_history.users.add(user_obj)
                ad_view_history.save()
                return Response(ad_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Ad size and Ad Location is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            
class GetPartnerDashboardData(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @extend_schema(
        responses={
            200: OpenApiResponse(response=PartnerDashboardDataSerializer),
            403: OpenApiResponse(response={'error': 'You are not authorized to access this resource'}),
        }
    )
    def get(self, request):
        if not request.user.groups.filter(name='partner').exists():
            return Response({'error': 'You are not authorized to access this resource'}, status=status.HTTP_403_FORBIDDEN)
        # Get all AdsViewHistory for all partner profiles of this user
        ads_view_histories = AdsViewHistory.objects.filter(partner__user__id=request.user.id)
        serializer = PartnerDashboardDataSerializer(ads_view_histories)
        return Response(serializer.data, status=status.HTTP_200_OK)