import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from blog.models import Post

User = get_user_model()

ADMIN_USERNAME = 'admin'
ADMIN_EMAIL = 'admin@example.com'
ADMIN_PASSWORD = 'Admin@12345'

DEFAULT_USER_PASSWORD = 'BlogUser@123'

SAMPLE_USERS = [
    {
        'username': 'alice',
        'email': 'alice@example.com',
        'first_name': 'Alice',
        'last_name': 'Chen',
        'is_staff': True,
    },
    {
        'username': 'bob',
        'email': 'bob@example.com',
        'first_name': 'Bob',
        'last_name': 'Martinez',
        'is_staff': True,
    },
    {
        'username': 'carol',
        'email': 'carol@example.com',
        'first_name': 'Carol',
        'last_name': 'Nguyen',
        'is_staff': False,
    },
    {
        'username': 'david',
        'email': 'david@example.com',
        'first_name': 'David',
        'last_name': 'Patel',
        'is_staff': False,
    },
]

SAMPLE_POSTS = [
    {
        'title': 'Getting Started with Django',
        'slug': 'getting-started-with-django',
        'author': 'admin',
        'category': 'technology',
        'image_url': 'blog/images/django-start.svg',
        'content': (
            'Django is a high-level Python web framework that encourages rapid development. '
            'This post covers project setup, apps, models, and the admin site. '
            'You will learn how to configure URLs, register models, and structure templates for a maintainable app. '
            'By the end of this guide, you should feel comfortable creating your first Django project from scratch. '
            'The guide includes best practices for organizing code and using Django conventions safely.'
        ),
    },
    {
        'title': 'Understanding URL Routing',
        'slug': 'understanding-url-routing',
        'author': 'admin',
        'category': 'technology',
        'image_url': 'blog/images/url-routing.svg',
        'content': (
            'URL routing maps browser requests to view functions. '
            'Use path() and include() to organize routes across apps. '
            'This post explains how Django resolves paths in the URLconf and how to build reusable route patterns. '
            'It also covers named URLs and reverse resolution for cleaner templates and redirects. '
            'A well-designed URL layer improves maintainability and helps authors avoid hard-coded links.'
        ),
    },
    {
        'title': 'Building a Blog App',
        'slug': 'building-a-blog-app',
        'author': 'admin',
        'category': 'technology',
        'image_url': 'blog/images/blog-app.svg',
        'content': (
            'A blog app typically includes Post models, list/detail views, templates, and admin registration for content management. '
            'This article breaks down how to design models, build views, and render content with template inheritance. '
            'You will also see how to add post categories, author pages, and rich presentation for each entry. '
            'The result is a complete, user-friendly publication experience.'
        ),
    },
    {
        'title': 'Working with Django Templates',
        'slug': 'working-with-django-templates',
        'author': 'alice',
        'category': 'reviews',
        'image_url': 'blog/images/template-workflow.svg',
        'content': (
            'Templates separate presentation from logic. Learn template inheritance, blocks, filters, and how to pass context from views. '
            'This review explores useful filters, custom tags, and performance considerations for complex pages. '
            'It also explains how to design reusable components, such as post cards and author callouts, to keep your frontend consistent.'
        ),
    },
    {
        'title': 'Introduction to Django ORM',
        'slug': 'introduction-to-django-orm',
        'author': 'alice',
        'category': 'technology',
        'image_url': 'blog/images/orm-queries.svg',
        'content': (
            'The ORM lets you query the database using Python instead of SQL. '
            'Explore models, QuerySets, filtering, and relationships. '
            'This detailed introduction also covers related object lookups, prefetching, and optimizing queries to keep your application fast as it grows. '
            'Use these patterns to make your data layer expressive and easy to maintain. '
            'The post includes practical examples for joins, aggregation, and raw SQL when you need it.'
        ),
    },
    {
        'title': 'Deploying Django to Production',
        'slug': 'deploying-django-to-production',
        'author': 'bob',
        'category': 'reviews',
        'image_url': 'blog/images/deployment.svg',
        'content': (
            'Production deployments require static files, environment variables, a WSGI server, and a reverse proxy. '
            'This guide walks through the basics of configuring Django for reliability and security. '
            'It also covers best practices for managing secrets, enabling HTTPS, and avoiding common deployment mistakes. '
            'Proper deployment creates a stable foundation for your application and keeps users happy. '
            'We also highlight monitoring, log aggregation, and environment-specific settings to avoid surprises on launch day.'
        ),
    },
    {
        'title': 'Securing Your Django Application',
        'slug': 'securing-your-django-application',
        'author': 'bob',
        'category': 'reviews',
        'image_url': 'blog/images/security.svg',
        'content': (
            'Use HTTPS, keep DEBUG off in production, validate user input, and follow Django security best practices to protect your app. '
            'This article explains CSRF protection, secure session settings, and password management. '
            'It also reviews how to harden admin access, sanitize user data, and avoid exposure of sensitive information in logs and error output. '
            'We cover common attack vectors, secure headers, and how to limit access to sensitive resources.'
        ),
    },
    {
        'title': 'Writing Effective Unit Tests',
        'slug': 'writing-effective-unit-tests',
        'author': 'carol',
        'category': 'reviews',
        'image_url': 'blog/images/testing.svg',
        'content': (
            'Tests catch regressions early. Use Django TestCase, factories, and focus on behavior rather than implementation details. '
            'This post explains how to write readable tests for views, forms, and models. '
            'It also includes tips for isolating dependencies and keeping suites fast by using in-memory databases and mocks where appropriate. '
            'Good tests make refactoring safer and speed development overall.'
        ),
    },
    {
        'title': 'Customizing the Django Admin',
        'slug': 'customizing-the-django-admin',
        'author': 'carol',
        'category': 'technology',
        'image_url': 'blog/images/admin-customization.svg',
        'content': (
            'Register models with ModelAdmin to control list displays, filters, search fields, and inline editing for a better content workflow. '
            'Learn how to configure fieldsets, add custom actions, and create a cleaner admin experience for authors and editors. '
            'A well-customized admin can dramatically reduce the time needed to manage published content and users. '
            'This post also covers list display customization, ordering rules, and how to surface the most important fields to editors.'
        ),
    },
    {
        'title': 'Handling Forms and User Input',
        'slug': 'handling-forms-and-user-input',
        'author': 'david',
        'category': 'technology',
        'image_url': 'blog/images/forms.svg',
        'content': (
            'Django forms handle validation and rendering. Combine forms with views to process POST data safely and provide helpful error messages. '
            'This post walks through custom validators, formsets, and handling file uploads. '
            'It also highlights how to preserve user input on error and keep your UI accessible for everyone. '
            'You will learn how to structure reusable form components and integrate them with templates cleanly.'
        ),
    },
    {
        'title': 'Caching Strategies for Faster Pages',
        'slug': 'caching-strategies-for-faster-pages',
        'author': 'david',
        'category': 'technology',
        'image_url': 'blog/images/caching.svg',
        'content': (
            'Page caching, template fragment caching, and low-level cache APIs can dramatically reduce database load for read-heavy applications. '
            'This post compares cache backends and demonstrates when to cache queries versus whole views. '
            'It also explains cache invalidation patterns and how to keep fresh content without sacrificing performance. '
            'You will learn how to choose between Redis, Memcached, and local-memory caching based on your deployment scenario.'
        ),
    },
    {
        'title': 'REST APIs with Django REST Framework',
        'slug': 'rest-apis-with-django-rest-framework',
        'author': 'alice',
        'category': 'technology',
        'image_url': 'blog/images/drf.svg',
        'content': (
            'DRF adds serializers, viewsets, and browsable APIs on top of Django. '
            'It is a popular choice for building JSON endpoints. '
            'This article shows how to expose models with serializers, handle nested data, and add authentication to your API. '
            'Learn how to use routers and mixins to keep API code clean and maintainable. '
            'You will also see how to test endpoints and version APIs for long-term compatibility.'
        ),
    },
    {
        'title': 'Easy One-Pot Cooking Ideas',
        'slug': 'easy-one-pot-cooking-ideas',
        'author': 'alice',
        'category': 'cooking',
        'image_url': 'blog/images/cooking-photo.png',
        'content': (
            'One-pot meals are perfect for busy weeknights. Use seasonal produce, simple spices, and minimal cleanup for tasty dinners. '
            'This article includes several recipes for pasta, rice, and stews that can be made in a single pot. '
            'You will also learn how to layer flavors and keep prep time under 30 minutes while still serving a satisfying meal.'
        ),
    },
    {
        'title': 'Weekend Brunch Recipes',
        'slug': 'weekend-brunch-recipes',
        'author': 'bob',
        'category': 'cooking',
        'image_url': 'blog/images/cooking-photo.png',
        'content': (
            'Weekend brunch is a great way to relax and enjoy fresh flavors. '
            'From fluffy pancakes to savory egg bakes, these recipes are easy to follow and perfect for sharing. '
            'Learn how to make classic brunch dishes with a twist, plus tips for plating and pairing with coffee or juice.'
        ),
    },
    {
        'title': 'Sheet Pan Comfort Foods',
        'slug': 'sheet-pan-comfort-foods',
        'author': 'carol',
        'category': 'cooking',
        'image_url': 'blog/images/cooking-photo.png',
        'content': (
            'Sheet pan meals simplify dinner without sacrificing flavor. '
            'Roast vegetables, proteins, and herbs together for an easy, one-tray dinner. '
            'This post includes seasoning ideas, timing tricks, and a meal-prep version for busy families.'
        ),
    },
    {
        'title': 'The Joy of Home Baking',
        'slug': 'the-joy-of-home-baking',
        'author': 'david',
        'category': 'cooking',
        'image_url': 'blog/images/cooking-photo.png',
        'content': (
            'Baking at home can be calming and rewarding. Learn how to make bread, cookies, and simple pastries from scratch. '
            'This post walks through equipment basics, timing, and common troubleshooting tips. '
            'You will also discover how to customize sweet and savory bakes to suit your pantry.'
        ),
    },
    {
        'title': 'Weekend Travel Essentials',
        'slug': 'weekend-travel-essentials',
        'author': 'bob',
        'category': 'travel',
        'image_url': 'blog/images/travel-packing.svg',
        'content': (
            'A successful travel weekend starts with a lightweight bag, strong plans, and easy-to-pack items that keep you comfortable on the go. '
            'This post covers must-have travel gear, itinerary tips, and how to choose flexible accommodations. '
            'It is ideal for short trips when you want to maximize time and minimize stress.'
        ),
    },
    {
        'title': 'Minimalist Lifestyle Habits',
        'slug': 'minimalist-lifestyle-habits',
        'author': 'david',
        'category': 'lifestyle',
        'image_url': 'blog/images/lifestyle-photo.png',
        'content': (
            'Minimalism is about intentional living. Learn how to simplify routines, clear clutter, and focus on what matters most. '
            'This long-form post guides you through decluttering, batching tasks, and creating a calm daily rhythm. '
            'Use these habits to create more space, energy, and creative freedom in your home.'
        ),
    },
    {
        'title': 'Morning Routines for Better Focus',
        'slug': 'morning-routines-for-better-focus',
        'author': 'alice',
        'category': 'lifestyle',
        'image_url': 'blog/images/lifestyle-photo.png',
        'content': (
            'A mindful morning routine can set the tone for a productive day. '
            'This post explores journaling, light movement, and digital boundaries to help you start strong. '
            'It also provides scheduling ideas for both slow mornings and busy days, so you can find a routine that fits your life.'
        ),
    },
    {
        'title': 'Home Theater Setup Guide',
        'slug': 'home-theater-setup-guide',
        'author': 'carol',
        'category': 'entertainment',
        'image_url': 'blog/images/home-theater.svg',
        'content': (
            'Turn your living room into a movie night destination with smart speaker placement, cozy seating, and optimal screen calibration. '
            'This long guide covers audio tuning, lighting control, and choosing the right streaming gear. '
            'It also includes tips for building a watchlist and hosting an immersive viewing experience.'
        ),
    },
    {
        'title': 'Streaming Service Show Reviews',
        'slug': 'streaming-service-show-reviews',
        'author': 'bob',
        'category': 'entertainment',
        'image_url': 'blog/images/streaming.svg',
        'content': (
            'This post reviews current favorites on streaming platforms and explains what makes each show worth watching. '
            'From comedy to drama, it highlights standout storylines, performances, and binge-worthiness. '
            'Use this curated list to decide your next weekend watch without the endless scrolling.'
        ),
    },
    {
        'title': 'Tech Gadgets for Home Entertainment',
        'slug': 'tech-gadgets-for-home-entertainment',
        'author': 'carol',
        'category': 'entertainment',
        'image_url': 'blog/images/entertainment-gadgets.svg',
        'content': (
            'Modern home entertainment blends audio, video, and smart devices. '
            'This review covers projectors, speakers, and streaming players that boost your at-home cinema. '
            'It also discusses setup tips for small apartments and multi-purpose living spaces.'
        ),
    },
    {
        'title': 'Top Kitchen Gadgets Reviewed',
        'slug': 'top-kitchen-gadgets-reviewed',
        'author': 'alice',
        'category': 'reviews',
        'image_url': 'blog/images/kitchen-gadget-review.svg',
        'content': (
            'From air fryers to smart blenders, this review covers kitchen gadgets that make cooking easier and more enjoyable. '
            'It compares build quality, ease of cleaning, and whether each tool is worth the shelf space. '
            'Whether you are a beginner cook or a seasoned foodie, you will find useful recommendations here.'
        ),
    },
]

class Command(BaseCommand):
    help = 'Create admin user, additional users, and sample blog posts'

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

        users_by_username = {ADMIN_USERNAME: admin_user}

        for user_data in SAMPLE_USERS:
            user, user_created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'is_staff': user_data['is_staff'],
                },
            )
            user.set_password(DEFAULT_USER_PASSWORD)
            user.email = user_data['email']
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.is_staff = user_data['is_staff']
            user.save()

            users_by_username[user.username] = user
            if user_created:
                self.stdout.write(self.style.SUCCESS(
                    f'Created user "{user.username}" with password "{DEFAULT_USER_PASSWORD}"'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'User "{user.username}" already exists. Password reset to "{DEFAULT_USER_PASSWORD}"'
                ))

        for post_data in SAMPLE_POSTS:
            author = users_by_username[post_data['author']]

            # Ensure longer, richer content for each seeded post
            def make_long(content):
                extra = (
                    'This article continues with in-depth explanations, practical examples, and suggestions for further reading. '
                    'It expands on the original topic with step-by-step guides, real-world tips, and references to related concepts. '
                    'Readers will find takeaways they can apply immediately and ideas for deeper exploration.'
                )
                return content + '\n\n' + extra + '\n\n' + extra

            POST_IMAGE_OVERRIDES = {
                'easy-one-pot-cooking-ideas': 'blog/images/cooking-photo-1.png',
                'weekend-brunch-recipes': 'blog/images/recipe-2.png',
                'sheet-pan-comfort-foods': 'blog/images/recipe-1.png',
                'the-joy-of-home-baking': 'blog/images/cooking-photo-2.png',
                'minimalist-lifestyle-habits': 'blog/images/lifestyle-photo-1.png',
                'morning-routines-for-better-focus': 'blog/images/lifestyle-photo-2.png',
                'weekend-travel-essentials': 'blog/images/travel-photo-1.png',
                'streaming-service-show-reviews': 'blog/images/entertainment-photo-1.png',
                'tech-gadgets-for-home-entertainment': 'blog/images/tech-photo-1.png',
                'top-kitchen-gadgets-reviewed': 'blog/images/reviews-photo-1.png',
            }

            long_content = make_long(post_data['content'])
            chosen_image = POST_IMAGE_OVERRIDES.get(post_data['slug'], post_data.get('image_url', 'blog/images/default.svg'))
            view_count = post_data.get('view_count', random.randint(12, 240))

            defaults = {
                'title': post_data['title'],
                'content': long_content,
                'author': author,
                'category': post_data['category'],
                'image_url': chosen_image,
                'published': True,
                'view_count': view_count,
            }

            post, post_created = Post.objects.get_or_create(
                slug=post_data['slug'],
                defaults=defaults,
            )
            if post_created:
                self.stdout.write(self.style.SUCCESS(
                    f'Created post: {post.title} (by {author.username})'
                ))
            else:
                post.title = defaults['title']
                post.content = defaults['content']
                post.author = defaults['author']
                post.category = defaults['category']
                post.image_url = defaults['image_url']
                post.published = defaults['published']
                post.view_count = defaults['view_count']
                post.save()
                self.stdout.write(self.style.WARNING(
                    f'Updated post: {post.title} (by {author.username})'
                ))

        self.stdout.write(self.style.SUCCESS('Database seeding complete.'))
        self.stdout.write('Admin login: http://127.0.0.1:8000/admin/')
        self.stdout.write(f'Admin — username: {ADMIN_USERNAME}, password: {ADMIN_PASSWORD}')
        self.stdout.write('Author login: http://127.0.0.1:8000/blog/login/')
        self.stdout.write(f'Authors — password: {DEFAULT_USER_PASSWORD}')
        for username in sorted(users_by_username):
            if username != ADMIN_USERNAME:
                self.stdout.write(f'  - {username}')
