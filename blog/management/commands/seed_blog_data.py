from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from blog.models import Post

User = get_user_model()

ADMIN_USERNAME = 'admin'
ADMIN_EMAIL = 'admin@example.com'
ADMIN_PASSWORD = 'Admin@12345'

SAMPLE_POSTS = [
    {
        'title': 'Getting Started with Django',
        'slug': 'getting-started-with-django',
        'content': (
            'Django is a high-level Python web framework that encourages rapid development. '
            'This post covers project setup, apps, models, and the admin site.'
        ),
    },
    {
        'title': 'Understanding URL Routing',
        'slug': 'understanding-url-routing',
        'content': (
            'URL routing maps browser requests to view functions. '
            'Use path() and include() to organize routes across apps.'
        ),
    },
    {
        'title': 'Building a Blog App',
        'slug': 'building-a-blog-app',
        'content': (
            'A blog app typically includes Post models, list/detail views, '
            'templates, and admin registration for content management.'
        ),
    },
]


class Command(BaseCommand):
    help = 'Create admin user and sample blog posts'

    def handle(self, *args, **options):
        admin_user, created = User.objects.get_or_create(
            username=ADMIN_USERNAME,
            defaults={'email': ADMIN_EMAIL, 'is_staff': True, 'is_superuser': True},
        )
        if created:
            admin_user.set_password(ADMIN_PASSWORD)
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(
                f'Created admin user "{ADMIN_USERNAME}" with password "{ADMIN_PASSWORD}"'
            ))
        else:
            admin_user.set_password(ADMIN_PASSWORD)
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            self.stdout.write(self.style.WARNING(
                f'Admin user "{ADMIN_USERNAME}" already exists. Password reset to "{ADMIN_PASSWORD}"'
            ))

        for post_data in SAMPLE_POSTS:
            post, post_created = Post.objects.get_or_create(
                slug=post_data['slug'],
                defaults={
                    'title': post_data['title'],
                    'content': post_data['content'],
                    'author': admin_user,
                    'published': True,
                },
            )
            if post_created:
                self.stdout.write(self.style.SUCCESS(f'Created post: {post.title}'))
            else:
                self.stdout.write(f'Post already exists: {post.title}')

        self.stdout.write(self.style.SUCCESS('Database seeding complete.'))
        self.stdout.write('Admin login: http://127.0.0.1:8000/admin/')
        self.stdout.write(f'Username: {ADMIN_USERNAME}')
        self.stdout.write(f'Password: {ADMIN_PASSWORD}')
