from django.urls import path
from . import views

urlpatterns = [
    path("attack-page/", views.attack_page, name="attack_page"),
    path("cards/", views.get_random_cards, name="get_random_cards"),
    path("attack/", views.attack_request, name="attack_request"),
]