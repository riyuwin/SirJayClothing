from django.shortcuts import render
from rest_framework.authtoken.models import Token 
 
     
#@login_required
def LaunchIndex(request):
    user_id = request.user.id if request.user.is_authenticated else None
    username = request.user.username if request.user.is_authenticated else None
    user_token = None
    if request.user.is_authenticated:
        try:
            user_token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            # Handle the case where the token doesn't exist for the user
            pass
    
    return render(request, "index.html", {'logged_in': request.user.is_authenticated, 'user_id': user_id, 'username': username, 'user_token': user_token})
 

def LaunchAppointmentForm(request):
    return render(request, 'AppointmentForm.html')

def SuccessPage(request):
    return render(request, 'Success.html')
