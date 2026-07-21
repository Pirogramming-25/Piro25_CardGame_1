from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings


class AttackRequest(models.Model):
    STATUS_CHOICES = [
        ("waiting", "Waiting"),
        ("completed", "Completed"),
    ]

    attacker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_attacks"
    )

    defender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_attacks"
    )

    attacker_card = models.PositiveSmallIntegerField()
    
    defender_card = models.PositiveSmallIntegerField(null=True, blank=True) #jhm: 방어자 카드
    # jhm
    winner = models.ForeignKey(   # 숭자를 User 한명으로 가리킴
      settings.AUTH_USER_MODEL,
      null=True, blank=True,
      on_delete=models.SET_NULL,  # 승자유저 계정 삭제되어도 상대에게는 이력 남음
      related_name='won_attacks'  # 추후 이긴 경기 조회할 때 사용가능
    )  
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="waiting"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attacker} → {self.defender}"