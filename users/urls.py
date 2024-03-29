from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path(
        'login/',
        view = views.user_login,
        name = 'login'
    ),
    path(
        'signup/',
        view = views.user_signup,
        name = 'signup'
    ),
    path(
        'logout/',
        view = auth_views.LogoutView.as_view(
            template_name = 'users/logout.html'
        ),
        name = 'logout'
    ),
    path(
        'edit/',
        view = views.edit_user,
        name = 'edit_user'
    ),
    path(
        '<str:username>',
        view = views.profile,
        name = 'profile'
    ),
    path(
        'password_change/',
        view = auth_views.PasswordChangeView.as_view(
            template_name = 'users/pass_change_form.html'
        ),
        name = 'password_change'
    ),
    path(
        'password_change_done/',
        view = auth_views.PasswordChangeDoneView.as_view(
            template_name = 'users/pass_change_done.html'
        ),
        name = 'password_change_done'
    ),
    path(
        'password_reset/',
        view = auth_views.PasswordResetView.as_view(
            template_name = 'users/password_reset_form.html'
        ),
        name = 'password_reset'
    ),
    path(
        'password_reset/done',
        view = auth_views.PasswordResetDoneView.as_view(
            template_name = 'users/password_reset_form.html',
            extra_context = {
                "email_sent": True
            }
        ),
        name = 'password_reset_done'
    ),
    path(
        'password_reset/confirm/<uidb64>/<token>',
        view = auth_views.PasswordResetConfirmView.as_view(
            template_name = 'users/password_reset_confirm.html'
        ),
        name = 'password_reset_confirm'
    ),
    path(
        'password_reset/complete',
        view = auth_views.PasswordResetCompleteView.as_view(
            template_name = 'users/password_reset_confirm.html',
            extra_context = {
                "password_reset_success" : True
            }
        ),
        name = 'password_reset_complete'
    ),
    path(
        'api/follow/',
        view = views.follow_user,
        name = 'follow_user'
    ),
    path(
        'api/unfollow/',
        view = views.unfollow_user,
        name = 'unfollow_user'
    ),
    path(
        'api/following',
        view = views.get_following_list,
        name = 'following_list'
    ),
    path(
        'api/followers',
        view = views.get_followers_list,
        name = 'followers_list'
    )
]

