from django.contrib import admin
from projects.models import Project, TOR


admin.site.register([Project, TOR])
