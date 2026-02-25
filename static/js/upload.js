// File Upload Handler
class FileUploadHandler {
    constructor() {
        this.files = [];
        this.maxFileSize = 100 * 1024 * 1024; // 100 MB
        this.init();
    }

    init() {
        this.bindElements();
        this.bindEvents();
    }

    bindElements() {
        this.uploadBox = document.getElementById('uploadBox');
        this.fileInput = document.getElementById('fileInput');
        this.uploadBtn = document.getElementById('uploadBtn');
        this.processBtn = document.getElementById('processBtn');
        this.clearBtn = document.getElementById('clearBtn');
        this.newUploadBtn = document.getElementById('newUploadBtn');
        
        this.filesListSection = document.getElementById('filesListSection');
        this.filesList = document.getElementById('filesList');
        this.progressSection = document.getElementById('progressSection');
        this.progressFill = document.getElementById('progressFill');
        this.progressText = document.getElementById('progressText');
        
        // Loader elements
        this.loaderSection = document.getElementById('loaderSection');
        this.loaderTitle = document.getElementById('loaderTitle');
        this.loaderStatus = document.getElementById('loaderStatus');
        this.processingStats = document.getElementById('processingStats');
        this.processingCount = document.getElementById('processingCount');
        this.completedCount = document.getElementById('completedCount');
        this.elapsedTime = document.getElementById('elapsedTime');
        
        this.resultsSection = document.getElementById('resultsSection');
        this.resultsList = document.getElementById('resultsList');
        
        this.errorMessage = document.getElementById('errorMessage');
        this.successMessage = document.getElementById('successMessage');
        
        this.extractText = document.getElementById('extractText');
        this.extractMetadata = document.getElementById('extractMetadata');
        this.extractTables = document.getElementById('extractTables');
        this.extractImages = document.getElementById('extractImages');
    }

    bindEvents() {
        // Upload box events
        this.uploadBox.addEventListener('click', () => this.fileInput.click());
        this.uploadBtn.addEventListener('click', () => this.fileInput.click());
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        
        // Drag and drop events
        this.uploadBox.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.uploadBox.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.uploadBox.addEventListener('drop', (e) => this.handleDrop(e));
        
        // Button events
        this.processBtn.addEventListener('click', () => this.processFiles());
        this.clearBtn.addEventListener('click', () => this.clearFiles());
        this.newUploadBtn.addEventListener('click', () => this.resetForm());
    }

    handleFileSelect(event) {
        const files = Array.from(event.target.files);
        this.addFiles(files);
    }

    handleDragOver(event) {
        event.preventDefault();
        event.stopPropagation();
        this.uploadBox.classList.add('drag-over');
    }

    handleDragLeave(event) {
        event.preventDefault();
        event.stopPropagation();
        this.uploadBox.classList.remove('drag-over');
    }

    handleDrop(event) {
        event.preventDefault();
        event.stopPropagation();
        this.uploadBox.classList.remove('drag-over');
        
        const files = Array.from(event.dataTransfer.files);
        this.addFiles(files);
    }

    addFiles(files) {
        this.hideMessages();
        
        for (const file of files) {
            // Validate PDF type
            if (!this.isPDFFile(file)) {
                this.showError(`"${file.name}" is not a valid PDF file`);
                continue;
            }

            // Validate file size
            if (file.size > this.maxFileSize) {
                this.showError(`"${file.name}" exceeds 100 MB limit`);
                continue;
            }

            // Check for duplicate
            if (this.files.some(f => f.name === file.name && f.size === file.size)) {
                this.showError(`"${file.name}" is already added`);
                continue;
            }

            this.files.push(file);
        }

        this.renderFilesList();
    }

    isPDFFile(file) {
        return file.type === 'application/pdf' || file.name.endsWith('.pdf');
    }

    renderFilesList() {
        if (this.files.length === 0) {
            this.filesListSection.style.display = 'none';
            return;
        }

        this.filesListSection.style.display = 'block';
        this.filesList.innerHTML = '';

        this.files.forEach((file, index) => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.innerHTML = `
                <div class="file-details">
                    <div class="file-name">📄 ${file.name}</div>
                    <div class="file-size">${this.formatFileSize(file.size)}</div>
                </div>
                <button class="file-remove" onclick="fileUploadHandler.removeFile(${index})">
                    Remove
                </button>
            `;
            this.filesList.appendChild(fileItem);
        });
    }

    removeFile(index) {
        this.files.splice(index, 1);
        this.renderFilesList();
    }

    clearFiles() {
        this.files = [];
        this.fileInput.value = '';
        this.renderFilesList();
        this.hideMessages();
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    }

    async processFiles() {
        if (this.files.length === 0) {
            this.showError('Please select at least one PDF file');
            return;
        }

        // Get processing options
        const options = {
            extractText: this.extractText.checked,
            extractMetadata: this.extractMetadata.checked,
            extractTables: this.extractTables.checked,
            extractImages: this.extractImages.checked,
        };

        // Show progress section
        this.progressSection.style.display = 'block';
        this.filesListSection.style.display = 'none';
        this.hideMessages();

        // Create FormData with all files
        try {
            const result = await this.uploadFilesToServer(this.files, options);
            this.showResults([result]);
        } catch (error) {
            this.showResults([{
                name: 'Upload',
                type: 'error',
                error: error.message
            }]);
        }
    }

    async uploadFilesToServer(files, options) {
        const formData = new FormData();
        
        // Add all files to FormData
        for (const file of files) {
            formData.append('files', file);
        }
        
        // Add processing options
        formData.append('extractText', options.extractText);
        formData.append('extractMetadata', options.extractMetadata);
        formData.append('extractTables', options.extractTables);
        formData.append('extractImages', options.extractImages);

        try {
            this.updateProgress(50);
            
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Upload failed');
            }

            const data = await response.json();
            this.updateProgress(100);
            
            // Hide progress and files list, show loader
            this.progressSection.style.display = 'none';
            this.filesListSection.style.display = 'none';
            this.resultsSection.style.display = 'none';
            this.loaderSection.style.display = 'block';
            this.processingStats.style.display = 'block';
            
            // Start polling for status
            const startTime = Date.now();
            this.pollUploadStatus(startTime);
            
            return {
                name: `${files.length} file(s) uploaded`,
                type: data.success ? 'success' : 'warning',
                message: data.message,
                uploaded: data.uploaded,
                errors: data.errors
            };
        } catch (error) {
            this.updateProgress(0);
            throw error;
        }
    }

    async pollUploadStatus(startTime) {
        const pollInterval = setInterval(async () => {
            try {
                const response = await fetch('/api/upload-status');
                const status = await response.json();
                
                // Update elapsed time
                const elapsedSeconds = Math.floor((Date.now() - startTime) / 1000);
                this.elapsedTime.textContent = this.formatTime(elapsedSeconds);
                
                // Update processing counts
                this.processingCount.textContent = status.processing + status.pending;
                this.completedCount.textContent = status.completed;
                
                // Update status message
                if (status.still_processing) {
                    this.loaderStatus.textContent = 
                        `Processing ${status.processing + status.pending} file(s)... ` +
                        `${status.completed} completed, ${status.failed} failed`;
                } else {
                    // Processing complete
                    clearInterval(pollInterval);
                    
                    // Hide loader and show results
                    this.loaderSection.style.display = 'none';
                    this.showProcessingResults(status);
                }
            } catch (error) {
                console.error('Status check error:', error);
            }
        }, 1000); // Poll every second
    }

    showProcessingResults(status) {
        this.resultsSection.style.display = 'block';
        this.resultsList.innerHTML = '';

        const resultItem = document.createElement('div');
        resultItem.className = `result-item success`;

        let content = `<div class="result-file-name">📊 Processing Summary</div>`;
        content += `<div class="result-content">`;
        content += `<strong>✓ Completed:</strong> ${status.completed} file(s)<br>`;
        
        if (status.failed > 0) {
            content += `<strong style="color: #c0392b;">✗ Failed:</strong> ${status.failed} file(s)<br>`;
        }
        
        if (status.failed_files && status.failed_files.length > 0) {
            content += `<br><strong>Failed Files:</strong><ul>`;
            status.failed_files.forEach(file => {
                content += `<li>❌ ${file.name} - ${file.error}</li>`;
            });
            content += `</ul>`;
        }
        
        content += `<br><strong>Total Processing Time:</strong> ${this.elapsedTime.textContent}`;
        content += `</div>`;

        resultItem.innerHTML = content;
        this.resultsList.appendChild(resultItem);

        if (status.failed === 0) {
            this.showSuccess('All files processed successfully!');
        } else {
            this.showError(`Processing completed with ${status.failed} error(s)`);
        }
    }

    formatTime(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;

        if (hours > 0) {
            return `${hours}h ${minutes}m ${secs}s`;
        } else if (minutes > 0) {
            return `${minutes}m ${secs}s`;
        } else {
            return `${secs}s`;
        }
    }

    updateProgress(progress) {
        this.progressFill.style.width = progress + '%';
        this.progressText.textContent = progress + '%';
    }

    showResults(results) {
        this.progressSection.style.display = 'none';
        this.resultsSection.style.display = 'block';
        this.resultsList.innerHTML = '';

        results.forEach((result) => {
            const resultItem = document.createElement('div');
            resultItem.className = `result-item ${result.type}`;

            let content = `<div class="result-file-name">📄 ${result.name}</div>`;

            if (result.error) {
                content += `<div class="result-content" style="color: #c0392b;">❌ Error: ${result.error}</div>`;
            } else {
                // Display upload message
                if (result.message) {
                    content += `<div class="result-content"><strong>Status:</strong> ${result.message}</div>`;
                }

                // Display uploaded files list
                if (result.uploaded && result.uploaded.length > 0) {
                    content += `<div class="result-content"><strong>Uploaded Files (${result.uploaded.length}):</strong><ul>`;
                    result.uploaded.forEach(file => {
                        content += `<li>✓ ${file.name} - Size: ${file.size} bytes - Status: ${file.status}</li>`;
                    });
                    content += `</ul></div>`;
                }

                // Display errors if any
                if (result.errors && result.errors.length > 0) {
                    content += `<div class="result-content" style="color: #c0392b;"><strong>Errors (${result.errors.length}):</strong><ul>`;
                    result.errors.forEach(error => {
                        content += `<li>❌ ${error}</li>`;
                    });
                    content += `</ul></div>`;
                }
            }

            resultItem.innerHTML = content;
            this.resultsList.appendChild(resultItem);
        });

        const message = results.some(r => r.error) ? 'Upload completed with errors' : 'Files uploaded successfully!';
        this.showSuccess(message);
    }

    resetForm() {
        this.files = [];
        this.fileInput.value = '';
        this.filesListSection.style.display = 'none';
        this.progressSection.style.display = 'none';
        this.resultsSection.style.display = 'none';
        this.loaderSection.style.display = 'none';
        this.progressFill.style.width = '0%';
        this.progressText.textContent = '0%';
        this.hideMessages();
    }

    showError(message) {
        this.errorMessage.textContent = '❌ ' + message;
        this.errorMessage.style.display = 'block';
    }

    showSuccess(message) {
        this.successMessage.textContent = '✓ ' + message;
        this.successMessage.style.display = 'block';
    }

    hideMessages() {
        this.errorMessage.style.display = 'none';
        this.successMessage.style.display = 'none';
    }
}

// Initialize on DOM ready
let fileUploadHandler;
document.addEventListener('DOMContentLoaded', () => {
    fileUploadHandler = new FileUploadHandler();
});
