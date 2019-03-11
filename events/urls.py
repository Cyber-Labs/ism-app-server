from django.urls import path,include
from . import views
from django.conf.urls import url
urlpatterns=[
    
    path('create_event/',view=views.CreateEvent.as_view()),
    path('list/',view=views.EventList.as_view()),
    path('details/',view=views.EventDetails.as_view()),

]