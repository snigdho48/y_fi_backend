from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from api.models import ReleaseApp
import os

class ReleaseAppViewSet(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        apps = ReleaseApp.objects.all().order_by('-created_at').first()

        if not apps:
            return Response({'error': 'No apps found'}, status=status.HTTP_404_NOT_FOUND)

        apps.count += 1
        apps.save()

        file_path = apps.app.path
        if not os.path.exists(file_path):
            return Response({'error': 'APK file not found'}, status=status.HTTP_404_NOT_FOUND)

        # Return the APK file URL (adjust URL if needed based on your media file serving configuration)
        # get server name from request
        server_name = request.get_host()
        file_url = f'https://{server_name}{apps.app.url}'
        return Response({'url': file_url}, status=status.HTTP_200_OK)
