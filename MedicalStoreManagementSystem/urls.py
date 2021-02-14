from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from MedicalStoreApp import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from MedicalStoreApp.views import CompanyNameViewSet

router = routers.DefaultRouter()
router.register("company", views.CompanyViewSet, basename='company')
router.register("medicine", views.MedicineViewSet, basename='medicine')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/gettoken/', TokenObtainPairView.as_view(), name="gettoken"),
    path('api/rest_fresh_token/', TokenRefreshView.as_view(), name="refresh_token"),
    path('api/company_name/<str:name>', CompanyNameViewSet.as_view(), name="company_by_name"),
]
