from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import ListAPIView

from apprest.serializers.facility import CalipsoFacilitySerializer
from apprest.services.facility import CalipsoFacilityServices

service = CalipsoFacilityServices()


class GetAllFacilities(ListAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = CalipsoFacilitySerializer
    pagination_class = None

    def get_queryset(self):
        return service.get_all_facilities()

    def dispatch(self, *args, **kwargs):
        return super(GetAllFacilities, self).dispatch(*args, **kwargs)
