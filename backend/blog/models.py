from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class UserProfile(models.Model):
    """Extended user profile with additional information."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, help_text='Tell us about yourself')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    website = models.URLField(blank=True, help_text='Your personal website')
    twitter = models.URLField(blank=True, help_text='Twitter profile URL')
    linkedin = models.URLField(blank=True, help_text='LinkedIn profile URL')
    github = models.URLField(blank=True, help_text='GitHub profile URL')
    instagram = models.URLField(blank=True, help_text='Instagram profile URL')
    location = models.CharField(max_length=100, blank=True, help_text='Your location')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_absolute_url(self):
        return reverse('blog:profile', kwargs={'username': self.user.username})


class Post(models.Model):
    CATEGORY_LIFESTYLE = 'lifestyle'
    CATEGORY_COOKING = 'cooking'
    CATEGORY_ENTERTAINMENT = 'entertainment'
    CATEGORY_REVIEWS = 'reviews'
    CATEGORY_TECHNOLOGY = 'technology'
    CATEGORY_TRAVEL = 'travel'

    CATEGORIES = [
        (CATEGORY_LIFESTYLE, 'Lifestyle'),
        (CATEGORY_COOKING, 'Cooking'),
        (CATEGORY_ENTERTAINMENT, 'Entertainment'),
        (CATEGORY_REVIEWS, 'Reviews'),
        (CATEGORY_TECHNOLOGY, 'Technology'),
        (CATEGORY_TRAVEL, 'Travel'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.CharField(max_length=50, default=CATEGORY_LIFESTYLE)
    image = models.ImageField(upload_to='blog/images/', blank=True, null=True)
    published = models.BooleanField(default=True)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'post_id': self.pk})


class Comment(models.Model):
    """Comments on posts."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'


class Like(models.Model):
    """Likes on posts."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')
    
    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'
