from django.db import models
from django.contrib.auth.models import User


class CyberbullyingReport(models.Model):
    PLATFORM_CHOICES = (
        ('Twitter / X', 'Twitter / X'),
        ('Instagram', 'Instagram'),
        ('Facebook', 'Facebook'),
        ('TikTok', 'TikTok'),
        ('Discord', 'Discord'),
        ('Reddit', 'Reddit'),
        ('WhatsApp / Telegram', 'WhatsApp / Telegram'),
        ('YouTube', 'YouTube'),
        ('Other', 'Other Platform'),
    )

    CATEGORY_CHOICES = (
        ('Harassment', 'Harassment'),
        ('Hate Speech', 'Hate Speech'),
        ('Threatening Language', 'Threatening Language'),
        ('Personal Attack', 'Personal Attack'),
        ('Sexual Harassment', 'Sexual Harassment'),
        ('Toxic / Abusive Language', 'Toxic / Abusive Language'),
        ('Cyberstalking', 'Cyberstalking'),
        ('Other Harm', 'Other Harm'),
    )

    STATUS_CHOICES = (
        ('Pending', 'Pending Review'),
        ('Under Review', 'Under Investigation'),
        ('Resolved', 'Resolved & Action Taken'),
        ('Dismissed', 'Dismissed (Insufficient Evidence)'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    title = models.CharField(max_length=255)
    offensive_message = models.TextField(help_text="The offensive or harmful text observed")
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES, default='Other')
    incident_url = models.URLField(blank=True, help_text="Link to public post or profile (optional)")
    description = models.TextField(help_text="Detailed context or circumstances of the incident")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Harassment')
    evidence_file = models.FileField(upload_to='evidence/', blank=True, null=True, help_text="Screenshots or documentation")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    admin_notes = models.TextField(blank=True, help_text="Internal notes added by moderator/admin")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Cyberbullying Report'
        verbose_name_plural = 'Cyberbullying Reports'

    def __str__(self):
        return f"Report #{self.id}: {self.title} ({self.get_status_display()})"

    @property
    def status_badge_class(self):
        mapping = {
            'Pending': 'badge-warning',
            'Under Review': 'badge-info',
            'Resolved': 'badge-safe',
            'Dismissed': 'badge-muted'
        }
        return mapping.get(self.status, 'badge-warning')
