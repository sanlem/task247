from django.db import models
from django.conf import settings
from projects.models import Project


class Ticket(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=500)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    points = models.IntegerField(default=0)
    
    ASSIGNED = 'Assigned'
    ACCEPTED = 'Accepted'
    CLOSED = 'Closed'
    UNASSIGNED = 'Unassigned'
    STATUS_CHOICES = (
        (ACCEPTED, 'Accepted'),
        (ASSIGNED, 'Assigned'),
        (CLOSED, 'Closed'),
        (UNASSIGNED, 'Unassigned'),
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
    	                      default=UNASSIGNED, blank=True)
    ENHANCEMENT = 'Enhancement'
    FIX = 'Fix'
    GOAL_CHOICES = (
        (ENHANCEMENT, 'Enhancement'),
        (FIX, 'Fix'),
    )

    goal = models.CharField(max_length=11, choices=GOAL_CHOICES)

    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'
    PRIORITY_CHOICES = (
    	(HIGH, 'High'),
    	(MEDIUM, 'Medium'),
    	(LOW, 'Low'),
    )

    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES,
                                default=HIGH)

    def save(self, *args, **kwargs):
        # if ticket has an owner, it's status can only be ACCEPTED or ASSIGNED
        if self.owner and self.status != self.ACCEPTED:
            self.status = self.ASSIGNED
        super(Ticket, self).save(*args, **kwargs)

    def __str__(self):
        return self.project.name + '#' + self.name


class TicketComment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    text = models.TextField(max_length=300)
    ticket = models.ForeignKey(Ticket)


class Attachment(models.Model):
    attachment = models.FileField(upload_to='documents/%Y/%m/%d')
    ticket = models.ForeignKey(Ticket)
    name = models.CharField(max_length=30)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)