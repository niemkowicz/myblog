
from django.contrib.auth import login, authenticate
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm  # Importujemy nasz niestandardowy formularz





from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponseForbidden
from .models import Post
from .forms import PostForm

class HomeView(View):
    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')
        post_form = PostForm()
        return render(request, 'home.html', {
            'posts': posts,
            'post_form': post_form,
        })

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        action = request.POST.get('action')

        if action == 'add_post':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('home')


        elif action == 'delete_post':
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, pk=post_id)

            if post.author != request.user:
                return HttpResponseForbidden("You are not allowed to delete this post.")

            post.delete()
            return redirect('home')

        return redirect('home')


class SignUpView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect('home')
        return render(request, 'registration/signup.html', {'form': form})

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'edit_post.html'
    context_object_name = 'post'

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.author != self.request.user:
            return HttpResponseForbidden("You are not allowed to edit this post.")
        post.save()
        return super().form_valid(form)