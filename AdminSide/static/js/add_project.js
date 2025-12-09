// Add Project Form Functionality
document.addEventListener('DOMContentLoaded', function() {
    initializeAddProjectForm();
});

function initializeAddProjectForm() {
    const addProjectForm = document.getElementById('addProjectForm');
    const closeBtn = document.getElementById('closeBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const technologiesInput = document.getElementById('technologiesInput');
    const tagsContainer = document.getElementById('tagsContainer');
    const technologiesHidden = document.getElementById('technologies');
    
    let technologies = [];

    // Technologies/Tags Management
    technologiesInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            const tech = this.value.trim();
            if (tech && !technologies.includes(tech)) {
                addTechnology(tech);
                this.value = '';
            }
        }
    });

    function addTechnology(tech) {
        technologies.push(tech);
        updateTagsDisplay();
        updateHiddenInput();
    }

    window.removeTechnology = function(tech) {
        technologies = technologies.filter(t => t !== tech);
        updateTagsDisplay();
        updateHiddenInput();
    }

    function updateTagsDisplay() {
        tagsContainer.innerHTML = '';
        technologies.forEach(tech => {
            const tag = document.createElement('div');
            tag.className = 'tag';
            tag.innerHTML = `
                ${tech}
                <button type="button" class="tag-remove" onclick="removeTechnology('${tech}')">
                    <i class="fas fa-times"></i>
                </button>
            `;
            tagsContainer.appendChild(tag);
        });
    }

    function updateHiddenInput() {
        technologiesHidden.value = technologies.join(',');
    }

    // File Upload Handling
    setupFileUploads();

    // Form Submission
    addProjectForm.addEventListener('submit', handleFormSubmit);

    // Close and Cancel buttons
    closeBtn.addEventListener('click', closeForm);
    cancelBtn.addEventListener('click', closeForm);

    // Escape key to close
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeForm();
        }
    });
}

function setupFileUploads() {
    const screenshotsInput = document.getElementById('screenshots');
    const screenshotsUploadArea = document.getElementById('screenshotsUploadArea');
    const screenshotsPreview = document.getElementById('screenshotsPreview');
    const zipFileInput = document.getElementById('zipFile');
    const zipUploadArea = document.getElementById('zipUploadArea');
    const zipFilePreview = document.getElementById('zipFilePreview');

    // Screenshots upload
    screenshotsUploadArea.addEventListener('click', () => screenshotsInput.click());
    setupDragAndDrop(screenshotsUploadArea, screenshotsInput, true);
    screenshotsInput.addEventListener('change', handleScreenshotsSelection);

    // ZIP file upload
    zipUploadArea.addEventListener('click', () => zipFileInput.click());
    setupDragAndDrop(zipUploadArea, zipFileInput, false);
    zipFileInput.addEventListener('change', handleZipFileSelection);
}

function setupDragAndDrop(uploadArea, input, isMultiple) {
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            input.files = e.dataTransfer.files;
            if (isMultiple) {
                handleScreenshotsSelection();
            } else {
                handleZipFileSelection();
            }
        }
    });
}

function handleScreenshotsSelection() {
    const files = Array.from(document.getElementById('screenshots').files);
    const preview = document.getElementById('screenshotsPreview');
    
    preview.innerHTML = '';
    
    files.forEach((file, index) => {
        const previewItem = document.createElement('div');
        previewItem.className = 'preview-item';
        previewItem.innerHTML = `
            <img src="" alt="Preview" style="background: #f5f5f5;">
            <div class="file-info">
                <div class="file-name">${file.name}</div>
                <div class="file-size">${formatFileSize(file.size)}</div>
            </div>
            <button type="button" class="preview-remove" onclick="removeScreenshot(${index})">
                <i class="fas fa-times"></i>
            </button>
        `;
        preview.appendChild(previewItem);
        
        // Create image preview
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = previewItem.querySelector('img');
                img.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });
}

function handleZipFileSelection() {
    const file = document.getElementById('zipFile').files[0];
    const preview = document.getElementById('zipFilePreview');
    
    preview.innerHTML = '';
    
    if (file) {
        const previewItem = document.createElement('div');
        previewItem.className = 'preview-item';
        previewItem.innerHTML = `
            <div style="padding: 20px; text-align: center; background: #f5f5f5;">
                <i class="fas fa-file-archive" style="font-size: 3rem; color: #666;"></i>
            </div>
            <div class="file-info">
                <div class="file-name">${file.name}</div>
                <div class="file-size">${formatFileSize(file.size)}</div>
            </div>
            <button type="button" class="preview-remove" onclick="removeZipFile()">
                <i class="fas fa-times"></i>
            </button>
        `;
        preview.appendChild(previewItem);
    }
}

window.removeScreenshot = function(index) {
    const input = document.getElementById('screenshots');
    const files = Array.from(input.files);
    files.splice(index, 1);
    
    const dt = new DataTransfer();
    files.forEach(file => dt.items.add(file));
    input.files = dt.files;
    
    handleScreenshotsSelection();
}

window.removeZipFile = function() {
    document.getElementById('zipFile').value = '';
    document.getElementById('zipFilePreview').innerHTML = '';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    
    // Show loading
    document.getElementById('loadingOverlay').style.display = 'flex';
    
    try {
        const response = await fetch('/api/projects', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const result = await response.json();
            showNotification('Project added successfully!', 'success');
            
            // Redirect to admin dashboard after success
            setTimeout(() => {
                window.location.href = '/admin';
            }, 1500);
            
        } else {
            const error = await response.json();
            throw new Error(error.error || 'Failed to add project');
        }
        
    } catch (error) {
        console.error('Error adding project:', error);
        showNotification(error.message || 'Error adding project. Please try again.', 'error');
    } finally {
        document.getElementById('loadingOverlay').style.display = 'none';
    }
}

function closeForm() {
    if (confirm('Are you sure you want to leave? Any unsaved changes will be lost.')) {
        window.location.href = '/admin';
    }
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        z-index: 2001;
        animation: slideIn 0.3s ease-out;
        max-width: 400px;
    `;
    
    if (type === 'success') {
        notification.style.backgroundColor = 'var(--success)';
    } else if (type === 'error') {
        notification.style.backgroundColor = 'var(--danger)';
    } else {
        notification.style.backgroundColor = 'var(--primary)';
    }
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }
    }, 5000);
}