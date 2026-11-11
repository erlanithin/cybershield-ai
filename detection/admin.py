from django.contrib import admin
from .models import MessageAnalysis, Feedback


@admin.register(MessageAnalysis)
class MessageAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'predicted_category', 'risk_level', 'confidence_score', 'review_status', 'user', 'created_at')
    list_filter = ('risk_level', 'predicted_category', 'review_status', 'is_batch', 'created_at')
    search_fields = ('original_text', 'predicted_category', 'explanation')
    readonly_fields = ('created_at', 'cleaned_text', 'trigger_words', 'probabilities')
    list_editable = ('review_status',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'analysis', 'feedback_type', 'suggested_category', 'user', 'created_at')
    list_filter = ('feedback_type', 'created_at')
    search_fields = ('comments', 'suggested_category')
