from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import LoginForm, SignupForm, UserEditForm, UserProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from posts.models import Post
from django.core.validators import validate_email

User = get_user_model()

# password validation function
def validate_password(password):
    # checking if password is of length 8 or not
    if len(password) < 8:
        return False

    # checking if password has atleast one uppercase letter
    if not any(char.isupper() for char in password):
        return False

    # checking if password has atleast one lowercase letter
    if not any(char.islower() for char in password):
        return False

    # checking if password has atleast one digit
    if not any(char.isdigit() for char in password):
        return False

    # checking if password has atleast one special character
    special_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '[', ']', '{', '}', '|', '\\', '/', '<', '>', ',', '.', '?', ':', ';', '~', '`']
    if not any(char in special_characters for char in password):
        return False

    return True




# Create your views here.

# handles user login request
def user_login(request):
    # redirecting user to user home page if already logged in
    if request.user.is_authenticated:
        return redirect('feed')


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
                return redirect('feed')
            else:
                # sending invalid credentials in response
                return render(request, 'users/login.html', {"invalid_login" : True})
        else: # sending invalid request when form data is not valid
            return render(request, 'users/login.html', {"login_error" : True})
    else:
        context = {}

        if 'source' in request.GET and request.GET['source'] == 'signup':
            context['signup_success'] = True

        return render(request, 'users/login.html', context)


# handles user signup request
def user_signup(request):
    # checks if user is logged in and if yes, then redirect to user home page
    if request.user.is_authenticated:
        return redirect('feed')

    # if form data is submitted
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)

        # returing error if account already exists with username
        try:
            username = request.POST['username'].strip().lower()

            User.objects.get(username=username)
            return render(request, 'users/signup.html', {"username_taken" : True, "form": signup_form})
        except:
            pass

        # first validating email
        try:
            email = request.POST['email'].strip()
            validate_email(email)

            #returning error if account already exitss with email
            try:
                User.objects.get(email=email)
                return render(request, 'users/signup.html', {"email_taken" : True, "form": signup_form})
            except:
                pass
        except:
            #invalid email
            return render(request, 'users/signup.html', {"invalid_email" : True})


        # first check if signup_form is data is valid
        if signup_form.is_valid():

            # validating password
            if not validate_password(signup_form.cleaned_data['password']):
                return render(request, 'users/signup.html', {"invalid_password" : True, "form": signup_form})

            new_user = signup_form.save(commit=False)
            new_user.set_password(signup_form.cleaned_data['password_confirm'])
            new_user.save()
            Profile.objects.create(user=new_user)

            # redirect to login page with context passed as signup_success
            return redirect(reverse('login') + '?source=signup')

        else:
            return render(request, 'users/signup.html', {"signup_error" : True})
    else:
        return render(request, 'users/signup.html')


@login_required
def edit_user(request):

    # handling when form is submitted
    if request.method == 'POST':
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST
        )

        profile_form = UserProfileEditForm(
            instance=request.user.profile,
            data = request.POST,
            files=request.FILES
        )

        print(request.FILES)
        # saving edits if both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('edit_user')
        else:
            return HttpResponse('Invalid input')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.profile)

    context = {
        "user_form" : user_form,
        "profile_form" : profile_form
    }

    return render(request, 'users/edit_user.html', context=context)


# handles profile page request of user
@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
        user_profile = Profile.objects.get(user=user)
        posts = Post.objects.filter(user=user).order_by('created_at').reverse()

    except:
        return redirect('feed')

    context = {
        "profile" : user_profile,
        "posts" : posts,
    }
    return render(request, 'users/index.html', context)