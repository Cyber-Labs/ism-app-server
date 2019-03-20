from django.urls import path,include
from . import views
from django.conf.urls import url
urlpatterns=[
    path('create_news/',view=views.PostNews.as_view()),
    path('edit_news/',view=views.EditNews.as_view()),
    path('delete/',view=views.NewsDelete.as_view()),
    path('list/',view=views.NewsList.as_view()),
    path('details/',view=views.NewsDetails.as_view()),
    path('club_news/',view=views.ClubNews.as_view()),
]