from .models import Profile

def check_user(request):
    if not request.session.session_key:
        request.session.save()
    
    if request.session.get('current_user', False):
        current_user = int(request.session['current_user'])
    else:
        new_user = Profile(name=request.session.session_key)
        new_user.save()
        current_user = new_user.id
        request.session['current_user'] = current_user
    return current_user