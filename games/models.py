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

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="waiting"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attacker} → {self.defender}"