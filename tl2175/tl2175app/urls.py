from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

# URLConfiguration

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_from_xslx, name='upload'),
<<<<<<< HEAD
    path('providers/', views.Providers_list.as_view(), name='providers'),
    path('providers/<int:pk>/', views.Providers_Details.as_view()),
    path('PassesPerStation/<str:pk>/<str:df>/<str:dt>/',
         views.PassesPerStation.as_view()),
    # path('transportation/', views.transportation, name='transportation')
=======
    path('transportation/', views.transportation, name='transportation')
>>>>>>> 6de50ba084f1a69f2f8cd096e7084665a661ccfc
]

urlpatterns = format_suffix_patterns(urlpatterns)
