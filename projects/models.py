from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


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


class TOR(models.Model):
    project = models.ForeignKey(Project)
    text = models.TextField()
    version = models.IntegerField(validators=[MinValueValidator(5)], blank=True)

    class Meta:
        ordering = ['-version']

    def save(self, *args, **kwargs):
        try:
            self.version = self.__class__.objects.last().version + 1
        except Exception:
            self.version = 1
        super(TOR, self).save(*args, **kwargs)

    def __str__(self):
        return '%s ТЗ, v.%d' % (self.project.name, self.version)
