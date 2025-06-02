from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import translation
from accounts.models import User
from django.utils.timezone import now

def projects(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None
    return render(request, 'projects/projects.html', {'user': user})