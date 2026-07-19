from django.shortcuts import render

# Create your views here.

import json
import random

from django.http import JsonResponse

from .models import AttackRequest

def attack_page(request):
    return render(request, "attack.html")

def get_random_cards(request):
    if request.method != "GET":
        return JsonResponse(
            {"error": "GET 요청만 가능합니다."},
            status=405
        )

    cards = random.sample(range(1, 11), 5)

    return JsonResponse({
        "cards": cards
    })


def attack_request(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST 요청만 가능합니다."},
            status=405
        )

    data = json.loads(request.body)

    target_user = data.get("target_user")
    attacker_card = data.get("attacker_card")

    attack = AttackRequest.objects.create(
        attacker=request.user,
        defender_id=target_user,
        attacker_card=attacker_card,
    )

    return JsonResponse({
        "message": "공격 신청 완료",
        "attack_id": attack.id,
    })