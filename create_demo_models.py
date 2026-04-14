"""
Demo Model Generator for MedDiag AI.

Creates lightweight placeholder models for each diagnostic module
and seeds the database with DiagnosticModule entries.

Usage:
    python create_demo_models.py

Note: These models are NOT trained on real data.
They will produce random predictions for demonstration purposes.
Replace them with properly trained models for real-world use.
"""
import os
import sys
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meddiag.settings')

import django
django.setup()

from django.conf import settings
from diagnosis.models import DiagnosticModule


# Module definitions
MODULES = [
    {
        'name': 'Chest X-Ray Analysis',
        'slug': 'chest-xray',
        'icon': '🫁',
        'description': 'Analyze chest X-ray images to detect signs of pneumonia. The model classifies images as Normal or showing indicators of Pneumonia, leveraging deep learning trained on radiological datasets.',
        'model_filename': 'chest_xray_model.h5',
        'image_width': 224,
        'image_height': 224,
        'classes': ['Normal', 'Pneumonia'],
    },
    {
        'name': 'Skin Lesion Classification',
        'slug': 'skin-lesion',
        'icon': '🔬',
        'description': 'Classify dermatoscopic images of skin lesions as benign or malignant. Early detection of malignant skin lesions is crucial for effective treatment and patient outcomes.',
        'model_filename': 'skin_lesion_model.h5',
        'image_width': 224,
        'image_height': 224,
        'classes': ['Benign', 'Malignant'],
    },
    {
        'name': 'Brain Tumor MRI',
        'slug': 'brain-tumor',
        'icon': '🧠',
        'description': 'Analyze MRI brain scans to classify tumors into categories: No Tumor, Glioma, Meningioma, and Pituitary tumors. Assists in preliminary screening and radiological assessment.',
        'model_filename': 'brain_tumor_model.h5',
        'image_width': 224,
        'image_height': 224,
        'classes': ['No Tumor', 'Glioma', 'Meningioma', 'Pituitary'],
    },
    {
        'name': 'Diabetic Retinopathy',
        'slug': 'diabetic-retinopathy',
        'icon': '👁️',
        'description': 'Grade retinal fundus photographs for diabetic retinopathy severity. Classifies images across 5 severity levels from No DR to Proliferative DR for early intervention.',
        'model_filename': 'diabetic_retinopathy_model.h5',
        'image_width': 224,
        'image_height': 224,
        'classes': ['No DR', 'Mild', 'Moderate', 'Severe', 'Proliferative DR'],
    },
]


def create_demo_models():
    """Create lightweight demo .h5 model files."""
    try:
        import tensorflow as tf
        import numpy as np
        
        models_dir = settings.ML_MODELS_DIR
        os.makedirs(models_dir, exist_ok=True)
        
        print("Creating demo models...")
        print(f"Output directory: {models_dir}")
        print()
        
        for module_def in MODULES:
            filename = module_def['model_filename']
            filepath = os.path.join(models_dir, filename)
            num_classes = len(module_def['classes'])
            img_size = (module_def['image_height'], module_def['image_width'])
            
            print(f"  Creating {module_def['name']}...")
            print(f"    File: {filename}")
            print(f"    Classes: {num_classes} — {module_def['classes']}")
            
            # Create a simple small model (NOT EfficientNet — to keep file size small)
            model = tf.keras.Sequential([
                tf.keras.layers.Input(shape=(img_size[0], img_size[1], 3)),
                tf.keras.layers.Conv2D(16, (3, 3), activation='relu', padding='same'),
                tf.keras.layers.GlobalAveragePooling2D(),
                tf.keras.layers.Dense(32, activation='relu'),
                tf.keras.layers.Dense(num_classes, activation='softmax'),
            ])
            
            model.compile(optimizer='adam', loss='categorical_crossentropy')
            model.save(filepath)
            
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"    Saved: {size_mb:.2f} MB")
            print()
        
        print("[OK] All demo models created successfully!")
        
    except ImportError:
        print("[WARN] TensorFlow not installed. Skipping model file creation.")
        print("   Models will use demo predictions (random) instead.")
        print("   Install TensorFlow: pip install tensorflow")
        
        # Still create the directory
        os.makedirs(settings.ML_MODELS_DIR, exist_ok=True)


def seed_database():
    """Create DiagnosticModule entries in the database."""
    print("\nSeeding database with diagnostic modules...")
    
    for module_def in MODULES:
        module, created = DiagnosticModule.objects.update_or_create(
            slug=module_def['slug'],
            defaults={
                'name': module_def['name'],
                'icon': module_def['icon'],
                'description': module_def['description'],
                'model_filename': module_def['model_filename'],
                'image_width': module_def['image_width'],
                'image_height': module_def['image_height'],
                'classes_json': json.dumps(module_def['classes']),
                'is_active': True,
            }
        )
        status = "Created" if created else "Updated"
        print(f"  {status}: {module.name}")
    
    print("\n[OK] Database seeded successfully!")


if __name__ == '__main__':
    print("=" * 60)
    print("  MedDiag AI — Demo Model Generator")
    print("=" * 60)
    print()
    
    create_demo_models()
    seed_database()
    
    print()
    print("=" * 60)
    print("  Setup complete! Run: python manage.py runserver")
    print("=" * 60)
