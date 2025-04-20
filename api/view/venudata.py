from drf_spectacular.utils import extend_schema, OpenApiResponse,OpenApiExample,OpenApiParameter
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.serializer import PartnerProfileSerializer,CustomPartnerProfileSerializerRegister,VenudataViewSerializer
from api.models import PartnerProfile
import qrcode
import io,os
from django.http import FileResponse
from django.conf import settings
from PIL import Image
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string






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
        responses={200: OpenApiResponse(response=PartnerProfileSerializer),400: OpenApiResponse(response={
            "type": "object",
            "properties": {
                "error": {"type": "string"}
            }
        },
            examples=[
                OpenApiExample(
                    name="Venu Not Found",
                    value={"error": "Venu Not Found"},
                    response_only=True
                ),
                OpenApiExample(
                    name="Venu Code not found",
                    value={"error": "Venu Code is required"},
                    response_only=True
                )
            ]
        )
        }
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
    
class AddVenuWifiDataView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "ssid": {"type": "string"},
                    "password": {"type": "string"}
                }
            }
        },
        responses={
            200: OpenApiResponse(
                response=VenudataViewSerializer(many=True),
               
            ),
            400: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "detail": {"type": "string"}
                    }
                },
                examples=[
                    OpenApiExample(
                        name="SSID or password not found",
                        value={"detail": "SSID and password are required."},
                        response_only=True
                    ),
                    OpenApiExample(
                        name="Invalid credentials",
                        value={"detail": "Unauthorized"},
                        response_only=True
                    )
                ]
            )
        }
    )
    def post(self, request):
        
        user = request.user
        group = user.groups.first()
        if group.name != 'partner':
                return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        partner = PartnerProfile.objects.filter(user=user).first()
        if not partner:
            return Response({"error": "Partner not found"}, status=status.HTTP_400_BAD_REQUEST)
        venu_routers = PartnerProfile.objects.filter(user=user)
        venu_name = partner.venue_name
        address = partner.address   
        phone_number = partner.phone_number
        
        request.data['venue_name'] = venu_name
        request.data['address'] = address
        request.data['phone_number'] = phone_number
        request.data['user'] = user.id
        request.data['code'] = genrate_Unique_code(venu_name=venu_name,wifi_routers_length=len(venu_routers)+1)
        
        
        serializer = CustomPartnerProfileSerializerRegister(data=request.data)
        if serializer.is_valid():
            serializer.save()
            all_wifi_routers = PartnerProfile.objects.filter(user=user)
            data= all_wifi_routers.exclude(ssid=None).exclude(password=None).exclude(code=None).exclude(ssid='').exclude(password='').exclude(code='')
            serializer_data = VenudataViewSerializer(data, many=True)
            qrcode = qrcode_generator(code=serializer.data['code'])
            if qrcode:
                send_qr_code_email(
                    partner=partner,
                    code=serializer.data['code'],
                   
                )
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteVenueDataView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "code": {"type": "string"}
                }
            }
        },
        responses={
            200: OpenApiResponse(
                response=VenudataViewSerializer(many=True),
               
            ),
            400: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "detail": {"type": "string"}
                    }
                },
                examples=[
                    OpenApiExample(
                        name="Code not found",
                        value={"detail": "Code is required."},
                        response_only=True
                    ),
                    OpenApiExample(
                        name="Invalid credentials",
                        value={"detail": "Unauthorized"},
                        response_only=True
                    ),
                    OpenApiExample(
                        name="Venu not found",
                        value={"detail": "Venue not found"},
                        response_only=True
                    )
                ]
            )
        }
    )
    def post(self, request):
        user = request.user
        group = user.groups.first()
        if group.name != 'partner':
                return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        code = request.data.get('code')
        if not code:
            return Response({"error": "Code is required"}, status=status.HTTP_400_BAD_REQUEST)
        partner = PartnerProfile.objects.filter(code=code).first()
        if not partner:
            return Response({"error": "Venue not found"}, status=status.HTTP_400_BAD_REQUEST)
        partner.delete()
        all_wifi_routers = PartnerProfile.objects.filter(user=user)
        data= all_wifi_routers.exclude(ssid=None).exclude(password=None).exclude(code=None).exclude(ssid='').exclude(password='').exclude(code='')
        serializer_data = VenudataViewSerializer(data, many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)
    
class UpdateVenueDataView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "code": {"type": "string"},
                    "ssid": {"type": "string"},
                    "password": {"type": "string"},
                    
                }
            }
        },
        responses={
            200: OpenApiResponse(
                response=VenudataViewSerializer(many=True),
               
            ),
            400: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "detail": {"type": "string"}
                    }
                },
                examples=[
                 
                    OpenApiExample(
                        name="Invalid credentials",
                        value={"detail": "Unauthorized"},
                        response_only=True
                    ),
                    OpenApiExample(
                        name="No Venue Found",
                        value={"detail": "Venue not found"},
                        response_only=True
                    ),
                    OpenApiExample(
                        name="SSID not found",
                        value={"detail": "SSID is required"},
                        response_only=True
                    ),
                    OpenApiExample(
                        name="Password not found",
                        value={"detail": "Password is required"},
                        response_only=True
                    ),
                    OpenApiExample(
                        name="Code not found",
                        value={"detail": "Code is required"},
                        response_only=True
                    )
                ]
            )
            
        }
    )
    def post(self, request):
        user = request.user
        group = user.groups.first()
        if group.name != 'partner':
                return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        code = request.data.get('code')
        if not code:
            return Response({"error": "Code is required"}, status=status.HTTP_400_BAD_REQUEST)
        ssid = request.data.get('ssid')
        if not ssid:
            return Response({"error": "SSID is required"}, status=status.HTTP_400_BAD_REQUEST)
        password = request.data.get('password')
        if not password:
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)
        partner = PartnerProfile.objects.filter(code=code).first()
        if not partner:
            return Response({"error": "Venue not found"}, status=status.HTTP_400_BAD_REQUEST)
        partner.ssid = ssid
        partner.password = password
        partner.save()
        all_wifi_routers = PartnerProfile.objects.filter(user=user)
        data= all_wifi_routers.exclude(ssid=None).exclude(password=None).exclude(code=None).exclude(ssid='').exclude(password='').exclude(code='')
        serializer_data = VenudataViewSerializer(data, many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)
    
class GetAllVenueDataView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=VenudataViewSerializer(many=True),
               
            ),
            400: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "detail": {"type": "string"}
                    }
                },
                examples=[
                    OpenApiExample(
                        name="Invalid credentials",
                        value={"detail": "Unauthorized"},
                        response_only=True
                    )
                ]
            )
        }
    )
    def get(self, request):
        user = request.user
        group = user.groups.first()
        if group.name != 'partner':
                return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        all_wifi_routers = PartnerProfile.objects.filter(user=user)
        data= all_wifi_routers.exclude(ssid=None).exclude(password=None).exclude(code=None).exclude(ssid='').exclude(password='').exclude(code='')
        
        serializer_data = VenudataViewSerializer(data, many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)


def genrate_Unique_code(venu_name,wifi_routers_length):
    venu_name = venu_name.replace(' ','_')
    code = venu_name.upper() + str(wifi_routers_length)
    return code
    
    
class GetQrCodeApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @extend_schema(
        parameters=[
            OpenApiParameter(name="code", required=True, type=str, location=OpenApiParameter.QUERY)
        ],
        responses={
            200: OpenApiResponse(description="QR Code Image"),
            400: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "error": {"type": "string"}
                    }
                },
                examples=[
                    OpenApiExample(
                        name="Code not found",
                        value={"error": "Code is required."},
                        response_only=True
                    )
                ]
            ),
            401: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "error": {"type": "string"}
                    }
                },
                examples=[
                    OpenApiExample(
                        name="Unauthorized",
                        value={"error": "Unauthorized"},
                        response_only=True
                    )
                ]
            )
        }
    )
    def get(self, request):
        user = request.user
        group = user.groups.first()
        if group.name != 'partner':
                return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        code = request.query_params.get('code')
        if not code:
            return Response({"error": "Code is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        partner = PartnerProfile.objects.filter(code=code,user=user)
        if not partner.exists():
            return Response({"error": "Venue not found"}, status=status.HTTP_400_BAD_REQUEST)
        partner = partner.first()
        qrlink = qrcode_generator(code)
        return FileResponse(qrlink, content_type='image/jpeg', filename=f'{partner.venue_name}_${partner.code}_qr.jpg')

    
def qrcode_generator(code):
    data = f"https://app.freeyfi.com/?code={code}"  # also fixed the incorrect `${code}`
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # ✅ Properly load logo from media path
    logo_path = os.path.join(settings.MEDIA_ROOT, "logo.png")
    if os.path.exists(logo_path):
        logo_img = Image.open(logo_path).convert("RGBA")
        qr_width, qr_height = img.size

        # Scale the logo size (20% of QR code)
        logo_size = int(qr_width * 0.15)
        logo_img = logo_img.resize((logo_size, logo_size), Image.LANCZOS)
        pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        img.paste(logo_img, pos, mask=logo_img)

    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG", quality=100)
    img_bytes.seek(0)
    return img_bytes




def send_qr_code_email(partner, code):
    try:
        print("Sending email...")

        # Generate the QR code image
        qrcode_image = qrcode_generator(code)

        subject = "Your FreeYFi QR Code"
        from_email = settings.EMAIL_HOST_USER
        to_email = [partner.user.email]

        # Create HTML content (inline)
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; color: #333; }}
                .container {{ padding: 20px; }}
                .header {{ font-size: 20px; font-weight: bold; }}
                .qr-section {{ margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">Hello {partner.user.first_name},</div>
                <p>Here is your QR code for <strong>{partner.venue_name}</strong>.</p>
                <p><strong>WIFI Code:</strong> {code}</p>
                <p>The QR code is attached to this email.</p>
                <br>
                <p>Thanks,<br>FreeYFi Team</p>
            </div>
        </body>
        </html>
        """

        # Create the email
        email = EmailMultiAlternatives(
          subject,
            '',
            from_email,
            to_email
        )
        print(email.from_email)
        print(email.to)

        # Attach HTML content
        email.attach_alternative(html_content, "text/html")

        # Attach the QR code image
        email.attach(f"{code}_qr.jpg", qrcode_image.read(), "image/jpeg")
        print("About to send email")

        # Send the email
        email.send(fail_silently=True)
        print("Email sent successfully.")

    except Exception as e:
        print(f"Error sending email: {e}")