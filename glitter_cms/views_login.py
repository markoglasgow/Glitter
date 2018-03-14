from django.shortcuts import render,redirect
from registration.backends.simple.views import RegistrationView
from glitter_cms.forms_login import UserForm, UserProfileForm
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
from django.contrib.auth.forms import UserCreationForm
from glitter_cms.forms_login import RegisterForm

# Create a new class that redirects the user to the index page,
#if successful at logging


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request, 'registration/registration_complete.html')
    else:
        form = RegisterForm()
    return render(request, 'registration/registration_form.html', {'form': form})

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
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
# An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
# Bad login details were provided. So we can't log the user in.
          #  print("Invalid login details: {0}, {1}".format(username, password))
           # return HttpResponse("Invalid login details supplied.")
            return render_to_response('registration/login.html',{
                'error': 'invaid information',
                'user_name':username,
                'user_pwd': password,
            })
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
            return render(request,'registration/password_change_done.html')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {
        'form': form
    })
