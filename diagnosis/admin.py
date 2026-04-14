from django.contrib import admin
from .models import DiagnosticModule, DiagnosisRecord


@admin.register(DiagnosticModule)
class DiagnosticModuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'model_filename', 'created_at']
    list_filter = ['is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(DiagnosisRecord)
class DiagnosisRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'module', 'predicted_class', 'confidence', 'created_at']
    list_filter = ['module', 'created_at']
    search_fields = ['user__username', 'predicted_class']
    readonly_fields = ['created_at']
