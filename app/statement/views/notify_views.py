# views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from statement.forms.notify_forms import NotifyForm, MessageForm
from django.contrib.auth.decorators import login_required
from statement.models import City, Dog, MessageChannel
from django.template.loader import render_to_string
from django.http import JsonResponse
from statement.forms.filter_forms import FilterForm


@login_required
def add_notify(request):
    if request.method == "POST":
        form = NotifyForm(request.POST, request.FILES)
        if form.is_valid():
            dog = form.save(commit=False)
            dog.user_id = request.user  # Assuming user_id is a ForeignKey to User
            dog.save()
            # Create MessageChannel and add user as participant
            channel = MessageChannel.objects.create(statement=dog)
            channel.participants.add(request.user)
            return redirect("list_notify")
    else:
        form = NotifyForm()
    return render(request, "app/notify/add_notify.html", {"form": form})


def statement_channel_view(request, id):
    dog = get_object_or_404(Dog, id=id)  # Or your actual model
    return render(request, "app/notify/channel.html", {"dog": dog})


def list_notify(request):
    form = FilterForm(request.GET or None)
    dogs = Dog.objects.select_related("city").all()

    if form.is_valid():
        voivodeship = form.cleaned_data.get("voivodeship")
        city = form.cleaned_data.get("city")
        size = form.cleaned_data.get("size")
        race = form.cleaned_data.get("race")
        name = form.cleaned_data.get("name")

        if voivodeship:
            dogs = dogs.filter(city__voivodeship=voivodeship)
        if city:
            dogs = dogs.filter(city=city)
        if size:
            dogs = dogs.filter(size=size)
        if race:
            dogs = dogs.filter(race__icontains=race)
        if name:
            dogs = dogs.filter(name__icontains=name)

    # Create a list of dog data with URLs
    dogs_data = [
        {
            "id": dog.id,
            "name": dog.name if dog.name else "",
            "race": dog.race,
            "size": dog.size,
            "city": dog.city.city,
            "voivodeship": dog.city.voivodeship,
            "display_size": dog.get_display_size(),
            "state_type": dog.get_display_state_type(),
            "latitude": float(dog.latitude),
            "longitude": float(dog.longitude),
            "image": dog.image.url if dog.image else "",
            "radius": float(dog.radius),
            "url": reverse("detail_notify", args=[dog.id]),  # Generate URL
        }
        for dog in dogs
        if dog.city is not None
    ]
    return render(
        request,
        "app/notify/list_notify.html",
        {
            "dogs": dogs,
            "form": form,
            "dogs_data_json": dogs_data,
        },
    )


def detail_notify(request, id):
    dog = get_object_or_404(Dog, id=id)
    dog.image = dog.image.url if dog.image else ""
    context = {
        "dog": dog,
    }
    print(dog.longitude, dog.latitude)
    return render(request, "app/notify/detail_notify.html", context)


def dog_detail_with_chat(request, id):
    dog = get_object_or_404(Dog, id=id)
    dog.image = dog.image.url if dog.image else ""

    # Get or create associated channel
    channel, created = MessageChannel.objects.get_or_create(statement=dog)
    if created:
        channel.participants.add(request.user)

    # Get messages for the chat
    messages = channel.messages.all().order_by("created_at")

    form = MessageForm() if request.user.is_authenticated else None

    context = {
        "dog": dog,
        "statement": dog,  # 'statement' for backward compatibility with your chat template
        "channel": channel,
        "messages": messages,
        "form": form,
        "can_send_messages": request.user.is_authenticated,
    }

    return render(request, "app/notify/detail_notify.html", context)


def get_cities(request):
    voivodeship = request.GET.get("voivodeship")
    cities = City.objects.filter(voivodeship=voivodeship).order_by("city")
    data = [{"city": city.city} for city in cities]
    return JsonResponse(data, safe=False)
