"""
Views for the medical diagnosis application.
"""
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.http import JsonResponse
from .models import DiagnosticModule, DiagnosisRecord
from .forms import ImageUploadForm
from .ml import predictor


def dashboard(request):
    """Main dashboard with module cards and analytics."""
    modules = DiagnosticModule.objects.filter(is_active=True)
    
    context = {
        'modules': modules,
        'page_title': 'Dashboard',
    }
    
    if request.user.is_authenticated:
        user_records = DiagnosisRecord.objects.filter(user=request.user)
        recent_records = user_records[:5]
        total_diagnoses = user_records.count()
        
        # Per-module stats
        module_stats = user_records.values('module__name').annotate(
            count=Count('id'),
            avg_confidence=Avg('confidence')
        ).order_by('-count')
        
        context.update({
            'recent_records': recent_records,
            'total_diagnoses': total_diagnoses,
            'module_stats': module_stats,
        })
    
    return render(request, 'diagnosis/dashboard.html', context)


@login_required
def diagnose(request, slug):
    """Upload page for a specific diagnostic module."""
    module = get_object_or_404(DiagnosticModule, slug=slug, is_active=True)
    
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            notes = form.cleaned_data.get('notes', '')
            
            # Run prediction
            result = predictor.predict(module, image)
            
            if result['success']:
                # Save record
                record = DiagnosisRecord(
                    user=request.user,
                    module=module,
                    image=image,
                    predicted_class=result['predicted_class'],
                    confidence=result['confidence'],
                    all_predictions_json=json.dumps(result['all_predictions']),
                    notes=notes,
                )
                record.save()
                
                return redirect('diagnosis:result', pk=record.pk)
            else:
                messages.error(request, f"Prediction failed: {result.get('error', 'Unknown error')}")
    else:
        form = ImageUploadForm()
    
    context = {
        'module': module,
        'form': form,
        'page_title': f'Diagnose — {module.name}',
    }
    return render(request, 'diagnosis/diagnose.html', context)


@login_required
def result(request, pk):
    """Display prediction results."""
    record = get_object_or_404(DiagnosisRecord, pk=pk, user=request.user)
    
    # Prepare data for chart
    predictions = record.all_predictions
    chart_labels = list(predictions.keys())
    chart_values = list(predictions.values())
    
    context = {
        'record': record,
        'chart_labels': json.dumps(chart_labels),
        'chart_values': json.dumps(chart_values),
        'page_title': f'Result — {record.module.name}',
    }
    return render(request, 'diagnosis/result.html', context)


@login_required
def history(request):
    """Paginated list of past diagnoses."""
    records = DiagnosisRecord.objects.filter(user=request.user).select_related('module')
    
    # Filter by module
    module_slug = request.GET.get('module')
    if module_slug:
        records = records.filter(module__slug=module_slug)
    
    paginator = Paginator(records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    modules = DiagnosticModule.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'modules': modules,
        'current_module': module_slug,
        'total_records': records.count(),
        'page_title': 'Diagnosis History',
    }
    return render(request, 'diagnosis/history.html', context)


def about(request):
    """About page with project info and medical disclaimer."""
    modules = DiagnosticModule.objects.filter(is_active=True)
    context = {
        'modules': modules,
        'page_title': 'About',
    }
    return render(request, 'diagnosis/about.html', context)
