from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='register_page'),
    path('login/', views.LoginView.as_view(), name='login_page'),
    path('logout/', views.LogoutView.as_view(), name='logout_page'),
    path('activate-account/<str:active_code>',views.ActiveAccountView.as_view(),name='activate_account'),
    path('forgot-password/',views.ForgotPassView.as_view(),name='forgot_pass_page'),
    path('reset-password/<str:active_code>', views.ResetPass.as_view(), name='active_pass_code'),
]
