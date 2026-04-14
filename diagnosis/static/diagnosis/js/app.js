/**
 * MedDiag — UI Interactions & Animations
 */

document.addEventListener('DOMContentLoaded', function() {
    initMobileMenu();
    initDropZone();
    initLoadingState();
    initAnimations();
    initMessageDismiss();
    initConfidenceBars();
});

/* ---- Mobile Menu ---- */
function initMobileMenu() {
    const menuBtn = document.getElementById('mobile-menu-btn');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');

    if (!menuBtn || !sidebar) return;

    menuBtn.addEventListener('click', () => {
        sidebar.classList.toggle('open');
        if (overlay) overlay.classList.toggle('show');
    });

    if (overlay) {
        overlay.addEventListener('click', () => {
            sidebar.classList.remove('open');
            overlay.classList.remove('show');
        });
    }
}

/* ---- Drag & Drop Upload ---- */
function initDropZone() {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('image-upload-input');
    const previewContainer = document.getElementById('image-preview-container');
    const previewImage = document.getElementById('image-preview');
    const previewName = document.getElementById('preview-filename');
    const previewSize = document.getElementById('preview-filesize');
    const removeBtn = document.getElementById('remove-preview');
    const submitBtn = document.getElementById('submit-btn');

    if (!dropZone || !fileInput) return;

    // Click to upload
    dropZone.addEventListener('click', () => fileInput.click());

    // Drag events
    ['dragenter', 'dragover'].forEach(event => {
        dropZone.addEventListener(event, (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        });
    });

    ['dragleave', 'drop'].forEach(event => {
        dropZone.addEventListener(event, (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
        });
    });

    // Handle drop
    dropZone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            showPreview(files[0]);
        }
    });

    // Handle file input change
    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            showPreview(this.files[0]);
        }
    });

    function showPreview(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please select an image file.');
            return;
        }

        const reader = new FileReader();
        reader.onload = function(e) {
            if (previewImage) previewImage.src = e.target.result;
            if (previewName) previewName.textContent = file.name;
            if (previewSize) previewSize.textContent = formatFileSize(file.size);
            if (previewContainer) previewContainer.classList.add('show');
            if (dropZone) dropZone.style.display = 'none';
            if (submitBtn) submitBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    // Remove preview
    if (removeBtn) {
        removeBtn.addEventListener('click', () => {
            fileInput.value = '';
            if (previewContainer) previewContainer.classList.remove('show');
            if (dropZone) dropZone.style.display = '';
            if (submitBtn) submitBtn.disabled = true;
        });
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

/* ---- Loading State ---- */
function initLoadingState() {
    const form = document.getElementById('diagnosis-form');
    const loadingOverlay = document.getElementById('loading-overlay');

    if (!form || !loadingOverlay) return;

    form.addEventListener('submit', function() {
        loadingOverlay.classList.add('show');
    });
}

/* ---- Scroll Animations ---- */
function initAnimations() {
    const elements = document.querySelectorAll('.animate-on-scroll');

    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-slide-up');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        elements.forEach(el => observer.observe(el));
    } else {
        elements.forEach(el => el.classList.add('animate-slide-up'));
    }
}

/* ---- Message Auto-Dismiss ---- */
function initMessageDismiss() {
    const messages = document.querySelectorAll('.message');
    messages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-10px)';
            msg.style.transition = 'all 0.3s ease';
            setTimeout(() => msg.remove(), 300);
        }, 5000);
    });
}

/* ---- Confidence Bars Animation ---- */
function initConfidenceBars() {
    const bars = document.querySelectorAll('.confidence-bar-fill');
    
    if (bars.length === 0) return;

    // Use IntersectionObserver to animate when visible
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const bar = entry.target;
                const targetWidth = bar.dataset.width || '0%';
                setTimeout(() => {
                    bar.style.width = targetWidth;
                }, 200);
                observer.unobserve(bar);
            }
        });
    }, { threshold: 0.1 });

    bars.forEach(bar => {
        // Store target width and start at 0
        bar.dataset.width = bar.style.width || getComputedStyle(bar).width;
        bar.style.width = '0%';
        observer.observe(bar);
    });
}
