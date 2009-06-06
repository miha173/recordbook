from django.conf.urls.defaults import *
urlpatterns = patterns("src.userextended.views",
                       (r'login', 'login'),
                       (r'logout', 'logout'),
                       )