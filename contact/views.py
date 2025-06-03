from django.shortcuts import render
from accounts.models import User

def contact_view(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None
    return render(request, 'contact/contact.html', {'user': user})
