from django.shortcuts import render, get_object_or_404
from projects.models import Project
from tickets.models import Ticket, TicketComment
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from tickets.forms import TicketCommentForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class TicketDetail(DetailView):

    model = Ticket
    template_name = 'ticket_detail.html'

    def get_context_data(self, **kwargs):
        context = super(TicketDetail, self).get_context_data(**kwargs)
        context['comments'] = TicketComment.objects.filter(ticket=self.object)
        context['form'] = TicketCommentForm()
        return context


class AddComment(CreateView):
    
    model = TicketComment
    form_class = TicketCommentForm
    template_name = 'ticketcomment_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.ticket = get_object_or_404(Ticket, pk=self.kwargs['ticket'])
        self.object.save()
        return HttpResponseRedirect(reverse('ticket_detail', kwargs={'pk': self.kwargs['ticket']}))