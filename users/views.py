from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignupForm
from django.contrib.auth.decorators import login_required


# Create your views here.

# handles user login request
def user_login(request):
    # redirecting user to user home page if already logged in
    if request.user.is_authenticated:
        return redirect('user_home')


    # handles login data
    if request.method == 'POST':
        form = LoginForm(request.POST) #getting form data

        #checking user if form data is valid
        if form.is_valid():
            data = form.cleaned_data # cleaning it

            # authenticating user (checking if valid or not)
            user = authenticate(request, username=data['username'], password=data['password'])

            # logging user if it is valid
            if user is not None:
                login(request, user=user)
                return redirect('user_home')
            else:
                # for invalid credentials
                return HttpResponse(f'Invalid login credentials')
        else: # sending invalid request when form data is not valid
            return redirect('user_home')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', context={"form":form})


# handles index page request
@login_required
def user_index(request):
    return render(request, 'users/index.html')


# handles user signup request
def user_signup(request):
    # checks if user is logged in and if yes, then redirect to user home page
    if request.user.is_authenticated:
        return redirect('user_home')

    # if form data is submitted
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)

        # first check if signup_form is data is valid
        if signup_form.is_valid():
            new_user = signup_form.save(commit=False)
            new_user.set_password(signup_form.cleaned_data['password_confirm'])
            new_user.save()

            return render(request, 'users/signup_complete.html')

    else:
        signup_form = SignupForm()
        return render(request, 'users/signup.html', {'signup_form': signup_form})