from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.views import generic
from groups.models import Group, Membership


class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description')
    model = Group

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.leader = self.request.user
        self.object.save()
        Membership.objects.create(group=self.object, user=self.request.user, date_joined=timezone.now())
        return super().form_valid(form)

    # def get(self, request, *args, **kwargs):
    #     group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
    #     try:
    #         Membership.objects.create(group=group, user=self.request.user, date_joined=timezone.now())
    #     except IntegrityError:
    #         messages.warning(self.request, ("Warning, already a member of {}".format(group.name)))
    #     else:
    #         messages.success(self.request, "You are now a member of the {} group.".format(group.name))
    #     return super().get(request, *args, **kwargs)


class DetailGroup(generic.DetailView):
    model = Group


class ListGroup(generic.ListView):
    model = Group


class DeleteGroup(LoginRequiredMixin, generic.DeleteView):
    model = Group

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(leader_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("groups:list")
