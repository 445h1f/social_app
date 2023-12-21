from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', view=views.user_index, name='user_home'),
    path('login/', view=views.user_login, name='login'),
    path('signup/', view=views.user_signup, name='signup'),
    path('signup/success', view=views.user_signup, name='signup_success'),
    path('logout/', view=auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password_change/', view=auth_views.PasswordChangeView.as_view(template_name='users/pass_change_form.html'), name='password_change'),
    path('password_change_done/', view=auth_views.PasswordChangeDoneView.as_view(template_name='users/pass_change_done.html'), name='password_change_done'),
    path('password_reset/', view=auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html'), name='password_reset'),
    path('password_reset/done', view=auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>', view=auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/complete', view=auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete')
]

