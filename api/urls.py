from django.conf.urls import url, include
from rest_framework.authtoken import views
from rest_framework import routers

from .views import UserViewSet, VacationRequestViewSet, CurrentUserView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, base_name='users')
router.register(r'vacations', VacationRequestViewSet, base_name='vacations')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^token-auth/$', views.obtain_auth_token),
    url(r'^current-user/', CurrentUserView.as_view()),
]
