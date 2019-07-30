from django.conf.urls import url, include

from .views import (
    UserLoginAPIView,
)

app_name = 'accounts'
urlpatterns = [
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
]

