from django.shortcuts import render, get_object_or_404
from projects.models import Project
from tickets.models import Ticket, TicketComment, Attachment
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from tickets.forms import TicketForm, TicketCommentForm, AttachmentForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from rest_framework import viewsets, filters
import django_filters
from tickets.serializers import CommentSerializer
from django.conf import settings
from tickets.permissions import IsAuthorOrReadOnly
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class TicketDetail(LoginRequiredMixin, DetailView):

    model = Ticket
    template_name = 'ticket_detail.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(TicketDetail, self).get_context_data(**kwargs)
        context['files'] = Attachment.objects.filter(ticket=self.object)
        context['comments'] = TicketComment.objects.filter(ticket=self.object)
        context['page_size'] = settings.REST_FRAMEWORK['PAGE_SIZE']
        context['form'] = TicketCommentForm()
        return context


class CommentFilter(filters.FilterSet):
    newer_than = django_filters.NumberFilter(name='id', lookup_type='gt')
    class Meta:
        model = TicketComment
        fields = ['ticket', 'newer_than']


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    queryset = TicketComment.objects.all()
    filter_class = CommentFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AddTicketView(LoginRequiredMixin, CreateView):
    
    model = Ticket
    form_class = TicketForm
    template_name = 'ticket_form.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(AddTicketView, self).get_context_data(**kwargs)
        context['project'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.project = get_object_or_404(Project, pk=self.kwargs['pk'])
        self.object.save()
        pk = self.object.id
        messages.success(self.request, 'Тікет успішно створено.')
        return HttpResponseRedirect(reverse('ticket_detail', kwargs={'pk': pk}))

@login_required(login_url = reverse_lazy('login'))
def accept_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    ticket.status = ticket.ACCEPTED
    ticket.owner = request.user
    ticket.save()
    if ticket.project not in request.user.project_set.all():
        ticket.project.developers.add(request.user)
    messages.success(request, 'Ви прийняли тікет.')
    return HttpResponseRedirect(reverse('ticket_detail', kwargs={'pk': pk}))

@login_required(login_url = reverse_lazy('login'))
def close_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    ticket.status = ticket.CLOSED
    ticket.save()
    messages.success(request, 'Ви закрили тікет.')
    return HttpResponseRedirect(reverse('ticket_detail', kwargs={'pk': pk}))


class AttachmentCreateView(LoginRequiredMixin, CreateView):
    model = Attachment
    form_class = AttachmentForm
    template_name = 'attachment_form.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(AttachmentCreateView, self).get_context_data(**kwargs)
        context['ticket'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.ticket = get_object_or_404(Ticket, pk=self.kwargs['pk'])
        self.object.author = self.request.user
        self.object.save()
        pk = self.object.id
        messages.success(self.request, 'Файл успішно створено.')
        return HttpResponseRedirect(reverse('ticket_detail', kwargs={'pk': pk}))
