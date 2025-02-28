from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from api.models import ReleaseApp

class ReleaseAppViewSet(APIView):
    permission_classes = [AllowAny]  

    def get(self, request):
        apps = ReleaseApp.objects.all().order_by('-created_at').first()
        
        if not apps:
            return Response({'error': 'No apps found'}, status=status.HTTP_404_NOT_FOUND)

        apps.count += 1  
        apps.save()
        
        return Response({'url': apps.app.url}, status=status.HTTP_200_OK)
