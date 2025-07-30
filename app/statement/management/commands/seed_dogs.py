import csv
import os
from django.core.files import File
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from statement.models import Dog
from django.conf import settings

User = get_user_model()


class Command(BaseCommand):
    help = "Seed dogs from CSV and assign to test user"

    def handle(self, *args, **kwargs):
        # Create test user if not exists
        user, created = User.objects.get_or_create(
            email="test@test.com",
            defaults={"first_name": "Test", "last_name": "User", "is_active": True},
        )
        if created:
            user.set_password("test1234")
            user.save()
            self.stdout.write(self.style.SUCCESS("Created test user."))

        csv_path = os.path.join(settings.BASE_DIR, "dataset", "dogs.csv")
        image_path = os.path.join(settings.BASE_DIR, "dataset", "dog_image.jpg")

        if not os.path.exists(csv_path) or not os.path.exists(image_path):
            self.stdout.write(self.style.ERROR("CSV or image file not found."))
            return

        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                with open(image_path, "rb") as img_file:
                    dog = Dog(
                        name=row["name"],
                        race=row["race"],
                        size=row["size"],
                        state_type=row["state_type"].lower() == "true",
                        latitude=row["latitude"],
                        longitude=row["longitude"],
                        about=row["about"],
                        user_id=user,
                    )
                    dog.image.save("dog_image.jpg", File(img_file), save=True)
                    count += 1

            self.stdout.write(self.style.SUCCESS(f"Seeded {count} dogs."))
