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
import users.views
from rest_framework import routers
from django.conf.urls.static import static


router = routers.SimpleRouter()
router.register(r'comments', tickets.views.CommentViewSet, 'comment')
router.register(r'attachments', tickets.views.AttachmentReadOnlyViewSet, 'attachment')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', projects.views.index),
    url(r'^projects/$', projects.views.projects_list, name='projects_list'),
    url(r'^projects/(?P<pk>\d+)/$', projects.views.ProjectDetail.as_view(), name='projects_detail'),
    url(r'^projects/(?P<pk>\d+)/addticket/$', tickets.views.AddTicketView.as_view(), name='ticket_add'),
    url(r'^tickets/(?P<pk>\d+)/$', tickets.views.TicketDetail.as_view(), name='ticket_detail'),
    url(r'^tickets/(?P<pk>\d+)/accept/$', tickets.views.accept_ticket, name='ticket_accept'),
    url(r'^tickets/(?P<pk>\d+)/close/$', tickets.views.close_ticket, name='ticket_close'),
    url(r'^tickets/(?P<pk>\d+)/attach_file/$', tickets.views.AttachmentCreateView.as_view(), name='ticket_attach'),

    url(r'^login/', auth_views.login, {'template_name': 'login.html'},
        name="login"),
    url(r'^logout/', auth_views.logout, {'next_page': '/'}, name="logout"),
    url(r'^register/$', users.views.RegistrationView.as_view(), name='register'),
    url(r'^api/v1/', include(router.urls)),
    url(r'^users/(?P<username>[\w.@+-]+)$', users.views.UserDetailView.as_view(), name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
    ]
