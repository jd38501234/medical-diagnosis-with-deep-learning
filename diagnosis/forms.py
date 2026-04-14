from django import forms
from .models import DiagnosticModule


class ImageUploadForm(forms.Form):
    """Form for uploading medical images for diagnosis."""
    image = forms.ImageField(
        label='Select Medical Image',
        help_text='Supported formats: JPEG, PNG. Max size: 10MB.',
        widget=forms.ClearableFileInput(attrs={
            'accept': 'image/*',
            'id': 'image-upload-input',
            'class': 'file-input',
        })
    )
    notes = forms.CharField(
        required=False,
        max_length=500,
        widget=forms.Textarea(attrs={
            'placeholder': 'Optional notes about this image...',
            'rows': 3,
            'class': 'form-textarea',
            'id': 'notes-input',
        })
    )
