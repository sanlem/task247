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


class UserDetailView(LoginRequiredMixin, DetailView):
    
    model = get_user_model()
    template_name = 'profile.html'
    login_url = reverse_lazy('login')

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(get_user_model(), username=self.kwargs['username'])
        return user

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        projects = []
        tickets = Ticket.objects.filter(owner=self.object).order_by('created_at')
        assigned = tickets.filter(status=Ticket.ASSIGNED)
        accepted = tickets.filter(status=Ticket.ACCEPTED)
        for ticket in tickets:
            if ticket.project not in projects:
                projects.append(ticket.project)
        context['assigned_tickets'] = assigned
        context['accepted_tickets'] = accepted
        context['projects'] = projects
        return context
