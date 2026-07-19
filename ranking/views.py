from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import JsonResponse

User = get_user_model()


def _build_ranked_list(limit=5):
    """점수 내림차순 정렬 후, 동점자는 같은 순위를 부여하고
    다음 순위는 그만큼 건너뛰는 방식(1, 2, 2, 4 ...)으로 순위 리스트를 만든다."""
    users = list(User.objects.all().order_by('-score')[:limit])

    ranked = []
    rank = 0
    prev_score = None
    for i, u in enumerate(users):
        if u.score != prev_score:
            rank = i + 1
        ranked.append({'rank': rank, 'user': u})
        prev_score = u.score

    return ranked


def ranking_view(request):
    ranked_users = _build_ranked_list(limit=5)
    return render(request, 'ranking.html', {'ranked_users': ranked_users})


def ranking_data(request):
    """실시간 갱신용 JSON API. 프론트에서 주기적으로 fetch해서 화면을 다시 그림."""
    ranked_users = _build_ranked_list(limit=5)
    data = [
        {
            'rank': entry['rank'],
            'username': entry['user'].username,
            'score': entry['user'].score,
        }
        for entry in ranked_users
    ]
    return JsonResponse({'users': data})