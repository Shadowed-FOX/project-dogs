# forms.py
from django import forms
from statement.models import Dog, Message


class NotifyForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = ["name", "race", "size", "about", "state_type", "radius", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "race": forms.TextInput(attrs={"class": "form-control"}),
            "size": forms.Select(attrs={"class": "form-control"}),
            "about": forms.TextInput(attrs={"class": "form-control"}),
            "state_type": forms.Select(attrs={"class": "form-control"}),
            "radius": forms.NumberInput(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }
        labels = {
            "name": "Imię",
            "race": "Rasa",
            "size": "Wielkość",
            "about": "Opis",
            "radius": "Obszar (w kilometrach)",
            "image": "Zdjęcie",
            "state_type": "Rodzaj ogłoszenia",
        }

    latitude = forms.DecimalField(widget=forms.HiddenInput(), required=True)
    longitude = forms.DecimalField(widget=forms.HiddenInput(), required=True)

    def clean(self):
        cleaned_data = super().clean()
        latitude = cleaned_data.get("latitude")
        longitude = cleaned_data.get("longitude")

        if latitude is None or longitude is None:
            raise forms.ValidationError("Prosze zaznacz lokalizacje na mapie.")

        if not (-180 <= longitude <= 180):
            raise forms.ValidationError(
                "Długość geograficzna musi być między -180 i 180 stopni."
            )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        print(self.cleaned_data)
        if self.cleaned_data.get("latitude") and self.cleaned_data.get("longitude"):
            instance.latitude = self.cleaned_data["latitude"]
            instance.longitude = self.cleaned_data["longitude"]
        if commit:
            instance.save()
        return instance


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 1,
                    "placeholder": "Napisz wiadomość...",
                }
            )
        }
