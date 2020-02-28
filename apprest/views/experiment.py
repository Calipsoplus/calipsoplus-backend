import logging

from rest_framework import pagination, filters, status

from rest_framework.exceptions import PermissionDenied

from rest_framework.generics import ListAPIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.core.paginator import Paginator

from apprest.plugins.icat.helpers.complex_encoder import JsonResponse
from apprest.serializers.experiment import CalipsoExperimentSerializer
from apprest.services.experiment import CalipsoExperimentsServices
from apprest.utils.request import JSONResponse
from apprest.plugins.icat.services.ICAT import ICATService


from calipsoplus.settings_calipso import PAGE_SIZE_EXPERIMENTS, DYNAMIC_EXPERIMENTS_DATA_RETRIEVAL,\
    ENABLE_ICAT_DATA_RETRIEVAL

from django_filters.rest_framework import DjangoFilterBackend

service = CalipsoExperimentsServices()

logger = logging.getLogger(__name__)


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
    filter_backends = (filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend,)
    ordering_fields = ('subject', 'body', 'proposal_id', 'beam_line', 'calipsouserexperiment__favorite',)
    ordering = ('proposal_id',)
    search_fields = ('subject', 'body', 'proposal_id', 'beam_line', 'calipsouserexperiment__favorite',)
    filter_fields = ('calipsouserexperiment__favorite',)

    def get_queryset(self):
        username = self.kwargs.get('username')
        if username == self.request.user.username:
            logger.debug('experiments get from db')
            experiments_list = service.get_user_experiments(username)
            return experiments_list
        else:
            raise PermissionDenied

    def get(self, request, *args, **kwargs):
        if DYNAMIC_EXPERIMENTS_DATA_RETRIEVAL == 0:
            return super(GetExperimentsByUserName, self).get(self, request, *args, **kwargs)

        elif ENABLE_ICAT_DATA_RETRIEVAL:
            icat_service = ICATService()
            experiments_list = icat_service.get_embargo_data()
            paginator = Paginator(experiments_list, PAGE_SIZE_EXPERIMENTS) # PAGE_SIZE_EXPERIMENTS is results per page
            results = paginator.get_page(request.GET.get('page'))
            data = {'page_size': PAGE_SIZE_EXPERIMENTS, 'results': results.object_list, 'count': len(experiments_list),
                    'next': '', 'previous': ''}
            return JsonResponse(data, status=status.HTTP_200_OK)

        else:
            username = self.kwargs.get('username')
            if username == self.request.user.username:

                must_be_favorite = request.GET.get('calipsouserexperiment__favorite')
                logger.debug('must_be_favorite=%s' % must_be_favorite)

                query = {"page_size": PAGE_SIZE_EXPERIMENTS,
                         "page": request.GET.get('page'),
                         "ordering": request.GET.get('ordering'),
                         "search": request.GET.get('search'),
                         "calipsouserexperiment__favorite": request.GET.get('calipsouserexperiment__favorite')}

                experiments_list = service.get_external_user_experiments(username, query)
                experiments_list = service.update_favorite_from_external_experiments(username, experiments_list)

                experiments_list['page_size'] = PAGE_SIZE_EXPERIMENTS

                if must_be_favorite is None:
                    return JSONResponse(experiments_list, status=status.HTTP_200_OK)
                else:
                    return super(GetExperimentsByUserName, self).get(self, request, *args, **kwargs)
            else:
                raise PermissionDenied



