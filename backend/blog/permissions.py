"""Role-based access control helpers for the blog."""


def is_site_admin(user):
    return user.is_authenticated and user.is_staff


def can_view_post(user, post):
    if post.published:
        return True
    return user_can_manage_post(user, post)


def user_can_manage_post(user, post):
    if not user.is_authenticated:
        return False
    if is_site_admin(user):
        return False  # Admins cannot edit posts, only view and delete
    return post.author_id == user.id


def user_can_delete_post(user, post):
    if not user.is_authenticated:
        return False
    if is_site_admin(user):
        return True  # Admins can delete any post
    return post.author_id == user.id


def get_manageable_posts(user):
    from .models import Post

    if not user.is_authenticated:
        return Post.objects.none()
    if is_site_admin(user):
        return Post.objects.all()
    return Post.objects.filter(author=user)
