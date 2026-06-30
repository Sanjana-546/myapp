from django.contrib.admin import AdminSite
from django.db.models import Count, Sum
from django.shortcuts import render

from .models import Post


class InkspireAdminSite(AdminSite):
    site_header = 'Inkspire Admin'
    site_title = 'Inkspire Admin'
    index_title = 'Post reach dashboard'

    def index(self, request, extra_context=None):
        from django.shortcuts import redirect
        return redirect('blog:admin_dashboard')
