from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm




def home(request):
    context = {}
    return render(request, 'main/home.html', context)


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    context = {'form': form}
    return render(request, 'registration/sign_up.html', context)

# for more built-in views (e.g. localhost:8000/password_reset/):
# https://docs.djangoproject.com/en/4.0/topics/auth/default/#using-the-views-1