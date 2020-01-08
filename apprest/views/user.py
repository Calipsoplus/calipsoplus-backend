from django.http import HttpResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status, pagination, filters

from apprest.serializers.user import CalipsoUserSerializer
from apprest.services.user import CalipsoUserServices
from apprest.utils.request import JSONResponse
from calipsoplus.settings_calipso import PAGE_SIZE_USERS

from django_filters.rest_framework import DjangoFilterBackend


class UsersPagination(pagination.PageNumberPagination):
    page_size = PAGE_SIZE_USERS
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data,
            'page_size': self.page_size,
        })


class GetUser(APIView):
    """
    Return given user
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, *args, **kwargs):
        service = CalipsoUserServices()
        username = self.kwargs.get('username')
        print(self.kwargs.get('username'))
        print(username)
        user = service.get_user(username=username)
        serializer_class = CalipsoUserSerializer(user)
        return Response(serializer_class.data)


class GetAllUsers(ListAPIView):
    """
       get:
       Return all users
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    pagination_class = UsersPagination
    serializer_class = CalipsoUserSerializer
    filter_backends = (filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend,)
    ordering_fields = ('id', 'user__username')
    search_fields = ('id', 'user__username')
    ordering = ('id',)

    def get_queryset(self, *args, **kwargs):
        service = CalipsoUserServices()
        users = service.get_all_users()
        return users


class UserAdmin(APIView):
    """
        Return given user
        """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, *args, **kwargs):
        service = CalipsoUserServices()
        # User making the request
        authenticated_user = self.request.user.username
        # User to be checked
        requested_username = self.kwargs.get('username')

        # Make sure current user is an admin
        if service.is_admin(authenticated_user):
            requested_username_is_admin = service.is_admin(requested_username)
            if requested_username_is_admin:
                return JSONResponse({'is_admin': True})
            return JSONResponse({'is_admin': False})
        return HttpResponse(status=403)

    def post(self, *args, **kwargs):
        service = CalipsoUserServices()
        authenticated_user = self.request.user.username
        requested_username = self.kwargs.get('username')

        if service.is_admin(authenticated_user):
            service.make_user_admin(requested_username)
            return HttpResponse(status=200)
        return HttpResponse(status=403)