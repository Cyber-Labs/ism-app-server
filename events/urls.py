from django.urls import path,include
from . import views
from django.conf.urls import url
urlpatterns=[
    
    path('create_event/',view=views.CreateEvent.as_view()),
    path('list/',view=views.EventList.as_view()),
    path('details/',view=views.EventDetails.as_view()),
    path('edit/',view=views.EditEvent.as_view()),
    path('delete/',view=views.EventDelete.as_view()),
    path('club_event_list/',view=views.ClubEvent.as_view()),

]