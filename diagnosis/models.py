import json
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class DiagnosticModule(models.Model):
    """Represents a diagnostic capability (e.g., Chest X-Ray analysis)."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='🔬')  # Emoji icon
    model_filename = models.CharField(max_length=200, help_text='Filename of the .h5 model in ml_models/')
    image_width = models.IntegerField(default=224)
    image_height = models.IntegerField(default=224)
    classes_json = models.TextField(help_text='JSON array of class names')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def classes(self):
        return json.loads(self.classes_json)

    @property
    def num_classes(self):
        return len(self.classes)

    @property
    def image_size(self):
        return (self.image_width, self.image_height)


class DiagnosisRecord(models.Model):
    """Stores each prediction made by the system."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diagnoses')
    module = models.ForeignKey(DiagnosticModule, on_delete=models.CASCADE, related_name='records')
    image = models.ImageField(upload_to='diagnoses/%Y/%m/%d/')
    predicted_class = models.CharField(max_length=100)
    confidence = models.FloatField(help_text='Confidence percentage (0-100)')
    all_predictions_json = models.TextField(
        help_text='JSON object mapping class names to confidence percentages',
        default='{}'
    )
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.module.name} - {self.predicted_class} ({self.confidence:.1f}%) - {self.user.username}"

    @property
    def all_predictions(self):
        return json.loads(self.all_predictions_json)

    @property
    def confidence_color(self):
        """Returns a CSS color class based on confidence level."""
        if self.confidence >= 80:
            return 'high'
        elif self.confidence >= 50:
            return 'medium'
        return 'low'
