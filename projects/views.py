from django.shortcuts import render, get_object_or_404
from projects.models import Project
from tickets.models import Ticket
from django.views.generic.detail import DetailView

def index(request):
    return render(request, 'index.html', {})

def projects_list(request):
    projects = Project.objects.all()
    return render(request, 'projects_list.html', {'objects': projects})

class ProjectDetail(DetailView):
    
    model = Project
    template_name = 'project_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        context['tickets'] = Ticket.objects.filter(project=self.object)
        return context