from django.contrib import admin
from tickets.models import Ticket, TicketComment


admin.site.register([Ticket, TicketComment])
