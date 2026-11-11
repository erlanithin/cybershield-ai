import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import MessageAnalysis, Feedback
from .forms import SingleMessageForm, BatchMessageForm, CSVUploadForm, FeedbackForm, ReviewStatusForm
from .services import (
    process_and_save_analysis,
    process_batch_lines,
    process_uploaded_file,
    get_dashboard_analytics,
    generate_csv_response
)
from ml_engine.evaluate import get_model_metrics
from reports.models import CyberbullyingReport


def home_view(request):
    """
    Renders the CyberShield AI landing page with dynamic statistics,
    live recent detections, and interactive preview.
    """
    recent_detections = MessageAnalysis.objects.all()[:6]
    metrics = get_model_metrics()

    context = {
        'recent_detections': recent_detections,
        'model_metrics': metrics,
    }
    return render(request, 'home.html', context)


def detection_view(request):
    """
    Interactive text detection interface. Supports standard form submission
    and pre-populates sample test cases for user convenience.
    """
    result = None
    sample_texts = [
        "Hey, this tutorial was very helpful and well-structured, thank you!",
        "Why are you even here? Nobody likes you or wants you around. Delete your account loser.",
        "I will find where you live and beat you bloody tonight. Sleep with one eye open.",
        "You look like a disgusting, fat, hideous pig. Nobody could ever love you.",
        "All immigrants of your race are filthy subhuman parasites and should be wiped out.",
        "Shut your fucking mouth you absolute piece of shit, go drown in acid.",
        "Send your private naked pictures right now or I will leak your contacts online."
    ]

    if request.method == 'POST':
        form = SingleMessageForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['message']
            result = process_and_save_analysis(text, user=request.user)
            if not result.get('success'):
                messages.error(request, result.get('error', "Analysis failed."))
    else:
        sample_q = request.GET.get('sample')
        initial_text = sample_q if sample_q else ''
        form = SingleMessageForm(initial={'message': initial_text})
        if initial_text:
            result = process_and_save_analysis(initial_text, user=request.user)

    feedback_form = FeedbackForm()

    context = {
        'form': form,
        'result': result,
        'sample_texts': sample_texts,
        'feedback_form': feedback_form,
    }
    return render(request, 'detection.html', context)


def api_analyze(request):
    """
    Real-time JSON REST API endpoint for instantaneous AJAX message analysis.
    URL: /api/analyze/
    Method: POST
    Payload: {"message": "text"} or form-data
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed. Use POST.'}, status=405)

    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
            text = data.get('message', '').strip()
        else:
            text = request.POST.get('message', '').strip()

        if not text:
            return JsonResponse({'success': False, 'error': 'Message parameter is required and cannot be empty.'}, status=400)

        result = process_and_save_analysis(text, user=request.user if request.user.is_authenticated else None)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def batch_detection_view(request):
    """
    Batch analysis for multiple messages either pasted line-by-line
    or uploaded via a CSV/TXT dataset file.
    """
    text_form = BatchMessageForm()
    csv_form = CSVUploadForm()
    batch_results = None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'text_batch':
            text_form = BatchMessageForm(request.POST)
            if text_form.is_valid():
                raw_text = text_form.cleaned_data.get('messages_text', '')
                lines = raw_text.splitlines()
                batch_results = process_batch_lines(lines, user=request.user)
                messages.success(request, f"Analyzed {batch_results['stats']['total']} messages successfully.")
        elif action == 'csv_batch':
            csv_form = CSVUploadForm(request.POST, request.FILES)
            if csv_form.is_valid():
                file_obj = csv_form.cleaned_data.get('csv_file')
                if file_obj:
                    batch_results = process_uploaded_file(file_obj, user=request.user)
                    messages.success(request, f"Processed {batch_results['stats']['total']} messages from {file_obj.name}.")

    context = {
        'text_form': text_form,
        'csv_form': csv_form,
        'batch_results': batch_results,
    }
    return render(request, 'batch_detection.html', context)


def dashboard_view(request):
    """
    Comprehensive Admin / Moderator Analytics Dashboard.
    Visualizes real-time metrics, risk distribution, trends, and provides
    moderation table controls (search, filter, pagination, review status updates).
    """
    analytics = get_dashboard_analytics()

    # Queryset for detection history table
    queryset = MessageAnalysis.objects.all()

    # Filters
    q = request.GET.get('q', '').strip()
    if q:
        queryset = queryset.filter(original_text__icontains(q))

    risk = request.GET.get('risk', '').strip()
    if risk:
        queryset = queryset.filter(risk_level=risk)

    category = request.GET.get('category', '').strip()
    if category:
        queryset = queryset.filter(predicted_category=category)

    status = request.GET.get('status', '').strip()
    if status:
        queryset = queryset.filter(review_status=status)

    # Pagination
    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Distinct categories for filter dropdown
    categories_list = [
        "Normal / Safe",
        "Harassment",
        "Hate Speech",
        "Threatening Language",
        "Personal Attack",
        "Sexual Harassment",
        "Toxic / Abusive Language"
    ]

    total_reports = CyberbullyingReport.objects.count()
    pending_reports = CyberbullyingReport.objects.filter(status='Pending').count()

    context = {
        'analytics': analytics,
        'page_obj': page_obj,
        'total_count': queryset.count(),
        'categories_list': categories_list,
        'filter_q': q,
        'filter_risk': risk,
        'filter_category': category,
        'filter_status': status,
        'total_reports': total_reports,
        'pending_reports': pending_reports,
    }
    return render(request, 'dashboard.html', context)


@login_required
def user_dashboard_view(request):
    """Personal moderation and analysis history for the logged-in user."""
    user_analyses = MessageAnalysis.objects.filter(user=request.user)
    paginator = Paginator(user_analyses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user_reports = CyberbullyingReport.objects.filter(user=request.user)[:5]

    total = user_analyses.count()
    harmful = user_analyses.filter(risk_level__in=['Potentially Harmful', 'High-Risk Content']).count()
    safe = user_analyses.filter(risk_level='Safe').count()

    context = {
        'page_obj': page_obj,
        'user_reports': user_reports,
        'total': total,
        'harmful': harmful,
        'safe': safe,
    }
    return render(request, 'user_dashboard.html', context)


def model_analytics_view(request):
    """
    Displays true machine learning performance metrics, comparison table,
    and confusion matrix.
    """
    metrics = get_model_metrics()
    return render(request, 'model_analytics.html', {'metrics': metrics})


def export_csv_view(request):
    """Exports detection records as CSV with optional query filters."""
    queryset = MessageAnalysis.objects.all()

    q = request.GET.get('q', '').strip()
    if q:
        queryset = queryset.filter(original_text__icontains(q))

    risk = request.GET.get('risk', '').strip()
    if risk:
        queryset = queryset.filter(risk_level=risk)

    category = request.GET.get('category', '').strip()
    if category:
        queryset = queryset.filter(predicted_category=category)

    return generate_csv_response(queryset, filename='cybershield_detection_records.csv')


def update_review_status(request, pk):
    """Updates review status of a detection record."""
    if request.method == 'POST':
        analysis = get_object_or_404(MessageAnalysis, pk=pk)
        new_status = request.POST.get('review_status')
        if new_status in dict(MessageAnalysis.REVIEW_STATUS_CHOICES):
            analysis.review_status = new_status
            analysis.save()
            messages.success(request, f"Updated record #{analysis.id} to '{analysis.get_review_status_display()}'.")
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


def submit_feedback(request):
    """AJAX / Form endpoint to save user feedback on detection accuracy."""
    if request.method == 'POST':
        analysis_id = request.POST.get('analysis_id')
        feedback_type = request.POST.get('feedback_type')
        suggested_category = request.POST.get('suggested_category', '')
        comments = request.POST.get('comments', '')

        analysis = get_object_or_404(MessageAnalysis, pk=analysis_id)
        Feedback.objects.create(
            user=request.user if request.user.is_authenticated else None,
            analysis=analysis,
            feedback_type=feedback_type,
            suggested_category=suggested_category,
            comments=comments
        )

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Thank you! Your feedback helps calibrate our AI models.'})

        messages.success(request, "Feedback submitted successfully. Thank you for helping improve CyberShield AI!")
        return redirect(request.META.get('HTTP_REFERER', 'detection'))

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)
