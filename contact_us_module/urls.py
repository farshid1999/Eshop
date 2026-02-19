from django.urls import path
from . import views
urlpatterns=[
    path('',views.ContactUsView.as_view(),name='contact-us'),
    path('profile-page/',views.CreatProfileView.as_view(),name='profile-page'),
    path('profile-list/', views.ProfilesView.as_view(), name='profile-list')
]
