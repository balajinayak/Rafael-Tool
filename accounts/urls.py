from django.urls import path
from accounts import views
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('add-user', views.AddUserView.as_view(), name='add_user'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_complete'),
]