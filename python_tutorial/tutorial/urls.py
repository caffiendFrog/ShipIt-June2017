from django.conf.urls import url 
from tutorial import views 

urlpatterns = [ 
  # The home view ('/tutorial/') 
  url(r'^$', views.home, name='home'), 
  # Explicit home ('/tutorial/home/') 
  url(r'^home/$', views.home, name='home'), 
  # Redirect to get token ('/tutorial/gettoken')
  url(r'^gettoken/$', views.gettoken, name='gettoken'),
]
