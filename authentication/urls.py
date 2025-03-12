from django.urls import path
from .views import RegisterView, VerifyRegisterView
from .views import user_details

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("register/verify/", VerifyRegisterView.as_view(), name="register-verify"),
]


urlpatterns += [
    path('api/me/', user_details, name='user-details'),
]

from .views import logout_view

urlpatterns += [
    path('api/logout/', logout_view, name='logout'),
]

from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Authentication API",
        default_version='v1',
        description="API for user authentication",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]