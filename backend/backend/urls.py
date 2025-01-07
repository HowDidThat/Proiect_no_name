from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from authentication.views import auth_router
from quiz.views import quiz_router

from quiz.views import medical_router

api = NinjaAPI()
api.add_router("/auth/", auth_router)
api.add_router("/quiz/", quiz_router)
api.add_router("/medical/", medical_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
