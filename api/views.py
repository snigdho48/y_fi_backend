from .view.auth import MyTokenObtainPairView, LogoutAPIView, PartnerTokenObtainPairView, PartnerRegistrationView
from .view.venudata import VenueDataView, AddVenuWifiDataView,DeleteVenueDataView,UpdateVenueDataView,GetAllVenueDataView,GetQrCodeApiView,PassVenuInfoApiView
from .view.datacollect import DataCollectView
from .view.Releaseapp import ReleaseAppViewSet,PartnerAppViewSet
from .view.partnerDashbaord import PartnerDashboardView
from .view.adload import AdLoadView,GetPartnerDashboardData

# Create your views here.
