from django.shortcuts import render, redirect
from .forms import PostCreationForm
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from .models import Post, Comment

# Create your views here.

# view to handle creation of post request
@login_required
def create_post(request):

    # handles when post creation form is submitted
    if request.method == 'POST':
        post_form = PostCreationForm(
            data=request.POST,
            files=request.FILES
        )
        # checking if form is valid
        if post_form.is_valid() and len(request.POST['title'].strip()) <= 200 and len(request.POST['caption']) <= 5000:
            # create post object and not saving it in db bcoz user of post not set
            new_post = post_form.save(commit=False)
            new_post.user = request.user # adding logged in user to post
            new_post.save() #saving post in db

            return redirect('feed')
        else:
            return HttpResponse('invalid data')
    else:
        post_form = PostCreationForm(request.POST)

    context = {
        "post_form" : post_form
    }
    return render(request, 'posts/create.html', context=context)


# view to display post in a single page
def view_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except:
    # if post not found with given post id, redirecting to feed
        return redirect('feed')
    context = {
        "post" : post,
        "single_post" : True,
        "title" : f'Post | @{post.user.username}'
    }
    return render(request, 'posts/single_post.html', context)


# feed page
def feed_page(request):
    posts = Post.objects.all().order_by('created_at').reverse()
    context = {
        "posts" : posts,
        "title" : 'Feed Page'
    }
    return render(request, 'posts/feed.html', context)


@login_required
def like_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        try:
            post = Post.objects.get(pk=post_id)
        except:
        # if post not found with given post id, redirecting to feed
            return JsonResponse({
            "error": "invalid request"
        },  status=404)

        status = False

        # if post is already liked, the unlike it
        if post.liked_by.filter(id=request.user.id).exists():
            # remove current user from liked_by
            post.liked_by.remove(request.user)
        else:
            # adds like by logged in user
            post.liked_by.add(request.user)
            status = True

        return JsonResponse({
            "count" : post.liked_by.count(),
            'status' : status
        }, status=200)
    else:
        return JsonResponse({
            "error": "invalid request"
        }, status=404)


@login_required
def comment_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        try:
            post = Post.objects.get(pk=post_id)
        except:
        # if post not found with given post id, redirecting to feed
            return JsonResponse({
            "error": "invalid request"
            }, status=404)

        comment_text = request.POST.get('comment').strip()
        if len(comment_text) > 50:
            return JsonResponse({
                "error": "invalid request"
                }, status=404)
        comment = Comment(post=post, user=request.user, body=comment_text)
        comment.save()

        comment_element = render_to_string(
            'posts/components/comment.html',
            {
                "comment" : comment
            }
        )
        print(comment_element)
        return JsonResponse({
            "count" : post.comments.count(),
            "html" : comment_element,
        }, status=200)
    else:
        return JsonResponse({
            "error": "invalid request",
        }, status=404)