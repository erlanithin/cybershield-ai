"""
CyberShield AI - Context Processors
Provides real-time global statistics and system health indicators to all templates.
"""
from detection.models import MessageAnalysis
from reports.models import CyberbullyingReport
from ml_engine.evaluate import get_model_metrics


def global_stats(request):
    """Provides high-level system metrics for navigation bars, hero headers, and cards."""
    try:
        total_analyzed = MessageAnalysis.objects.count()
        safe_count = MessageAnalysis.objects.filter(risk_level='Safe').count()
        harmful_count = MessageAnalysis.objects.filter(
            risk_level__in=['Potentially Harmful', 'High-Risk Content']
        ).count()
        high_risk_count = MessageAnalysis.objects.filter(risk_level='High-Risk Content').count()
        pending_reports = CyberbullyingReport.objects.filter(status='Pending').count()
        total_reports = CyberbullyingReport.objects.count()

        metrics = get_model_metrics()
        accuracy_pct = round(metrics.get('accuracy', 0.62) * 100, 1)

        return {
            'global_total_analyzed': total_analyzed,
            'global_safe_count': safe_count,
            'global_harmful_count': harmful_count,
            'global_high_risk_count': high_risk_count,
            'global_detection_accuracy': accuracy_pct,
            'global_pending_reports': pending_reports,
            'global_total_reports': total_reports,
            'global_best_model': metrics.get('best_model', 'Logistic Regression'),
        }
    except Exception:
        return {
            'global_total_analyzed': 0,
            'global_safe_count': 0,
            'global_harmful_count': 0,
            'global_high_risk_count': 0,
            'global_detection_accuracy': 62.1,
            'global_pending_reports': 0,
            'global_total_reports': 0,
            'global_best_model': 'Logistic Regression',
        }
