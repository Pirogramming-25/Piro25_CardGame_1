from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import JsonResponse

User = get_user_model()


def ranking_view(request):
    users = User.objects.all().order_by('-score')[:5]
    return render(request, 'ranking.html', {'users': users})


def ranking_data(request):
    """실시간 갱신용 JSON API. 프론트에서 주기적으로 fetch해서 화면을 다시 그림."""
    users = User.objects.all().order_by('-score')[:5]
    data = [
        {
            'rank': i + 1,
            'username': u.username,
            'score': u.score,
        }
        for i, u in enumerate(users)
    ]
    return JsonResponse({'users': data})