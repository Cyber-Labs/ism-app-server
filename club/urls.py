from django.urls import path,include
from . import views
from django.conf.urls import url
urlpatterns=[
    path('list/',view=views.ClubList.as_view()),
    path('details/',view=views.ClubDetails.as_view()),
    path('member_list/',view=views.ClubMemberList.as_view()),
    path('add_member/',view=views.AddClubMembers.as_view()),
    path('remove_member/',view=views.RemoveClubMembers.as_view()),
    path('followclub',view=views.FollowClub.as_view()),
    path('unfollowclub',view=views.UnFollowClub.as_view()),
]