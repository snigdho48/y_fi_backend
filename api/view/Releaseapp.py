from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import ReleaseApp
from api.serializer import ReleaseAppSerializer

class ReleaseAppViewSet(APIView):
    
    def get(self, request):
        apps = ReleaseApp.objects.all().order_by('-created_at').first()
        apps.c
        return Response({'url':apps.app}, status=status.HTTP_200_OK)
