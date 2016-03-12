from django.shortcuts import render, get_object_or_404
from users.forms import RegistrationForm
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from tickets.models import Ticket
from django.db.models import Sum, Max
from collections import namedtuple


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('projects_list')

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('projects_list'))
        return super(RegistrationView, self).get(*args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        return render(self.request, 'registration_success.html', {'username': user.username})


# class Earning:
#     project = None
#     earned = None

Earning = namedtuple('Earning', ['project', 'earned'])


class UserDetailView(LoginRequiredMixin, DetailView):
    
    model = get_user_model()
    template_name = 'profile.html'
    login_url = reverse_lazy('login')

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(get_user_model(), username=self.kwargs['username'])
        return user

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        projects = self.object.project_set.annotate(total_points=Sum('ticket__points'))
        earned = []
        # shit here
        for proj in projects:
            points = proj.total_points
            t = proj.ticket_set.filter(status=Ticket.CLOSED,
                                       owner=self.object).aggregate(Sum('points'))
            try:
                point_sum = (t['points__sum'] / proj.total_points) * proj.cost
            except Exception:
                point_sum = 0
            earning = Earning(proj, point_sum)
            earned.append(earning)
        tickets = self.object.ticket_set.filter(owner=self.object).order_by('created_at')
        assigned = tickets.filter(status=Ticket.ASSIGNED)
        accepted = tickets.filter(status=Ticket.ACCEPTED)
        closed = tickets.filter(status=Ticket.CLOSED)
        points = {}
        context['assigned_tickets'] = assigned
        context['accepted_tickets'] = accepted
        context['closed_tickets'] = closed
        context['projects'] = earned
        return context
