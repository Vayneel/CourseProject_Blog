from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from post_app.forms import *
from post_app.models import *
from user_app.models import UserAdditional


def main_page(request):
    return render(request, 'post_app/main_page.html', {'posts': Post.objects.all().order_by('-pub_date'),
                                                       'is_authenticated': request.user.is_authenticated})


def read_post(request, post_url):
    if Post.objects.filter(url_name=post_url).exists():
        is_auth = request.user.is_authenticated
        in_favorites = False
        in_liked = False
        if is_auth:
            fav_posts = UserAdditional.objects.get(linked_user=request.user).favorite_posts
            in_favorites = True if fav_posts.filter(url_name=post_url) else False
            liked_posts = UserAdditional.objects.get(linked_user=request.user).liked_posts
            in_liked = True if liked_posts.filter(url_name=post_url) else False
        if request.method == 'POST':
            if request.POST.get('comm_btn'):
                comm = CommentForm(request.POST).save(commit=False)
                comm.post = Post.objects.get(url_name=post_url)
                comm.author = request.user
                comm.save()

            try:
                if eval(request.POST.get('favorite_btn')):
                    fav_posts.add(Post.objects.get(url_name=post_url))
                elif not eval(request.POST.get('favorite_btn')):
                    fav_posts.remove(Post.objects.get(url_name=post_url))
            except TypeError:
                print("Favorite button wasn't pressed")

            try:
                if eval(request.POST.get('like_btn')):
                    liked_posts.add(Post.objects.get(url_name=post_url))
                elif not eval(request.POST.get('like_btn')):
                    liked_posts.remove(Post.objects.get(url_name=post_url))
            except TypeError:
                print("Like button wasn't pressed")

            return HttpResponseRedirect(Post.objects.get(url_name=post_url).url)
        post = Post.objects.get(url_name=post_url)
        comments = Comment.objects.filter(post=post)
        com_form = CommentForm()
        likes = UserAdditional.objects.filter(liked_posts__url_name=post_url).count()
        return render(request, 'post_app/read_post.html', {'post': post, 'comments': comments, 'likes': likes,
                                                           'is_authenticated': is_auth, 'in_favorites': in_favorites,
                                                           'in_liked': in_liked, 'form': com_form})
    return HttpResponseRedirect(reverse('main_page'))


def search_post(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        if request.GET.get('by_name'):
            posts = posts.filter(title__icontains=request.GET.get('by_name'))
        if request.GET.get('by_tag'):
            posts = posts.filter(tag__tag__iexact=request.GET.get('by_tag'))
        if request.GET.get('by_author'):
            posts = posts.filter(author__username__icontains=request.GET.get('by_author'))
        return render(request, 'post_app/search.html', {'form': SearchForm(request.GET), 'posts': posts,
                                                        'is_authenticated': request.user.is_authenticated})
    return render(request, 'post_app/search.html', {'form': SearchForm(),
                                                    'is_authenticated': request.user.is_authenticated})


@login_required
def favorites(request):
    posts = UserAdditional.objects.filter(linked_user=request.user).first().favorite_posts.all()
    return render(request, 'post_app/main_page.html', {'posts': posts, 'is_authenticated': True})


@login_required
def create_post(request):
    user = request.user
    if request.method == 'POST':
        tag_form = TagForm(request.POST)
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            if not Tag.objects.filter(tag=request.POST['tag']).exists():
                tag = tag_form.save()
            else:
                tag = Tag.objects.get(tag=request.POST['tag'])
            post = form.save(commit=False)
            post.tag = Tag.objects.get(tag=tag)
            post.author = user
            post.url_name = post.title.replace(' ', '-').lower()
            post.url = '/post/read/' + post.url_name + '/'
            post.save()
            return HttpResponseRedirect(reverse('main_page'))
        return render(request, 'post_app/post_form.html', {'form': form, 'tag': tag, 'is_authenticated': True})
    return render(request, 'post_app/post_form.html', {'form': PostForm(), 'tag': TagForm(), 'is_authenticated': True})
