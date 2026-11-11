from django.contrib import admin
from .models import CyberbullyingReport


@admin.register(CyberbullyingReport)
class CyberbullyingReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'platform', 'category', 'status', 'user', 'created_at')
    list_filter = ('status', 'platform', 'category', 'created_at')
    search_fields = ('title', 'offensive_message', 'description')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')
