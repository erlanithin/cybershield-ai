from django import forms
from .models import CyberbullyingReport


class CyberbullyingReportForm(forms.ModelForm):
    class Meta:
        model = CyberbullyingReport
        fields = ['title', 'platform', 'category', 'offensive_message', 'incident_url', 'description', 'evidence_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Repeated threatening DMs on Instagram'}),
            'platform': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'offensive_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Copy-paste the exact message or comments here'}),
            'incident_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://... (optional URL to the post or profile)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe what occurred, any prior history, and how this affected you or the victim'}),
            'evidence_file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ReportStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = CyberbullyingReport
        fields = ['status', 'admin_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'admin_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notes on action taken, warnings issued, or escalations.'}),
        }
