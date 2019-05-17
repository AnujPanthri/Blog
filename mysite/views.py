from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from .forms import UserLoginForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def home(request):
    return render(request, 'index.html')

def sign_up_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            return HttpResponseRedirect(reverse('login'))

    else:
        form = SignUpForm()
    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('blog:home'))
    else:
        form = UserLoginForm()
    context = {
        'form': form,
    }
    return render(request,'login.html', context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('blog:home'))