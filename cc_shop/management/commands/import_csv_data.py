import csv
import os
import random
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db import transaction
from cc_shop.models import Country, CountryMetadata, ElectricConsumption, Product

class Command(BaseCommand):
    help = 'Automatically imports data and metadata from CSV files in the data folder, clearing previous entries.'

    def handle(self, *args, **options):
        base_dir = settings.BASE_DIR
        data_csv_path = os.path.join(base_dir, 'cc_shop', 'data', 'epcons_data.csv')
        metadata_csv_path = os.path.join(base_dir, 'cc_shop', 'data', 'epcons_metadata.csv')

        self.stdout.write(self.style.SUCCESS('Clearing existing data...'))
        CountryMetadata.objects.all().delete()
        ElectricConsumption.objects.all().delete()
        Country.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Importing new data...'))
        with transaction.atomic():
            self.parse_country_data(data_csv_path)
            self.parse_country_metadata(metadata_csv_path)
        self.stdout.write(self.style.SUCCESS('Data import completed successfully.'))

    def parse_country_data(self, csv_file_path):
        with open(csv_file_path, newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.DictReader(csvfile)
            reader.fieldnames = [field.strip() for field in reader.fieldnames]  # Strip spaces from headers

            for row in reader:
                if 'Country Code' not in row or not row['Country Code'].strip():
                    self.stdout.write(self.style.WARNING('Missing "Country Code" in row, skipping.'))
                    continue

                country, created = Country.objects.update_or_create(
                    country_code=row['Country Code'].strip(),
                    defaults={'country_name': row['Country Name'].strip()}
                )
                self.import_yearly_data(row, country)

                # Optionally create a Product for each country
                Product.objects.update_or_create(
                    country=country,
                    defaults={
                        'description': 'Energy conservation credit',
                        'price': random.uniform(50.00, 200.00),
                        'type': 'Renewable Energy Credit'
                    }
                )

    def import_yearly_data(self, data_row, country):
        for year in range(1994, 2015):
            year_key = str(year)
            if year_key in data_row and data_row[year_key].strip():
                ElectricConsumption.objects.create(
                    country=country,
                    year=year,
                    consumption=float(data_row[year_key]) if data_row[year_key] else None
                )

    def parse_country_metadata(self, csv_file_path):
        with open(csv_file_path, newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.DictReader(csvfile)
            reader.fieldnames = [field.strip() for field in reader.fieldnames]  # Strip spaces from headers

            for row in reader:
                if 'Country Code' not in row:
                    self.stdout.write(self.style.WARNING('Missing "Country Code" in row, skipping metadata entry.'))
                    continue
                try:
                    country = Country.objects.get(country_code=row['Country Code'].strip())
                    CountryMetadata.objects.update_or_create(
                        country=country,
                        defaults={
                            'long_name': row.get('Long Name', '').strip(),
                            'region': row.get('Region', '').strip(),
                            'currency_unit': row.get('Currency Unit', '').strip(),
                            'income_group': row.get('Income Group', '').strip(),
                            'special_notes': row.get('Special Notes', '').strip(),
                        }
                    )
                except ObjectDoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Country not found for {row['Country Code']}, skipping metadata entry."))