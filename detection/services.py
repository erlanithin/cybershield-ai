"""
CyberShield AI - Detection Services
Handles business logic for single and batch message inference, database persistence,
CSV generation, and analytics aggregation.
"""
import io
import csv
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
from django.http import HttpResponse

from .models import MessageAnalysis
from ml_engine.predict import predict_message


def process_and_save_analysis(text: str, user=None, is_batch: bool = False) -> dict:
    """
    Performs AI prediction on text and persists the result to MessageAnalysis model.
    """
    result = predict_message(text)
    if not result.get('success'):
        return result

    analysis = MessageAnalysis.objects.create(
        user=user if user and user.is_authenticated else None,
        original_text=result['original_text'],
        cleaned_text=result['cleaned_text'],
        predicted_category=result['predicted_category'],
        confidence_score=result['confidence_score'],
        risk_level=result['risk_level'],
        explanation=result['explanation'],
        trigger_words=result['trigger_words'],
        probabilities=result['probabilities'],
        is_batch=is_batch,
        review_status='unreviewed'
    )

    result['id'] = analysis.id
    result['created_at'] = analysis.created_at.strftime('%Y-%m-%d %H:%M')
    return result


def process_batch_lines(lines: list, user=None) -> dict:
    """
    Processes a list of raw text lines in batch and returns individual items plus aggregate stats.
    """
    items = []
    stats = {
        'total': 0,
        'safe': 0,
        'warning': 0,
        'high_risk': 0,
        'categories': {}
    }

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        res = process_and_save_analysis(stripped, user=user, is_batch=True)
        if res.get('success'):
            items.append(res)
            stats['total'] += 1

            risk = res['risk_level']
            if risk == 'Safe':
                stats['safe'] += 1
            elif risk == 'High-Risk Content':
                stats['high_risk'] += 1
            else:
                stats['warning'] += 1

            cat = res['predicted_category']
            stats['categories'][cat] = stats['categories'].get(cat, 0) + 1

    return {
        'items': items,
        'stats': stats
    }


def process_uploaded_file(file_obj, user=None) -> dict:
    """
    Reads an uploaded .csv or .txt file and processes text entries.
    """
    decoded = file_obj.read().decode('utf-8', errors='ignore')
    lines = []

    if file_obj.name.endswith('.csv'):
        reader = csv.reader(io.StringIO(decoded))
        header = None
        target_col = 0
        for i, row in enumerate(reader):
            if not row:
                continue
            if i == 0:
                header = [c.strip().lower() for c in row]
                # Try finding relevant column name
                for col_name in ['text', 'message', 'comment', 'content', 'tweet']:
                    if col_name in header:
                        target_col = header.index(col_name)
                        break
                continue
            if len(row) > target_col:
                val = row[target_col].strip()
                if val:
                    lines.append(val)
    else:
        # Plain text line by line
        for line in decoded.splitlines():
            if line.strip():
                lines.append(line.strip())

    return process_batch_lines(lines, user=user)


def get_dashboard_analytics() -> dict:
    """
    Calculates comprehensive analytics for Admin and Moderator dashboards.
    """
    now = timezone.now()
    seven_days_ago = now - timedelta(days=6)

    total_analyses = MessageAnalysis.objects.count()
    safe_analyses = MessageAnalysis.objects.filter(risk_level='Safe').count()
    warning_analyses = MessageAnalysis.objects.filter(risk_level='Potentially Harmful').count()
    high_risk_analyses = MessageAnalysis.objects.filter(risk_level='High-Risk Content').count()
    harmful_total = warning_analyses + high_risk_analyses

    # Detection percentage
    harmful_pct = round((harmful_total / total_analyses * 100), 1) if total_analyses > 0 else 0.0
    safe_pct = round((safe_analyses / total_analyses * 100), 1) if total_analyses > 0 else 0.0

    # Category breakdown
    category_counts = (
        MessageAnalysis.objects.values('predicted_category')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    categories_labels = [c['predicted_category'] for c in category_counts]
    categories_data = [c['count'] for c in category_counts]

    # Daily detection timeline for past 7 days
    daily_labels = []
    daily_total = []
    daily_harmful = []
    daily_safe = []

    for i in range(7):
        day_date = (seven_days_ago + timedelta(days=i)).date()
        day_name = day_date.strftime('%b %d')
        daily_labels.append(day_name)

        day_queryset = MessageAnalysis.objects.filter(created_at__date=day_date)
        day_count = day_queryset.count()
        day_safe_count = day_queryset.filter(risk_level='Safe').count()
        day_harmful_count = day_queryset.filter(
            risk_level__in=['Potentially Harmful', 'High-Risk Content']
        ).count()

        daily_total.append(day_count)
        daily_safe.append(day_safe_count)
        daily_harmful.append(day_harmful_count)

    return {
        'total_analyses': total_analyses,
        'safe_analyses': safe_analyses,
        'warning_analyses': warning_analyses,
        'high_risk_analyses': high_risk_analyses,
        'harmful_total': harmful_total,
        'harmful_pct': harmful_pct,
        'safe_pct': safe_pct,
        'categories_labels': categories_labels,
        'categories_data': categories_data,
        'daily_labels': daily_labels,
        'daily_total': daily_total,
        'daily_harmful': daily_harmful,
        'daily_safe': daily_safe,
    }


def generate_csv_response(queryset, filename='cybershield_detection_export.csv'):
    """
    Exports a queryset of MessageAnalysis objects as a downloadable CSV.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow([
        'ID',
        'Timestamp',
        'User',
        'Risk Level',
        'Predicted Category',
        'Confidence Score (%)',
        'Trigger Signals',
        'Review Status',
        'Original Message'
    ])

    for obj in queryset:
        writer.writerow([
            obj.id,
            obj.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            obj.user.username if obj.user else 'Anonymous',
            obj.risk_level,
            obj.predicted_category,
            obj.confidence_score,
            ', '.join(obj.trigger_words or []),
            obj.get_review_status_display(),
            obj.original_text.replace('\n', ' ')
        ])

    return response
