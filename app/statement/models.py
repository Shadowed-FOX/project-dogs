from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from .utils import haversine_distance


class MyUserManager(BaseUserManager):
    def create_user(
        self, email, firstname="None", lastname="None", contact="None", password=None
    ):
        """
        Creates and saves a User with the given email, password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            first_name=firstname,
            last_name=lastname,
            contact=contact,
            email=self.normalize_email(email),
        )

        user.is_active = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, firstname="None", lastname="None", contact="None", password=None
    ):
        """
        Creates and saves a superuser with the given email, and password.
        """
        user = self.create_user(
            email,
            firstname=firstname,
            lastname=lastname,
            contact=contact,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    User model. Contains personal info about user, date of join and permision fields.
    """

    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=11, null=True)

    date_joined = models.DateField(auto_now_add=True)

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        "Returns string of user email address."
        return self.email

    def __str__(self):
        """Returns string of user email address."""
        return self.email

    @property
    def is_staff(self):
        """Is user a member of staff?"""
        return self.is_admin

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, if user is admin
        return self.is_admin

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, if user is admin
        return self.is_admin

    def get_by_natural_key(self, email):
        """
        Retrieve a user by their email (natural key), case-insensitive.
        """
        return self.__class__.objects.get(email__iexact=email)


class City(models.Model):
    city = models.CharField(max_length=100)
    voivodeship = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.city}, {self.voivodeship}"

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"


class Dog(models.Model):
    SIZE_CHOICES = [
        ("small", "Mały"),
        ("medium", "Średni"),
        ("large", "Wielki"),
        ("very large", "Bardzo wielki"),
    ]

    STATEMENT_TYPE_CHOICES = [
        (False, "Znaleziony"),
        (True, "Zaginiony"),
    ]

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20, null=True, blank=True, default="")
    race = models.CharField(max_length=20)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default="medium")
    state_type = models.BooleanField(default=True, choices=STATEMENT_TYPE_CHOICES)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)

    radius = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=1)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    image = models.ImageField(upload_to="dog_images/")
    about = models.TextField()

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_display_size(self):
        size_dict = dict(self.SIZE_CHOICES)
        return size_dict.get(self.size, "Nieznany rozmiar")

    def get_display_state_type(self):
        type_dict = dict(self.STATEMENT_TYPE_CHOICES)
        return type_dict.get(self.state_type, "Nieznany typ")

    def __str__(self):
        return f"{self.name} ({self.size})"

    def save(self, *args, **kwargs):
        if self.latitude and self.longitude:
            closest_city = None
            closest_distance = float("inf")

            # TODO make it with binary search
            for city in City.objects.all():
                distance = haversine_distance(
                    self.latitude, self.longitude, city.latitude, city.longitude
                )
                if distance < closest_distance:
                    closest_distance = distance
                    closest_city = city

            self.city = closest_city

        super().save(*args, **kwargs)


class MessageChannel(models.Model):
    statement = models.OneToOneField(
        Dog, on_delete=models.CASCADE, related_name="channel"
    )
    participants = models.ManyToManyField(User, related_name="statement_channels")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Channel for Statement #{self.statement.id}"


class Message(models.Model):
    channel = models.ForeignKey(
        MessageChannel, on_delete=models.CASCADE, related_name="messages"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return (
            f"Message by {self.user.first_name} {self.user.last_name} in {self.channel}"
        )
