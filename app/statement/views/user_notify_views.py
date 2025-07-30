from django.urls import reverse
from statement.forms.notify_forms import NotifyForm
from statement.models import Dog
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages


@login_required
def user_notify_list_view(request):
    notifications = Dog.objects.filter(user_id=request.user)
    context = {"user": request.user, "notifications": notifications}
    print(notifications)
    return render(request, "app/user/account.html", context)


@login_required
def user_notify_edit_view(request, id):
    notification = get_object_or_404(Dog, id=id, user_id=request.user)

    if request.method == "POST":
        form = NotifyForm(request.POST, request.FILES, instance=notification)
        if form.is_valid():
            form.save()
            messages.success(request, f"{notification.name} zaaktualizowano!")
            return redirect(reverse("edit_notify", kwargs={"id": str(id)}))
        else:
            messages.error(request, "Wystapil blad")
    else:
        form = NotifyForm(
            instance=notification,
            initial={
                "latitude": notification.latitude,
                "longitude": notification.longitude,
            },
        )

    return render(
        request,
        "app/user/notify/edit_notify.html",
        {"form": form, "notification": notification},
    )


@login_required
def user_notify_delete_view(request, id):
    notification = get_object_or_404(Dog, id=id, user_id=request.user)

    if request.method == "POST":
        notification.delete()
        messages.success(request, f"{notification.name} zostało usunięte.")
        return redirect("account")

    return render(
        request, "app/user/notify/delete_notify.html", {"notification": notification}
    )
