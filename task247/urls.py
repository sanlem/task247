"""task247 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles import views
from django.conf import settings
from django.contrib.auth import views as auth_views
import projects.views
import tickets.views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'comments', tickets.views.CommentViewSet, 'comment')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', projects.views.index),
    url(r'^projects/$', projects.views.projects_list, name='projects_list'),
    url(r'^projects/(?P<pk>\d+)/$', projects.views.ProjectDetail.as_view(), name='projects_detail'),
    url(r'^tickets/(?P<pk>\d+)/$', tickets.views.TicketDetail.as_view(), name='ticket_detail'),
    url(r'^tickets/(?P<ticket>\d+)/comment/add/$',
        tickets.views.AddComment.as_view(), name='ticket_comment_add'),

    url(r'^login/', auth_views.login, {'template_name': 'login.html'},
        name="login"),
    url(r'^logout/', auth_views.logout, {'next_page': '/'}, name="logout"),
    url(r'^api/v1/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
    ]
