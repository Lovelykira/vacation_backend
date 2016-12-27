from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import DjangoFilterBackend
from rest_framework.fields import CurrentUserDefault

from .models import VacationRequest

from .serializers import UserSerializer, VacationRequestSerializer


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# class UserPermissionsObj(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         print('user', request.user)
#         print('user.is_staff', request.user.is_staff)
#         print('obj == request.user', obj == request.user)
#         if request.user.is_staff:
#             return True
#
#         return obj == request.user


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    model = User
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication,)

    def list(self, request, *args, **kwargs):
        queryset = User.objects.filter(username=self.request.user).first()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class VacationRequestViewSet(viewsets.ModelViewSet):
    serializer_class = VacationRequestSerializer
    model = VacationRequest
    queryset = VacationRequest.objects.all()
    # pagination_class = PageNumberPagination
    authentication_classes = (TokenAuthentication,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user', )
    # permission_classes = (UserPermissionsObj,)

    # def list(self, request, *args, **kwargs):
    #     pageSize = request.GET.get('pageSize', 5)
        # pagination.PageNumberPagination.page_size = 100
        # self.pagination_class.max_page_size = pageSize
        # print(pageSize)

        # return super(VacationRequestViewSet, self).list(request, *args, **kwargs)

    def get_queryset(self):
        # if self.request.user.is_superuser:
        #     return VacationRequest.objects.all()
        return VacationRequest.objects.filter(user=self.request.user)

    # def create(self, request, *args, **kwargs):
    #     print('asd')
    #     print(request.__dict__)
    #     print(request.headers)

    # @property
    # def user(self):
    #     if not hasattr(self, '_user'):
    #         self._authenticator, self._user, self._auth = self._authenticate()
    #         if not isinstance(self._user, User) and self.request.auth is not None:
    #             token = Token.objects.get(key=self.request.auth)
    #         self._user = token.user
    #
    #     return self._user


class CurrentUserView(APIView):
    def post(self, request):
        username = request.data.get('username', '')
        user = User.objects.get(username=username)
        return Response(str(user.id))
