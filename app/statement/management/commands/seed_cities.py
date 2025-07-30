import csv
import os
from django.core.management.base import BaseCommand
from statement.models import City
from django.conf import settings


class Command(BaseCommand):
    help = "Seeds the database with city data from a CSV file in the dataset directory"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="cities.csv",
            help="Name of the CSV file in the dataset directory (default: cities.csv)",
        )

    def handle(self, *args, **options):
        csv_file_name = options["file"]
        csv_file_path = os.path.join(settings.BASE_DIR, "dataset", csv_file_name)

        try:
            with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile, delimiter=";")
                for row in reader:
                    City.objects.get_or_create(
                        city=row["Miasto"],
                        voivodeship=row["Wojewodztwo"],
                        latitude=float(row["Latitude"]),
                        longitude=float(row["Longitude"]),
                    )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully seeded city data from {csv_file_path}"
                )
            )
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f"CSV file not found at {csv_file_path}")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error seeding data: {str(e)}"))
