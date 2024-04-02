import csv
from product.models import Product
import os
from decimal import Decimal

def seed_products_from_csv(csv_file_path, image_folder):
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Extracting data from CSV row
            title = row['Title']
            image_name = os.path.basename(row['Image Src'])
            image_path = os.path.join(image_folder, image_name)
            price_str = row['Variant Price']
            if not price_str.strip():  # Check if the string is empty or contains only whitespace
                print(f"Empty price value for product: {title}. Skipping...")
                continue  # Skip this row if price is empty
            try:
                price = Decimal(price_str)
            except Exception as e:
                print(f"Invalid price value '{price_str}' for product: {title}. Skipping...")
                continue  # Skip this row if price is not valid
            tags = row['Tags']
            type = row['Type']
            vendor = row['Vendor']
            body = row['Body (HTML)']

            # Creating product instance
            product = Product.objects.create(
                title=title,
                image_path=image_path,  # Store the image path instead of using ImageField
                price=price,
                tags=tags,
                type=type,
                vendor=vendor,
                body=body
            )


# # Path to your CSV file
# csv_file_path = '../../assets/jewelery.csv'
# # Folder where your images are stored
# image_folder = '../../assets/images'
#
# seed_products_from_csv(csv_file_path, image_folder)
