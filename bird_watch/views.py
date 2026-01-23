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
def bird_entry(request, pk):
    """
    Display an individual bird - only if user owns it
    """

    bird = get_object_or_404(Bird, pk=pk, created_by=request.user)
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
def bird_edit(request, pk):
    bird = get_object_or_404(Bird, pk=pk, created_by=request.user)
    if request.method == "POST":
        form = BirdForm(request.POST, instance=bird)
        if form.is_valid():
            updated = form.save()
            messages.success(request, "Bird updated.")
            return HttpResponseRedirect(reverse("bird_entry", args=[updated.pk]))
    else:
        form = BirdForm(instance=bird)

    return render(request, "bird_watch_post/edit_bird.html", {
        "bird": bird,
        "bird_form": form,
    })


@login_required
def bird_delete(request, pk):
    bird = get_object_or_404(Bird, pk=pk, created_by=request.user)
    if request.method == "POST":
        bird.delete()
        messages.success(request, "Bird deleted.")
        return HttpResponseRedirect(reverse("home"))
    return render(request, "bird_watch_post/delete_bird.html", {"bird": bird})


def home_page(request):
    """
    Display the static home page or redirect authenticated users to user_home
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_home'))
    return render(request, "bird_watch_post/home.html")


@login_required
def user_bird_list(request):
    """
    Display only the logged-in user's birds
    """
    user_birds = Bird.objects.filter(created_by=request.user)
    return render(request, "bird_watch_post/bird_entry.html", {
        "bird": None,  # Set to None so the template shows empty state if no birds
        "birds": user_birds
    })


@login_required
def user_home(request):
    return render(request, "bird_watch_post/user_home.html")
