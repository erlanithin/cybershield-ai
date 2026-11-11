from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import CyberbullyingReport
from .forms import CyberbullyingReportForm, ReportStatusUpdateForm


def report_list_view(request):
    """Lists cyberbullying incident reports with status filtering and pagination."""
    reports = CyberbullyingReport.objects.all()

    # User can see only their reports if not staff, unless staff/moderator
    is_staff = request.user.is_authenticated and (
        request.user.is_staff or 
        (hasattr(request.user, 'profile') and request.user.profile.is_moderator_or_admin)
    )

    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        reports = reports.filter(status=status_filter)

    platform_filter = request.GET.get('platform', '').strip()
    if platform_filter:
        reports = reports.filter(platform=platform_filter)

    paginator = Paginator(reports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'platform_filter': platform_filter,
        'is_staff': is_staff,
    }
    return render(request, 'reports.html', context)


def report_create_view(request):
    """Form to submit a new cyberbullying report."""
    if request.method == 'POST':
        form = CyberbullyingReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            if request.user.is_authenticated:
                report.user = request.user
            report.status = 'Pending'
            report.save()
            messages.success(
                request,
                f"Incident Report #{report.id} submitted successfully. Our safety moderation team will investigate."
            )
            return redirect('report_detail', pk=report.id)
    else:
        # Prepopulate offensive message if passed from detection
        initial_msg = request.GET.get('message', '')
        form = CyberbullyingReportForm(initial={'offensive_message': initial_msg})

    return render(request, 'report_create.html', {'form': form})


def report_detail_view(request, pk):
    """Displays incident report details, evidence, and allows status updating for staff."""
    report = get_object_or_404(CyberbullyingReport, pk=pk)

    is_staff = request.user.is_authenticated and (
        request.user.is_staff or 
        (hasattr(request.user, 'profile') and request.user.profile.is_moderator_or_admin)
    )

    update_form = None
    if is_staff:
        if request.method == 'POST':
            update_form = ReportStatusUpdateForm(request.POST, instance=report)
            if update_form.is_valid():
                update_form.save()
                messages.success(request, f"Report #{report.id} status updated to {report.get_status_display()}.")
                return redirect('report_detail', pk=report.id)
        else:
            update_form = ReportStatusUpdateForm(instance=report)

    context = {
        'report': report,
        'is_staff': is_staff,
        'update_form': update_form,
    }
    return render(request, 'report_detail.html', context)
