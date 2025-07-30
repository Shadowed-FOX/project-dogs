from django.contrib import admin
from .models import *

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Dog, City
from django import forms


# Custom User Admin for your custom User model
class CustomUserAdmin(UserAdmin):
    # The fields to be used in displaying the User model.
    list_display = ("email", "first_name", "last_name", "is_admin", "date_joined")
    list_filter = ("is_admin",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "contact")}),
        ("Permissions", {"fields": ("is_admin", "is_active")}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin overrides get_fieldsets
    # to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "contact",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    filter_horizontal = ()


# Dog Admin configuration
class DogAdmin(admin.ModelAdmin):
    list_display = ("name", "size", "user_id", "longitude")
    list_filter = ("size",)
    search_fields = ("name", "user_id__email")
    raw_id_fields = ("user_id",)


class MessageInline(admin.TabularInline):
    model = Message
    extra = 1
    fields = ("user", "content", "created_at")
    readonly_fields = ("created_at",)
    ordering = ("created_at",)


@admin.register(MessageChannel)
class MessageChannelAdmin(admin.ModelAdmin):
    list_display = ("id", "statement", "created_at", "participant_count")
    list_filter = ("created_at",)
    search_fields = ("statement__name", "statement__id")
    readonly_fields = ("created_at",)
    filter_horizontal = ("participants",)
    inlines = [MessageInline]

    def participant_count(self, obj):
        return obj.participants.count()

    participant_count.short_description = "Participants"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("statement").prefetch_related("participants")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "channel", "user", "content_preview", "created_at")
    list_filter = ("channel", "user", "created_at")
    search_fields = ("content", "user__first_name", "user__last_name")
    readonly_fields = ("created_at",)
    fields = ("channel", "user", "content", "created_at")
    ordering = ("created_at",)

    def content_preview(self, obj):
        return obj.content[:50] + ("..." if len(obj.content) > 50 else "")

    content_preview.short_description = "Content"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("channel__statement", "user")


class CityAdminForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ["city", "voivodeship", "latitude", "longitude"]
        widgets = {
            "latitude": forms.NumberInput(attrs={"readonly": "readonly"}),
            "longitude": forms.NumberInput(attrs={"readonly": "readonly"}),
        }


class CityAdmin(admin.ModelAdmin):
    form = CityAdminForm
    list_display = ("city", "voivodeship", "latitude", "longitude")
    search_fields = ("city", "voivodeship")
    ordering = ("city",)

    # Custom template for map integration
    change_form_template = "admin/city_change_form.html"


admin.site.register(City, CityAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Dog, DogAdmin)
