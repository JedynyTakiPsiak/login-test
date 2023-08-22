from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
import json
  
  
#################### index#######################################
def index(request):
    return render(request, 'user/index.html')
    
################ login forms###################################################
def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_data = get_user_data_from_json(username)

        if user_data is not None:
            if user_data.get("blocked", False):
                messages.info(request, 'Konto zablokowane.')
            elif user_data.get("is_2fa_enabled", False):
                # Użytkownik ma włączoną autoryzację dwuskładnikową (2FA)
                # Tutaj możesz dodać kod do obsługi 2FA, jeśli jest wymagane.
                pass
            elif user_data.get("password") == password:
                messages.success(request, f'Welcome {username}!')
                return redirect('index')
            else:
                messages.info(request, 'Nieprawidłowa nazwa użytkownika lub hasło.')
        else:
            messages.info(request, 'Nieprawidłowa nazwa użytkownika lub hasło.')

    form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

def get_user_data_from_json(username):
    # Odczytaj dane z pliku JSON
    with open('../../login.json', 'r') as json_file:
        data = json.load(json_file)
        users = data.get("users", [])
        for user in users:
            if user.get("username") == username:
                return user
        return None