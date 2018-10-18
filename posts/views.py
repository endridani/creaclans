from django.contrib import messages
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import SelectRelatedMixin
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from posts.models import Post, Comment
from groups.models import Group
from posts.forms import PostForm


class ListPost(SelectRelatedMixin, generic.ListView):
    model = Post
    select_related = ("user", "group")

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by("-published_date")


class DetailPost(generic.DetailView):
    model = Post


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_form(self, *args, **kwargs):
        form = super(CreatePost, self).get_form(*args, **kwargs)
        form.fields['group'].queryset = Group.objects.filter(members=self.request.user)
        return form

        # def get_queryset(self):
        #     group = get_object_or_404(Group, slug=self.object.group.get("slug"))
        #     queryset = super().get_queryset()
        #     return queryset.filter(self.request.user in group.members)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = Post
    select_related = ("user", "group")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(group__leader_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("groups:detail", kwargs={'slug': self.object.group.slug})


class ListDraftPost(LoginRequiredMixin, SelectRelatedMixin, generic.ListView):
    model = Post
    select_related = ("user", "group")

    def get_queryset(self):
        return Post.objects.filter(group__members=self.request.user, published_date__isnull=True).order_by("-created_date")


class UpdatePost(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostForm

    def get_form(self, *args, **kwargs):
        form = super(UpdatePost, self).get_form(*args, **kwargs)
        form.fields['group'].queryset = Group.objects.filter(members=self.request.user)
        return form


@login_required
def publish_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect("posts:list")
