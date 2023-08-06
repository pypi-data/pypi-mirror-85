from django.conf import settings
from django.urls import path, include
from django.views.generic.base import RedirectView


urlpatterns = [
    path('oauth/', include('social_django.urls', namespace='social')),
    path('admin/login/', RedirectView.as_view(url=settings.LOGIN_URL)),
    path('admin/logout/', RedirectView.as_view(url=settings.LOGOUT_URL)),
]
