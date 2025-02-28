from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from api.models import ReleaseApp
import base64

def encode_apk_to_base64(file_path):
    with open(file_path, "rb") as apk_file:
        encoded_string = base64.b64encode(apk_file.read()).decode('utf-8')
    return encoded_string


class ReleaseAppViewSet(APIView):
    permission_classes = [AllowAny]  

    def get(self, request):
        apps = ReleaseApp.objects.all().order_by('-created_at').first()
        
        if not apps:
            return Response({'error': 'No apps found'}, status=status.HTTP_404_NOT_FOUND)

        apps.count += 1  
        apps.save()
        apk = encode_apk_to_base64('/home/ubuntu/projects/y_fi_backend'+apps.app.path)
        
        return Response({'base64': apk}, status=status.HTTP_200_OK)
