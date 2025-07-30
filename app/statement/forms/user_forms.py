from django import forms
from statement.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Hasło")
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, label="Potwierdź hasło"
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "contact", "password"]
        labels = {
            "first_name": "Imię",
            "last_name": "Nazwisko",
            "email": "Adres e-mail",
            "contact": "Numer kontaktowy",
            "password": "Hasło",
            "password_confirm": "Potwierdź hasło",
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Hasła nie są takie same.")

        if password:
            # Now validate password using Django validators
            try:
                validate_password(password)
            except ValidationError as e:
                # instead of just adding error to field, raise ValidationError for the form
                raise ValidationError({"password": e.messages})

        return cleaned_data


class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Adres E-mail")
    password = forms.CharField(widget=forms.PasswordInput, label="Hasło")

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
                if not user.check_password(password):
                    raise forms.ValidationError("Nieprawidłowy e-mail lub hasło")
                if not user.is_active:
                    raise forms.ValidationError(
                        "Prosze zweryfikuj e-mail przed logowaniem."
                    )
            except User.DoesNotExist:
                raise forms.ValidationError("Nieprawidłowy e-mail lub hasło")
        return cleaned_data


class UserUpdateForm(forms.ModelForm):
    contact = forms.CharField(label="Numer kontaktowy", required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "contact"]
        labels = {
            "first_name": "Imię",
            "last_name": "Nazwisko",
            "contact": "Numer kontaktowy",
        }


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Stare hasło")
    new_password = forms.CharField(widget=forms.PasswordInput, label="Nowe hasło")
    new_password_confirm = forms.CharField(
        widget=forms.PasswordInput, label="Potwierdź nowe hasło"
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not self.user.check_password(old_password):
            raise ValidationError("Stare hasło jest nieprawidłowe.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        new_password_confirm = cleaned_data.get("new_password_confirm")

        if new_password != new_password_confirm:
            raise ValidationError("Nowe hasła nie są identyczne.")

        validate_password(new_password, self.user)
        return cleaned_data
