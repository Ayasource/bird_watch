from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Bird
from .forms import EntryForm


class BirdEntry(generic.ListView):
    queryset = Bird.objects.filter(status=1)
    template_name = "bird_watch_post/index.html"
    paginate_by = 6


def bird_entry(request, slug):
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


def entry_edit(request, slug, entry_id):
    """
    view to edit entries
    """
    if request.method == "POST":

        queryset = Bird.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        entry = get_object_or_404(Bird, pk=entry_id)
        entry_form = EntryForm(data=request.POST, instance=entry)

        if entry_form.is_valid() and entry.created_by == request.user:
            entry = entry_form.save(commit=False)
            entry.post = post
            entry.approved = False
            entry.save()
            messages.add_message(request, messages.SUCCESS, 'Bird Entry Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating Bird Entry!')

    return HttpResponseRedirect(reverse('bird_entry', args=[slug]))


def entry_delete(request, slug, entry_id):
    """
    view to delete entries
    """
    queryset = Bird.objects.filter(status=1)
    entry = get_object_or_404(queryset, slug=slug)
    entry = get_object_or_404(Bird, pk=entry_id)

    if entry.created_by == request.user:
        entry.delete()
        messages.add_message(request, messages.SUCCESS, 'Entry deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own entries!')
    return HttpResponseRedirect(reverse('bird_entry', args=[slug]))
