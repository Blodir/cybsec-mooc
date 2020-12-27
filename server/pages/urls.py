from django.urls import path

from .views import homePageView, addView, deleteView

urlpatterns = [
    path('', homePageView, name='home'),
    path('add/', addView, name='add'),
    path('delete/', deleteView, name='delete'),
]
