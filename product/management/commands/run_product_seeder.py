from django.core.management.base import BaseCommand
from Backend_Shop.seeders.productSeeder import seed_products_from_csv
from product.seeder import generate_product_data_from_csv


class Command(BaseCommand):
    help = 'Seed product data from CSV file'

    def handle(self, *args, **options):
        csv_file_path = 'assets/fashion.csv'  # Adjust the path to your CSV file
        # image_folder = 'assets/images'  # Adjust the path to your image folder
        # seed_products_from_csv(csv_file_path, image_folder)
        generate_product_data_from_csv(csv_file_path, 50)
        self.stdout.write(self.style.SUCCESS('Successfully seeded product data'))
