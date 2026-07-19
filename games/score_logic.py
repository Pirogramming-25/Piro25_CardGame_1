# 점수 계산 함수

import random

DRAW = "DRAW"

# jhm : games/models.py랑 필드 이름 맞춤
# attack_card -> attacker_card
# defend_card -> defender_card
# "FINISHED" -> "completed"
def determine_winner(game):
    if game.attacker_card == game.defender_card:    #무승부
        game.higher_wins = None
        game.winner = None
        return None, None, None, None  # winner, loser, winner_card, loser_card

    higher_wins = random.choice([True, False]) #게임 기준 설정
    game.higher_wins = higher_wins

    if game.attacker_card > game.defender_card:
        higher_player, higher_card = game.attacker, game.attacker_card
        lower_player, lower_card = game.defender, game.defender_card
  
    else:
        higher_player, higher_card = game.defender, game.defender_card
  
        lower_player, lower_card = game.attacker, game.attacker_card

    if higher_wins:
        winner, winner_card = higher_player, higher_card
        loser, loser_card = lower_player, lower_card
    else:
        winner, winner_card = lower_player, lower_card
        loser, loser_card = higher_player, higher_card

    game.winner = winner
    return winner, loser, winner_card, loser_card


def apply_score(winner, loser, winner_card, loser_card):
    if winner is None: #무승부
        return

    winner.score += winner_card
    loser.score -= loser_card
    winner.save()
    loser.save()


def finish_game(game):
    winner, loser, winner_card, loser_card = determine_winner(game)
    apply_score(winner, loser, winner_card, loser_card)
    game.status = "completed"
    game.save()