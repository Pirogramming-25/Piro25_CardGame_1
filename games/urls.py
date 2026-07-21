from django.urls import path
from . import views

urlpatterns = [
    path("attack-page/", views.attack_page, name="attack_page"),
    path("cards/", views.get_random_cards, name="get_random_cards"),
    path("attack/", views.attack_request, name="attack_request"),
    path("game_list/", views.game_list, name="game_list"),
    path("counter/<int:attack_id>/", views.counter_attack, name="counter_attack"),
    path("cancel/<int:attack_id>/", views.cancel_attack, name="cancel_attack"),
]