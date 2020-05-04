from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from authentication.forms import SignUpForm
from django.contrib.auth.models import User
# Create your views here.


def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return redirect('login')            
    else:
        form = AuthenticationForm()
    if(request.user.is_authenticated):
        user = User.objects.get(username = request.user.username)
        context = {
        'form': form,
        'user': user,
        }
    else:
        context = {
        'form': form,
        }

    return render(request = request,template_name = "registration/login.html",context=context)

def logoutView(request):
    logout(request)
    return redirect('login')

def registerView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()

    if(request.user.is_authenticated):
        user = User.objects.get(username = request.user.username)
        context = {
        'form': form,
        'user': user,
        }
    else:
        context = {
        'form': form,
        }

    return render(request, 'register.html', context=context)