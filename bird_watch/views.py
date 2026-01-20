from urllib import request
from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from requests import post
from .models import Bird, Entry
from .forms import BirdForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify


class BirdEntry(generic.ListView):
    model = Bird
    queryset = Bird.objects.filter(status=1)
    context_object_name = "birds"
    template_name = "bird_watch_post/index.html"
    paginate_by = 6


def profile_page(request):
    user = get_object_or_404(User, user=request.user)
    entries = user.creator.all()


@login_required
def user_profile(request):
    """
    Display all entries for the logged-in user
    """
    user_entries = Entry.objects.filter(created_by=request.user)
    user_birds = Bird.objects.filter(created_by=request.user)

    return render(request, "bird_watch_post/profile.html", {
        "user_entries": user_entries,
        "user_birds": user_birds
    })


def bird_entry(request, slug):
    """
    Display an individual :model:`bird_watch.Bird`.

    **Context**

    ``post``
        An instance of :model:`bird_watch.Bird`.

    **Template:**

    :template:`bird_watch/bird_entry.html`
    """

    bird = get_object_or_404(Bird.objects.filter(status=1), slug=slug)
    entries = bird.entries.filter(approved=True)
    entry_count = entries.count()
    bird_form = BirdForm()

    if request.method == "POST":
        bird_form = BirdForm(data=request.POST)
        if bird_form.is_valid():
            new_bird = bird_form.save(commit=False)
            new_bird.created_by = request.user
            new_bird.slug = slugify(new_bird.bird_name)
            new_bird.save()
            messages.add_message(request, messages.SUCCESS, 'Bird added successfully!')
            bird_form = BirdForm()

    return render(request, "bird_watch_post/bird_entry.html", {
        "bird": bird,
        "bird_form": bird_form,
        "entries": entries,
        "entry_count": entry_count,
    })


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
            entry.bird = post
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


@login_required
def add_bird(request):
    """
    Allow users to add a new bird sighting
    """
    if request.method == "POST":
        bird_form = BirdForm(data=request.POST)
        if bird_form.is_valid():
            bird = bird_form.save(commit=False)
            bird.created_by = request.user
            bird.slug = slugify(bird.bird_name)
            bird.save()
            messages.add_message(request, messages.SUCCESS, 'Bird added successfully!')
            return HttpResponseRedirect(reverse('home'))
    else:
        bird_form = BirdForm()
 
    return render(request, "bird_watch_post/add_bird.html", {"bird_form": bird_form})


@login_required
def bird_edit(request, slug):
    bird = get_object_or_404(Bird, slug=slug, created_by=request.user)
    if request.method == "POST":
        form = BirdForm(request.POST, instance=bird)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.slug = slugify(updated.bird_name)
            updated.save()
            messages.success(request, "Bird updated.")
            return HttpResponseRedirect(reverse("bird_entry", args=[updated.slug]))
    else:
        form = BirdForm(instance=bird)

    return render(request, "bird_watch_post/edit_bird.html", {
        "bird": bird,
        "bird_form": form,
    })


@login_required
def bird_delete(request, slug):
    bird = get_object_or_404(Bird, slug=slug, created_by=request.user)
    if request.method == "POST":
        bird.delete()
        messages.success(request, "Bird deleted.")
        return HttpResponseRedirect(reverse("home"))
    return render(request, "bird_watch_post/delete_bird.html", {"bird": bird})
