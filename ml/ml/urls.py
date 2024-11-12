from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from ml_system.views import ml_router

api = NinjaAPI()
api.add_router("/ml/",  ml_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
