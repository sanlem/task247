from django.shortcuts import render
from users.forms import RegistrationForm
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect


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
