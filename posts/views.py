from django.shortcuts import render, get_object_or_404
from .forms import PostCreationForm
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Post

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
        if post_form.is_valid():
            # create post object and not saving it in db bcoz user of post not set
            new_post = post_form.save(commit=False)
            new_post.user = request.user # adding logged in user to post
            new_post.save() #saving post in db
        else:
            return HttpResponse('invalid data')
    else:
        post_form = PostCreationForm(request.POST)

    context = {
        "post_form" : post_form
    }
    return render(request, 'posts/create.html', context=context)



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
        post = get_object_or_404(Post, id=post_id)
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
        })
    else:
        return JsonResponse({
            "error": "invalid request"
        })
