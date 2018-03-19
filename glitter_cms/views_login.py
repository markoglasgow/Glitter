from django.shortcuts import render,redirect
from glitter_cms.forms_login import RegisterForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from glitter_cms.models import Profile
from glitter_cms.views_search import enable_all_search_settings
from datetime import datetime

# Create a new class that redirects the user to the index page,
#if successful at logging


def register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user_profile = Profile.objects.get(user=user)
            user_profile.student_id = profile_form.cleaned_data.get('student_id')
            user_profile.save()

            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request, 'registration/registration_complete.html')
        else:
            print(user_form.errors)
            print(profile_form.errors)
            messages.error(request, 'Please correct errors in form and try again.')
    else:
        user_form = RegisterForm()
        profile_form = UserProfileForm()
    return render(request, 'registration/registration_form.html', {'user_form': user_form, 'profile_form': profile_form})

@csrf_exempt
def user_login(request):
# If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
# Gather the username and password provided by the user.
# This information is obtained from the login form.
# We use request.POST.get('<variable>') as opposed
# to request.POST['<variable>'], because the
# request.POST.get('<variable>') returns None if the
# value does not exist, while request.POST['<variable>']
# will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')
# Use Django's machinery to attempt to see if the username/password
# combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
# If we have a User object, the details are correct.
# If None (Python's way of representing the absence of a value), no user
# with matching credentials was found.
        if user:
# Is the account active? It could have been disabled.
            if user.is_active:
# If the account is valid and active, we can log the user in.
# We'll send the user back to the homepage.
                enable_all_search_settings(request)
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
# An inactive account was used - no logging in!

                return HttpResponse("Your account is disabled.")
        else:
# Bad login details were provided. So we can't log the user in.
          #  print("Invalid login details: {0}, {1}".format(username, password))
           # return HttpResponse("Invalid login details supplied.")
            messages.info(request, 'Please input the correct username or password')
            return redirect('login')
# The request is not a HTTP POST, so display the login form.
# This scenario would most likely be a HTTP GET.
    else:
# No context variables to pass to the template system, hence the
# blank dictionary object...
        return render(request, 'registration/login.html', {})

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return render(request,
                'registration/logout.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password_change')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {
        'form': form
    })

# def get_server_side_cookie(request, cookie, default_val=None):
#     val = request.session.get(cookie)
#     if not val:
#         val = default_val
#     return val
#
# def visitor_cookie_handler(request):
#     visits = int(get_server_side_cookie(request, 'visits', '1'))
#     last_visit_cookie = get_server_side_cookie(request,
#                                                 'last_visit',
#                                                 str(datetime.now()))
#     last_visit_time = datetime.strptime(last_visit_cookie[:-7],
#                                         '%Y-%m-%d %H:%M:%S')
# # If it's been more than a day since the last visit...
#     if (datetime.now() - last_visit_time).days > 0:
#         visits = visits + 1
# #update the last visit cookie now that we have updated the count
#         request.session['last_visit'] = str(datetime.now())
#     else:
#         visits = 1
# # set the last visit cookie
#         request.session['last_visit'] = last_visit_cookie
# # Update/set the visits cookie
#     request.session['visits'] = visits