from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required

from .forms import RegisterForm, PostForm
from .models import Post


@login_required
def home(request):
    posts = Post.objects.all()
    if request.method == 'POST':
        post_id = request.POST.get('post-id')
        user_id = request.POST.get('user-id')

        if post_id:
            post = Post.objects.filter(id=post_id).first()
            if post and (post.author == request.user or request.user.has_perm('main.delete_post')):
                post.delete()
        elif user_id:
            user = User.objects.filter(id=user_id).first()
            if user and request.user.is_staff:
                try:
                    group = Group.objects.get(name='default')
                    group.user_set.remove(user)
                except:
                    pass
                try:
                    group = Group.objects.get(name='mod')
                    group.user_set.remove(user)
                except:
                    pass


    context = {'posts': posts}
    return render(request, 'main/home.html', context)


@login_required
@permission_required("main.add_post", raise_exception=True)  # raise_exception=True will raise error 403; False will
# redirect to login_url
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # if commit is not passed, it will create the entry in the db
            # automatically; we dont' want that since this form is incomplete - we need to add user to the form as
            # well (besides just title and description)
            post.author = request.user
            post.save()  # now we create the entry in db with the user
            return redirect('/home')
    else:
        form = PostForm()

    context = {'form': form}
    return render(request, 'main/create_post.html', context)


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    context = {'form': form}
    return render(request, 'registration/sign_up.html', context)

# for more built-in views (e.g. localhost:8000/password_reset/):
# https://docs.djangoproject.com/en/4.0/topics/auth/default/#using-the-views-1
