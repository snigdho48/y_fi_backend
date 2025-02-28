from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import ReleaseApp

class ReleaseAppViewSet(APIView):
    
    def get(self, request):
        apps = ReleaseApp.objects.all().order_by('-created_at').first()
        apps.count += 1
        apps.save()
        return Response({'url':apps.app}, status=status.HTTP_200_OK)
