"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from statement.views.user_notify_views import (
    user_notify_delete_view,
    user_notify_edit_view,
    user_notify_list_view,
)
from statement.views.user_views import (
    register,
    verify_email,
    login_view,
    logout_view,
    update_user_info,
    change_password,
)
from statement.views.notify_views import (
    add_notify,
    list_notify,
    detail_notify,
    dog_detail_with_chat,
    get_cities,
)
from django.conf import settings
from django.conf.urls.static import static
from statement import routing as statement_routing

urlpatterns = [
    # Admin views
    path("admin/", admin.site.urls),
    # User views
    path("register/", register, name="register"),
    path("verify/<uidb64>/<token>/", verify_email, name="verify_email"),
    path(
        "verified/",
        lambda request: render(request, "app/user/verified.html"),
        name="registration_verified",
    ),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("account/", user_notify_list_view, name="account"),
    path("account/update_user", update_user_info, name="update_user_info"),
    path("account/change_password", change_password, name="change_password"),
    path("account/edit/<str:id>/", user_notify_edit_view, name="edit_notify"),
    path("account/delete/<str:id>/", user_notify_delete_view, name="delete_notify"),
    # Notify views
    path("add_notify/", add_notify, name="add_notify"),
    path("", list_notify, name="list_notify"),
    path("detail_notify/<str:id>/", dog_detail_with_chat, name="detail_notify"),
    path("get-cities/", get_cities, name="get_cities"),
]

websocket_urlpatterns = statement_routing.websocket_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
