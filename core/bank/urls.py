from django.urls import path
from . import views

urlpatterns = [
    path('transfer/', views.transfer_view, name='transfer_form'),
]