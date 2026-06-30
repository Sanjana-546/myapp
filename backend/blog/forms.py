from django import forms
from django.contrib.auth.models import User

from .models import Comment, Post, UserProfile


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile."""
    
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)
    
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_image', 'website', 'twitter', 'linkedin', 'github', 'instagram', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Tell us about yourself...',
            }),
            'website': forms.URLInput(attrs={'placeholder': 'https://yourwebsite.com'}),
            'twitter': forms.URLInput(attrs={'placeholder': 'https://twitter.com/username'}),
            'linkedin': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/username'}),
            'github': forms.URLInput(attrs={'placeholder': 'https://github.com/username'}),
            'instagram': forms.URLInput(attrs={'placeholder': 'https://instagram.com/username'}),
            'location': forms.TextInput(attrs={'placeholder': 'City, Country'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.instance.user:
            self.instance.user.first_name = self.cleaned_data['first_name']
            self.instance.user.last_name = self.cleaned_data['last_name']
            self.instance.user.email = self.cleaned_data['email']
            if commit:
                self.instance.user.save()
        if commit:
            profile.save()
        return profile


class CommentForm(forms.ModelForm):
    """Form for adding comments to posts."""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write a comment...',
                'class': 'comment-form__textarea'
            })
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'category', 'image', 'content', 'published']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 10,
                'placeholder': 'Write the full post content here...',
            }),
            'title': forms.TextInput(attrs={'placeholder': 'Post title'}),
            'slug': forms.TextInput(attrs={'placeholder': 'post-slug-example'}),
            'category': forms.TextInput(attrs={'placeholder': 'Category (e.g., Lifestyle, Cooking, Technology, or custom)'}),
        }


class AdminPostForm(PostForm):
    class Meta(PostForm.Meta):
        fields = ['title', 'slug', 'author', 'category', 'image', 'content', 'published']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].widget.attrs.update({'class': 'author-select'})


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Choose a username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data
