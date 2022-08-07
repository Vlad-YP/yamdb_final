import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title

User = get_user_model()

CHOICES = {
    'category': Category,
    'genre': Genre,
    'title': Title,
    'genretitle': GenreTitle,
    'review': Review,
    'comment': Comment,
    'user': User,
}


class Command(BaseCommand):
    help = 'Uploads .csv to specified model'

    def add_arguments(self, parser):
        parser.add_argument('model', type=str)
        parser.add_argument('path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        model_kwargs = kwargs['model']
        model = CHOICES[model_kwargs]
        try:
            with open(path, 'rt', encoding='utf-8') as f:
                reader = csv.reader(f, dialect='excel')
                next(reader)
                print(f'Model is {model_kwargs}, path is {path}')
                for row in reader:
                    print('    ', *row)
                    if model != User:
                        tablespace = model(*row)
                        tablespace.save()
                    else:
                        tablespace = model.objects.create(
                            id=row[0],
                            username=row[1],
                            email=row[2],
                            role=row[3],
                            bio=row[4],
                            first_name=row[5],
                            last_name=row[6],
                        )
        except Exception as error:
            print(error)
