from django.contrib import admin
from django.urls import include,path

urlpatterns = [
    path("", include("control.urls")),  # add this
    path('admin/', admin.site.urls),
]