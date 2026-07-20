from django.shortcuts import render, get_object_or_404

# Create your views here.

import json
import random

from django.db.models import Q
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

# jhm: 내가 받은/보낸 대결 요청 + 완료된 대결 이력 조회
@login_required
def game_list(request):
  received_requests = AttackRequest.objects.filter(
    defender=request.user,
    status="waiting",
  ).select_related("attacker")

  sent_requests = AttackRequest.objects.filter(
    attacker=request.user,
    status="waiting",
  ).select_related("defender")

  finished_requests = AttackRequest.objects.filter(
    Q(attacker=request.user) | Q(defender=request.user),
    status="completed",
  ).select_related("attacker", "defender", "winner").order_by("-created_at")

  finished_matches = [_build_match_detail(req, request.user) for req in finished_requests]

  return render(request, "game_list.html", {
    "received_requests": received_requests,
    "sent_requests": sent_requests,
    "finished_matches": finished_matches,
  })


# jhm: 대결 상세 모달용 데이터 (승리 기준 / 카드 / 점수 변동)
def _build_match_detail(req, viewer):
  is_draw = req.winner_id is None

  if is_draw:
    criteria_text = "무승부 (카드 숫자 동일)"
    attacker_change = 0
    defender_change = 0
  elif req.winner_id == req.attacker_id:
    attacker_change = req.attacker_card
    defender_change = -req.defender_card
    criteria_text = (
      "숫자가 높은 카드 승리" if req.attacker_card > req.defender_card
      else "숫자가 낮은 카드 승리"
    )
  else:
    attacker_change = -req.attacker_card
    defender_change = req.defender_card
    criteria_text = (
      "숫자가 높은 카드 승리" if req.defender_card > req.attacker_card
      else "숫자가 낮은 카드 승리"
    )

  if is_draw:
    my_result = "무승부"
  elif req.winner_id == viewer.id:
    my_result = "승리"
  else:
    my_result = "패배"

  return {
    "attacker": req.attacker.username,
    "defender": req.defender.username,
    "attacker_card": req.attacker_card,
    "defender_card": req.defender_card,
    "is_draw": is_draw,
    "winner": req.winner.username if req.winner else None,
    "criteria_text": criteria_text,
    "attacker_change": attacker_change,
    "defender_change": defender_change,
    "my_result": my_result,
  }
  
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