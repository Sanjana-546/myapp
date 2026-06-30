from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User

from .admin_site import InkspireAdminSite
from .models import Post

admin_site = InkspireAdminSite(name='admin')


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'view_count', 'published_status', 'created_at')
    list_filter = ('category', 'published', 'created_at', 'author')
    search_fields = ('title', 'content', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    readonly_fields = ('view_count', 'created_at', 'updated_at', 'title', 'slug', 'author', 'category', 'content', 'published')

    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'slug', 'author', 'category'),
        }),
        ('Content', {
            'fields': ('content',),
            'classes': ('wide',),
        }),
        ('Publishing', {
            'fields': ('published', 'view_count'),
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def published_status(self, obj):
        from django.utils.html import format_html
        if obj.published:
            return format_html(
                '<span style="color: #10b981; font-weight: 600;">✓ Published</span>'
            )
        return format_html(
            '<span style="color: #f59e0b; font-weight: 600;">○ Draft</span>'
        )
    published_status.short_description = 'Status'


admin_site.register(Post, PostAdmin)
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
