from django.urls import path
from django.contrib import admin
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:question_id>/voted_users/', views.voted_users, name='voted_users'),
    path("<int:question_id>/votado/", views.vote, name="votado"),
    path('<int:question_id>/unvote_and_revote/', views.unvote_and_revote, name='unvote_and_revote'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/disable/', views.disable_question, name='disable_question'),
    path('<int:question_id>/enable/', views.enable_question, name='enable_question'),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name= "logout"),
    path('edit_question_and_choices/<int:question_id>/', views.edit_question_and_choices, name='edit_question_and_choices'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),  
    path('edit_question_and_choices/<int:question_id>/', views.edit_question_and_choices, name='edit_question_and_choices'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('user_list/', views.user_list, name='user_list')
]
