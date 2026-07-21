from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.ranking_view, name='ranking'),
    path('data/', views.ranking_data, name='ranking_data'),
]