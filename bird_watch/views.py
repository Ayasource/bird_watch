from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Bird


class BirdEntry(generic.ListView):
    queryset = Bird.objects.filter(status=1)
    template_name = "bird_watch_post/bird_entry.html"
    paginate_by = 1


def bird_detail(request, slug):
    """
    Display an individual :model:`bird_watch.Bird`.

    **Context**

    ``post``
        An instance of :model:`bird_watch.Bird`.

    **Template:**

    :template:`bird_watch/bird_entry.html`
    """

    queryset = Bird.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)

    return render(
        request,
        "bird_watch/bird_entry.html",
        {"bird": post},
    )
