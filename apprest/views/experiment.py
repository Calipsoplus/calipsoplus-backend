from rest_framework import pagination, filters
from rest_framework.exceptions import PermissionDenied

from rest_framework.generics import ListAPIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apprest.serializers.experiment import CalipsoExperimentSerializer
from apprest.services.experiment import CalipsoExperimentsServices
from calipsoplus.settings_calipso import PAGE_SIZE_EXPERIMENTS

service = CalipsoExperimentsServices()


class ExperimentsPagination(pagination.PageNumberPagination):
    page_size = PAGE_SIZE_EXPERIMENTS
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data,
            'page_size': self.page_size,
        })


class GetExperimentsByUserName(ListAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = CalipsoExperimentSerializer
    pagination_class = ExperimentsPagination
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    ordering_fields = '__all__'
    ordering = ('serial_number',)
    search_fields = ('subject', 'body', 'serial_number', 'beam_line',)

    def get_queryset(self):
        username = self.kwargs.get('username')
        if username == self.request.user.username:
            return service.get_user_experiments(self.kwargs.get('username'))
        else:
            raise PermissionDenied

