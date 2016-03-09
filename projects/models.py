from django.db import models
from django.conf import settings


class Project(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=500)
    deadline = models.DateTimeField()
    developers = models.ManyToManyField(settings.AUTH_USER_MODEL)
    repo_url = models.URLField(null=True, blank=True)
    customer = models.CharField(max_length=30)
    cost = models.IntegerField(default=0)

    def __str__(self):
        return self.name
