from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from api.serializer import ContactMessageSerializer


class ContactMessageView(APIView):
    """Public contact form for the marketing site (no auth)."""
    permission_classes = [AllowAny]
    authentication_classes = []

    @staticmethod
    def _client_ip(request):
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")

    @extend_schema(
        request=ContactMessageSerializer,
        responses={
            201: OpenApiResponse(description="Message stored."),
            400: OpenApiResponse(description="Validation error."),
        },
    )
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        ua = (request.META.get("HTTP_USER_AGENT") or "")[:512]
        serializer.save(
            user_agent=ua or None,
            source_ip=self._client_ip(request),
        )
        return Response(
            {"message": "Thank you. We will get back to you soon."},
            status=status.HTTP_201_CREATED,
        )
