from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model()

def ranking_view(request):
    users = User.objects.all().order_by('-score')
    return render(request, 'ranking.html', {'users': users})