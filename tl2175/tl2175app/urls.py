from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include, re_path
# URLConfiguration

urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('upload/', views.upload_from_xslx, name='upload'),
    path('PassesUpdate/', views.passupdt, name='passupdt'),
    path('PassesAnalysis', views.transauth, name='transauth'),
    #path('PassesUpdate/', views.PassesUpdate.as_view()),
    path('PassesPerStation/<str:pk>/<str:df>/<str:dt>/',
         views.PassesPerStation.as_view()),
    path('PassesAnalysis/<str:op1_ID>/<str:op2_ID>/<str:df>/<str:dt>/',
         views.PassesAnalysis.as_view()),
    path('PassesCost/', views.passescost, name='passescost'),
    path('PassesCost/<str:op1>/<str:op2>/<str:df>/<str:dt>/',
         views.PassesCost.as_view()),
    path('ChargesBy/<str:op1>/<str:df>/<str:dt>/',
         views.ChargesBy.as_view()),
    path('admin/healthcheck', views.healthcheck.as_view()),
    path('admin/resetpasses', views.resetpasses.as_view()),
    path('admin/resetstations', views.resetstations.as_view()),
    path('admin/resetvehicles', views.resetvehicles.as_view()),
    path('info', views.info, name='info'),
    path('ConfigurePayments/<str:op1>/<str:op2>/<str:df>/<str:dt>/',
         views.configurePayments.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'csv'])
