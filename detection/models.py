from django.db import models
from django.contrib.auth.models import User


class MessageAnalysis(models.Model):
    RISK_CHOICES = (
        ('Safe', 'Safe (Normal)'),
        ('Potentially Harmful', 'Potentially Harmful'),
        ('High-Risk Content', 'High-Risk Content'),
    )

    REVIEW_STATUS_CHOICES = (
        ('unreviewed', 'Unreviewed'),
        ('flagged', 'Flagged for Review'),
        ('verified', 'Verified Accurate'),
        ('dismissed', 'Dismissed as False Alarm'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='analyses')
    original_text = models.TextField()
    cleaned_text = models.TextField(blank=True)
    predicted_category = models.CharField(max_length=100)
    confidence_score = models.FloatField(default=0.0)
    risk_level = models.CharField(max_length=50, choices=RISK_CHOICES, default='Safe')
    explanation = models.TextField(blank=True)
    trigger_words = models.JSONField(default=list, blank=True)
    probabilities = models.JSONField(default=dict, blank=True)
    is_batch = models.BooleanField(default=False)
    review_status = models.CharField(max_length=30, choices=REVIEW_STATUS_CHOICES, default='unreviewed')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Message Analysis'
        verbose_name_plural = 'Message Analyses'

    def __str__(self):
        snippet = self.original_text[:40] + "..." if len(self.original_text) > 40 else self.original_text
        return f"[{self.risk_level}] {self.predicted_category}: {snippet}"

    @property
    def badge_class(self):
        if self.risk_level == 'Safe':
            return 'badge-safe'
        elif self.risk_level == 'High-Risk Content':
            return 'badge-high-risk'
        return 'badge-warning'


class Feedback(models.Model):
    FEEDBACK_TYPES = (
        ('accurate', 'Prediction is Accurate'),
        ('false_positive', 'False Positive (Should be Safe)'),
        ('false_negative', 'False Negative (Harmful Missed)'),
        ('incorrect_category', 'Wrong Category Assigned'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedbacks')
    analysis = models.ForeignKey(MessageAnalysis, on_delete=models.CASCADE, related_name='feedbacks')
    feedback_type = models.CharField(max_length=30, choices=FEEDBACK_TYPES)
    suggested_category = models.CharField(max_length=100, blank=True)
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback on #{self.analysis_id} - {self.get_feedback_type_display()}"
