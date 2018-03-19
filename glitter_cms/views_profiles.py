from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from glitter_cms.forms_login import ChangeUserProfileForm, UserProfileForm
from django.contrib import messages


def public_user_profile(request, user_id):
    if len(user_id) < 1:
        return HttpResponse("Please enter a valid user id.")

    user = User.objects.get(id=user_id)

    return render(request, 'glitter_cms/profile/user_public.html', context={'user_data': user})


@login_required
def private_user_profile(request):
    if request.method == 'POST':
        user_form = ChangeUserProfileForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your changes to your profile have been saved.')
            return render(request, 'glitter_cms/profile/user_private.html',
                          context={'user_form': user_form, 'profile_form': profile_form})
        else:
            print(user_form.errors)
            print(profile_form.errors)
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = ChangeUserProfileForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    return render(request, 'glitter_cms/profile/user_private.html', context={'user_form': user_form, 'profile_form': profile_form})


