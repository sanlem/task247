from django.shortcuts import render
from projects.models import Project, TOR
from tickets.models import Ticket
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect

def index(request):
    return render(request, 'index.html', {})

@login_required(login_url = reverse_lazy('login'))
def projects_list(request):
    projects = Project.objects.all()
    return render(request, 'projects_list.html', {'objects': projects})


class ProjectDetail(LoginRequiredMixin, DetailView):
    
    login_url = reverse_lazy('login')
    model = Project
    template_name = 'project_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        tickets = Ticket.objects.filter(project=self.object)
        context['accepted_tickets'] = tickets.filter(status=Ticket.ACCEPTED)
        context['assigned_tickets'] = tickets.filter(status=Ticket.ASSIGNED)
        context['unassigned_tickets'] = tickets.filter(status=Ticket.UNASSIGNED)
        context['closed_tickets'] = tickets.filter(status=Ticket.CLOSED)
        return context


class TORDetail(LoginRequiredMixin, DetailView):
    
    login_url = reverse_lazy('login')
    template_name = 'tor_detail.html'
    model = TOR
