from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post

# Create your views here.
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1)
    template_name = "bird_watch_post/index.html"
    paginate_by = 1

def post_detail(request, slug):
    """
    Display an individual :model:`bird_watch.Post`.

    **Context**

    ``post``
        An instance of :model:`bird_watch.Post`.

    **Template:**

    :template:`bird_watch/post_detail.html`
    """

    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)

    return render(
        request,
        "bird_watch/post_detail.html",
        {"post": post},
    )
