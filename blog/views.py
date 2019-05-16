from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404, redirect
from .models import Post, Comment
from .forms import PostCreateForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse

def homeView(request):
    q = request.GET.get('q')
    if q is not None:
        posts = Post.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
    else:
        posts = Post.objects.all().order_by('-id')
    context = {
        'posts': posts,
        'q' : q,
    }
    return render(request, "blog/blog_home.html", context)


def PostDetailView(request, slug):
    post = Post.objects.get_by_slug(slug)
    comments = post.comments.filter(reply=None)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        reply_id = request.POST.get('comment_id')
        comment_qs = None
        if comment_form.is_valid():
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.reply = comment_qs
            comment.save()
    comment_form = CommentForm()
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    context = {
        'post': post,
        'comments': comments,
        'comment_form':comment_form,
        'is_liked': is_liked,
    }
    if request.is_ajax():
        html = render_to_string('blog/_comment_section.html', context, request=request)
        return JsonResponse({'data':html})
    return render(request, "blog/blog_detail.html", context)


@login_required
def PostCreateView(request):
    form = PostCreateForm()
    context = {
        'form': form,
    }
    return render(request, 'blog/add_post.html', context)


@login_required
def likePost(request):
    # For fetch api
    # data = json.loads(request.body)
    # post = get_object_or_404(Post, id=data.get('id'))

    post = get_object_or_404(Post, id=request.POST.get('id'))

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True

    context = {
        'post': post,
        'is_liked': is_liked,
    }
    if request.is_ajax():
        html = render_to_string('blog/_like_section.html', context, request=request)
        return JsonResponse({'data':html})