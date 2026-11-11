from django import forms
from .models import Feedback, MessageAnalysis


class SingleMessageForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Type or paste a social media comment, chat message, or post here...',
            'id': 'message-input',
            'required': 'required'
        }),
        label="Message to Analyze"
    )


class BatchMessageForm(forms.Form):
    messages_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'placeholder': 'Enter multiple messages, one per line:\nExample 1: You are awesome and helpful!\nExample 2: Delete your account loser, nobody likes you.',
            'id': 'batch-messages-input'
        }),
        label="Enter Messages (One Per Line)",
        required=False
    )


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'id': 'csv-file-input',
            'accept': '.csv, .txt'
        }),
        label="Upload CSV or TXT File",
        required=False
    )

    def clean_csv_file(self):
        file = self.cleaned_data.get('csv_file')
        if file:
            if not file.name.endswith(('.csv', '.txt')):
                raise forms.ValidationError("Only .csv and .txt files are supported.")
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size exceeds maximum 5MB limit.")
        return file


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_type', 'suggested_category', 'comments']
        widgets = {
            'feedback_type': forms.Select(attrs={'class': 'form-select'}),
            'suggested_category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional: correct category'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional: notes for moderation team'}),
        }


class ReviewStatusForm(forms.ModelForm):
    class Meta:
        model = MessageAnalysis
        fields = ['review_status']
        widgets = {
            'review_status': forms.Select(attrs={'class': 'form-select form-select-sm'}),
        }
