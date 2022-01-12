from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

# URLConfiguration

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_from_xslx, name='upload'),
    path('providers/', views.Providers_list.as_view(), name='providers'),
    path('providers/<int:pk>/', views.Providers_Details.as_view()),
    path('PassesPerStation/<str:pk>/<str:df>/<str:dt>/',
         views.PassesPerStation.as_view()),
    path('PassesCost/<str:op1>/<str:op2>/<str:df>/<str:dt>/',
         views.PassesCost.as_view()),
    path('ChargesBy/<str:op1>/<str:df>/<str:dt>/',
         views.ChargesBy.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
