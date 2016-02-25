from django.shortcuts import render, get_object_or_404
from projects.models import Project
from tickets.models import Ticket, TicketComment
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from tickets.forms import TicketCommentForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from rest_framework import viewsets, filters
import django_filters
from tickets.serializers import CommentSerializer
from django.conf import settings


class TicketDetail(LoginRequiredMixin, DetailView):

    model = Ticket
    template_name = 'ticket_detail.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(TicketDetail, self).get_context_data(**kwargs)
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


class AddComment(LoginRequiredMixin, CreateView):
    
    model = TicketComment
    form_class = TicketCommentForm
    template_name = 'ticketcomment_form.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.ticket = get_object_or_404(Ticket, pk=self.kwargs['ticket'])
        self.object.save()
        return HttpResponseRedirect(reverse('ticket_detail', kwargs={'pk': self.kwargs['ticket']}))