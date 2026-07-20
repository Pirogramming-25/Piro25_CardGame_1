from django.shortcuts import render, get_object_or_404

# Create your views here.

import json
import random

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import AttackRequest
from .score_logic import finish_game
from accounts.models import User

def attack_page(request):
    users = User.objects.exclude(pk=request.user.pk)

    return render(request, "attack.html", {
        "users": users,
    })

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

@login_required
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

# jhm: 다른 유저에게 요청받은 대결 목록 조회
@login_required
def received_requests(request):
  requests = AttackRequest.objects.filter(
    defender = request.user,
    status="waiting",
  )
  
  return render(request, "received_requests.html", {
    "requests": requests,
  })
  
# jhm: 반격 -> 점수계산로직 실행
@login_required
def counter_attack(request, attack_id):
  if request.method != "POST":
    return JsonResponse(
      {"error": "POST 요청만 가능합니다."},
      status=405
    )
  
  attack = get_object_or_404(AttackRequest, pk=attack_id)
  
  if attack.defender != request.user:
    return JsonResponse({"error": "권한이 없습니다."}, status=403)
  
  if attack.status != "waiting":
    return JsonResponse({"error": "이미 처리된 요청입니다."}, status=400)
  
  data = json.loads(request.body)
  attack.defender_card = data.get("defender_card")
  attack.save()
  
  finish_game(attack)
  
  return JsonResponse({
    "message": "반격 완료",
    "winner" : attack.winner.username if attack.winner else None,
  })

# jhm: 요청했던 공격 삭제
@login_required
def cancel_attack(request, attack_id):
  if request.method != "POST":
    return JsonResponse(
      {"error": "POST 요청만 가능합니다."},
      status=405
    )
  
  attack = get_object_or_404(AttackRequest, pk=attack_id)
  
  if attack.attacker != request.user:
    return JsonResponse({"error": "권한이 없습니다."}, status=403)
  
  if attack.status != "waiting":
    return JsonResponse({"error": "이미 처리된 요청입니다."}, status=400)

  attack.delete()
  
  return JsonResponse({"message": "공격 신청이 취소되었습니다."})