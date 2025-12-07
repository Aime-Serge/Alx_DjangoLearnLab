from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Post
from .models import Post, Comment
from .forms import CustomUserCreationForm, ProfileForm, PostForm, CommentForm
from taggit.models import Tag


def home(request):
	posts = Post.objects.all().order_by("-published_date")
	return render(request, "blog/home.html", {"posts": posts})


def register(request):
	if request.method == "POST":
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful. You are now logged in.")
			return redirect("blog:profile")
	else:
		form = CustomUserCreationForm()
	return render(request, "blog/register.html", {"form": form})


@login_required
def profile(request):
	user = request.user
	if request.method == "POST":
		form = ProfileForm(request.POST, instance=user)
		if form.is_valid():
			form.save()
			messages.success(request, "Profile updated.")
			return redirect("blog:profile")
	else:
		form = ProfileForm(instance=user)
	return render(request, "blog/profile.html", {"form": form})


class PostListView(ListView):
	model = Post
	template_name = "blog/posts_list.html"
	context_object_name = "posts"
	ordering = ["-published_date"]


def posts_by_tag(request, tag_name):
	tag = Tag.objects.filter(name=tag_name).first()
	posts = tag.posts.all().order_by('-published_date') if tag else Post.objects.none()
	return render(request, 'blog/posts_list.html', {'posts': posts, 'tag': tag})


class PostByTagListView(ListView):
	model = Post
	template_name = "blog/posts_list.html"
	context_object_name = "posts"

	def get_queryset(self):
		tag_slug = self.kwargs.get('tag_slug')
		if tag_slug:
			return Post.objects.filter(tags__slug=tag_slug).order_by('-published_date')
		return Post.objects.none()

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		tag_slug = self.kwargs.get('tag_slug')
		ctx['tag'] = Tag.objects.filter(slug=tag_slug).first() if tag_slug else None
		return ctx


def search(request):
	query = request.GET.get('q', '').strip()
	posts = Post.objects.none()
	if query:
		from django.db.models import Q
		posts = Post.objects.filter(
			Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__name__icontains=query)
		).distinct().order_by('-published_date')
	return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})


class PostDetailView(DetailView):
	model = Post
	template_name = "blog/post_detail.html"

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		post = self.get_object()
		ctx["comments"] = post.comments.all()
		ctx["comment_form"] = CommentForm()
		return ctx


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	form_class = PostForm
	template_name = "blog/post_form.html"

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	form_class = PostForm
	template_name = "blog/post_form.html"

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	template_name = "blog/post_confirm_delete.html"
	success_url = reverse_lazy("blog:posts")

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author


class CommentCreateView(LoginRequiredMixin, CreateView):
	model = Comment
	form_class = CommentForm

	def form_valid(self, form):
		post_pk = self.kwargs.get("post_pk") or self.kwargs.get("pk") or self.kwargs.get("post_id")
		post = get_object_or_404(Post, pk=post_pk)
		form.instance.author = self.request.user
		form.instance.post = post
		return super().form_valid(form)

	def get_success_url(self):
		return self.object.post.get_absolute_url() if hasattr(self.object.post, "get_absolute_url") else reverse_lazy("blog:post_detail", args=[self.object.post.pk])


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Comment
	form_class = CommentForm
	template_name = "blog/comment_form.html"

	def test_func(self):
		comment = self.get_object()
		return self.request.user == comment.author

	def get_success_url(self):
		return reverse_lazy("blog:post_detail", args=[self.object.post.pk])


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Comment
	template_name = "blog/comment_confirm_delete.html"

	def test_func(self):
		comment = self.get_object()
		return self.request.user == comment.author

	def get_success_url(self):
		return reverse_lazy("blog:post_detail", args=[self.object.post.pk])
