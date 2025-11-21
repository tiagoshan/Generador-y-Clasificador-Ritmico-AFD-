# ritmos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('generate/<str:genre>/<int:measures>/', views.GenerateRhythmAPI.as_view(), name='generate'),

    path('classify/', views.ClassifyRhythmAPI.as_view(), name='classify'),
]