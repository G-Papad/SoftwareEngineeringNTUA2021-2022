from django.urls import path
from . import views

# URLConfiguration

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_from_xslx, name='upload'),
    path('transportation/', views.transportation, name='transportation')
]
