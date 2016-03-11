from django.contrib import admin
from tickets.models import Ticket, TicketComment, Attachment


admin.site.register([Ticket, TicketComment, Attachment])
