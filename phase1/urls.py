from django.urls import path,include
from . import views
from django.conf.urls import url
urlpatterns=[
    path('welcome/',view=views.Welcome.as_view()),
    path('signup/',view=views.Register.as_view()),
    path('verify_otp/',view=views.VerifyAccount.as_view()),
    path('login/',view=views.Login.as_view()),
    path('forgot_password/',view=views.ForgotPassword.as_view()),
    path('reset_password/',view=views.ResetPassword.as_view()),
    path('club/list/',view=views.ClubList.as_view()),
    path('club/details/',view=views.ClubDetails.as_view()),
    path('club/member_list/',view=views.ClubMemberList.as_view()),
    path('club/add_member/',view=views.AddClubMembers.as_view()),
    path('club/remove_member/',view=views.RemoveClubMembers.as_view()),
    path('followclub',view=views.FollowClub.as_view()),
    path('unfollowclub',view=views.UnFollowClub.as_view()),
    path('postnews',view=views.PostNews.as_view()),
    path('create_event',view=views.CreateEvent.as_view()),
    
]