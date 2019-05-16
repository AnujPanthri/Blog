from django.shortcuts import render, HttpResponseRedirect, reverse
from .forms import UserEditForm, UserProfileEditForm
from django.contrib.auth.decorators import login_required

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(data=request.POST, instance=request.user)
        user_profile_form = UserProfileEditForm(data=request.POST, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            return HttpResponseRedirect(reverse('blog:home'))
    context = {
        'user_form': UserEditForm(instance=request.user),
        'user_profile_form': UserProfileEditForm(instance=request.user.profile)
    }
    return render(request, 'accounts/edit_profile.html', context)