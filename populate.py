import os, django, random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from faker import Faker
from blog.models import Post
from django.contrib.auth.models import User
from django.utils import timezone

def create_posts(n):
    fake = Faker()
    for i in range(n):
        id = random.randint(1,4)
        status = random.choice(['published','draft'])
        title=fake.name()
        
        Post.objects.create(
        title=title,
        author=User.objects.get(id=id),
        slug = '-'.join(title.lower().split()),
        content=fake.text(),
        created_date = timezone.now(),
        update_date = timezone.now()
        )

create_posts(10)
print("populated")