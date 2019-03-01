from django.urls import path
from . import views

app_name = 'chat'
urlpatterns = [
	#path('farms/<int:pk>', views.FarmList.as_view(), name='farm-detail'), # GET request for user with id
    path('', views.FarmList.as_view(), name='farm-list'), # Get full list of farms

    # # topics
    path('topics/', views.TopicList.as_view(), name='topic_list'), # Get list of topic ?id=1
    path('messages/', views.ForumList.as_view(), name='message-list'),      # Get related message ?pk=1
    path('register/', view=views.Register.as_view()),

]

