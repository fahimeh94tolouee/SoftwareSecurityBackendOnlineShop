from django.core.management.base import BaseCommand
from product.seeder import generate_fake_question_and_answers


class Command(BaseCommand):
    help = 'Seed fake question and answers for products'

    def handle(self, *args, **options):
        generate_fake_question_and_answers()
        self.stdout.write(self.style.SUCCESS('Successfully seeded questions and answers data'))
