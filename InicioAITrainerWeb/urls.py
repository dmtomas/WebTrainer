from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.getout, name='out'),
    path('trainer/', views.trainer, name='AI'),
    path('payment/', views.payment, name='pay'),
    path('update/', views.FueraTrucho, name='update'),
    path('month/', views.month),
    path('curso/', views.curso, name='curso')
]