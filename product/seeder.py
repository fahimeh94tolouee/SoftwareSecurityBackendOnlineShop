import csv
import os
import random

import requests
from django.utils import timezone
from faker import Faker

from authentication.models import CustomUser
from .models import Product, Color, ProductQuestion, ProductAnswer

# Initialize Faker to generate fake data
fake = Faker()

# Define available colors
available_colors = ['White', 'Red', 'Blue', 'Green', 'Yellow', 'Black']


# Function to generate random colors array
def generate_random_colors():
    return random.sample(available_colors, random.randint(1, len(available_colors)))


# Function to generate tags
def generate_tags(gender, category, subcategory, product_type, product_title):
    return f"{gender} {category} {subcategory} {product_type} {product_title}"


# Function to download image from URL
def download_image(image_url, image_name):
    image_path = os.path.join('assets', 'images', image_name)
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(image_path, 'wb') as image_file:
            image_file.write(response.content)
    return image_path


def generate_product_data_from_csv(csv_file_path, num_products):
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = random.sample(list(reader), num_products)  # Select random rows from the CSV
        for row in rows:
            image_name = row['Image']
            image_url = row['ImageURL']
            # Download image
            image_path = download_image(image_url, image_name)
            product = Product.objects.create(
                title=row['ProductTitle'],
                image_path=image_path,
                category=row['Category'],
                type=row['ProductType'],
                price=random.uniform(10, 1000),  # Generate random price
                tags=generate_tags(row['Gender'], row['Category'], row['SubCategory'], row['ProductType'],
                                   row['ProductTitle']),
                vendor=fake.company(),
                description=fake.text(),
            )
            # Add colors to the product
            num_colors = random.randint(0, len(available_colors))
            colors = random.sample(available_colors, num_colors)
            for color in colors:
                color_obj, _ = Color.objects.get_or_create(name=color)
                product.colors.add(color_obj)


def generate_fake_question_and_answers():
    users = CustomUser.objects.all()
    products = Product.objects.all()
    for product in products:
        for _ in range(5):  # Generate 5 questions for each product
            user = fake.random_element(users)
            question_text = fake.text()
            anonymous = fake.boolean(chance_of_getting_true=50)  # Randomly set as anonymous
            question = ProductQuestion.objects.create(
                product=product,
                user=user,
                question=question_text,
                likes=fake.random_int(0, 10),
                dislikes=fake.random_int(0, 10),
                created_at=timezone.now(),
                anonymous=anonymous
            )

            for _ in range(3):  # Generate 3 answers for each question
                user = fake.random_element(users)
                answer_text = fake.text()
                anonymous = fake.boolean(chance_of_getting_true=50)  # Randomly set as anonymous
                ProductAnswer.objects.create(
                    question=question,
                    user=user,
                    answer=answer_text,
                    likes=fake.random_int(0, 10),
                    dislikes=fake.random_int(0, 10),
                    created_at=timezone.now(),
                    anonymous=anonymous
                )
