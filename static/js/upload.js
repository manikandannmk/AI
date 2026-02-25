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

        // Process files
        let completedFiles = 0;
        const results = [];

        for (const file of this.files) {
            try {
                const result = await this.processFile(file, options);
                results.push(result);
            } catch (error) {
                results.push({
                    name: file.name,
                    error: error.message,
                    type: 'error'
                });
            }

            // Update progress
            completedFiles++;
            const progress = Math.round((completedFiles / this.files.length) * 100);
            this.updateProgress(progress);
        }

        // Show results
        this.showResults(results);
    }

    async processFile(file, options) {
        // Simulate API call to process PDF
        return new Promise((resolve) => {
            const reader = new FileReader();
            
            reader.onload = (e) => {
                // Simulate processing delay
                setTimeout(() => {
                    const result = {
                        name: file.name,
                        type: 'success',
                        size: this.formatFileSize(file.size),
                    };

                    // Mock results based on selected options
                    if (options.extractText) {
                        result.text = `Text extraction from ${file.name} would appear here...`;
                    }
                    if (options.extractMetadata) {
                        result.metadata = {
                            'File Size': this.formatFileSize(file.size),
                            'File Type': 'PDF',
                            'Upload Time': new Date().toLocaleString(),
                        };
                    }

                    resolve(result);
                }, Math.random() * 2000);
            };

            reader.readAsArrayBuffer(file);
        });
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
                content += `<div class="result-content" style="color: #c0392b;">Error: ${result.error}</div>`;
            } else {
                if (result.size) {
                    content += `<div class="result-content"><strong>Size:</strong> ${result.size}</div>`;
                }

                if (result.text) {
                    content += `<div class="result-content"><strong>Extracted Text:</strong>\n${result.text}</div>`;
                }

                if (result.metadata) {
                    content += `<div class="result-content"><strong>Metadata:</strong>\n`;
                    for (const [key, value] of Object.entries(result.metadata)) {
                        content += `${key}: ${JSON.stringify(value)}\n`;
                    }
                    content += `</div>`;
                }

                // Add download link
                content += `<a href="#" class="result-link">⬇️ Download Result</a>`;
            }

            resultItem.innerHTML = content;
            this.resultsList.appendChild(resultItem);
        });

        this.showSuccess('Files processed successfully!');
    }

    resetForm() {
        this.files = [];
        this.fileInput.value = '';
        this.filesListSection.style.display = 'none';
        this.progressSection.style.display = 'none';
        this.resultsSection.style.display = 'none';
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
