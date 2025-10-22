// ============================================
// BRD Test Case Automation - Main JavaScript
// ============================================

// Global variables
let selectedFiles = [];
const API_BASE_URL = window.location.origin;

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const selectedFilesDiv = document.getElementById('selectedFiles');
const generateBtn = document.getElementById('generateBtn');
const targetCountInput = document.getElementById('targetCount');
const progressSection = document.getElementById('progressSection');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const resultsSection = document.getElementById('resultsSection');
const resultsContent = document.getElementById('resultsContent');

// ============================================
// Initialization
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('BRD Test Case Automation initialized');

    // Load config
    loadConfig();

    // Setup event listeners
    setupEventListeners();
});

// ============================================
// Event Listeners Setup
// ============================================

function setupEventListeners() {
    // Click to select files
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    // File input change
    fileInput.addEventListener('change', handleFileSelect);

    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);

    // Generate button
    generateBtn.addEventListener('click', generateTestCases);

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        document.body.addEventListener(eventName, preventDefaults, false);
    });
}

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// ============================================
// File Selection Handlers
// ============================================

function handleFileSelect(e) {
    const files = Array.from(e.target.files);
    addFiles(files);
}

function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');

    const files = Array.from(e.dataTransfer.files);
    addFiles(files);
}

function addFiles(files) {
    // Filter only PDF files
    const pdfFiles = files.filter(file => file.type === 'application/pdf' || file.name.endsWith('.pdf'));

    if (pdfFiles.length === 0) {
        alert('⚠️ Vui lòng chọn file PDF!');
        return;
    }

    // Check file size (16MB limit)
    const oversizedFiles = pdfFiles.filter(file => file.size > 16 * 1024 * 1024);
    if (oversizedFiles.length > 0) {
        alert(`⚠️ File quá lớn: ${oversizedFiles[0].name}\nKích thước tối đa: 16MB`);
        return;
    }

    // Add files to selected list
    pdfFiles.forEach(file => {
        // Check if file already selected
        if (!selectedFiles.find(f => f.name === file.name)) {
            selectedFiles.push(file);
        }
    });

    renderSelectedFiles();
    updateGenerateButton();
}

function removeFile(index) {
    selectedFiles.splice(index, 1);
    renderSelectedFiles();
    updateGenerateButton();
}

function renderSelectedFiles() {
    if (selectedFiles.length === 0) {
        selectedFilesDiv.innerHTML = '';
        return;
    }

    const html = selectedFiles.map((file, index) => `
        <div class="file-item">
            <div class="file-info">
                <div class="file-icon">📄</div>
                <div class="file-details">
                    <div class="file-name">${file.name}</div>
                    <div class="file-size">${formatFileSize(file.size)}</div>
                </div>
            </div>
            <button class="file-remove" onclick="removeFile(${index})">×</button>
        </div>
    `).join('');

    selectedFilesDiv.innerHTML = html;
}

function updateGenerateButton() {
    generateBtn.disabled = selectedFiles.length === 0;
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Make removeFile global
window.removeFile = removeFile;

// ============================================
// API Calls
// ============================================

async function loadConfig() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/config`);
        const data = await response.json();

        if (data.success) {
            document.getElementById('modelInfo').textContent = data.config.model;
            document.getElementById('coverageInfo').textContent = `${data.config.coverage_target}%`;
        }
    } catch (error) {
        console.error('Failed to load config:', error);
    }
}

async function generateTestCases() {
    if (selectedFiles.length === 0) return;

    // Hide results, show progress
    resultsSection.style.display = 'none';
    progressSection.style.display = 'block';
    generateBtn.disabled = true;

    // Reset progress
    updateProgress(0, 'Đang chuẩn bị...');

    // Prepare form data
    const formData = new FormData();
    selectedFiles.forEach(file => {
        formData.append('files', file);
    });
    formData.append('target_count', targetCountInput.value);

    try {
        updateProgress(20, 'Đang upload files...');

        const response = await fetch(`${API_BASE_URL}/api/generate-testcases`, {
            method: 'POST',
            body: formData
        });

        updateProgress(40, 'Đang extract text từ PDF...');

        const data = await response.json();

        updateProgress(100, 'Hoàn thành!');

        // Show results after a short delay
        setTimeout(() => {
            displayResults(data);
        }, 500);

    } catch (error) {
        console.error('Error:', error);
        progressSection.style.display = 'none';
        alert(`❌ Lỗi: ${error.message}`);
        generateBtn.disabled = false;
    }
}

function updateProgress(percentage, text) {
    progressFill.style.width = `${percentage}%`;
    progressText.textContent = text;
}

function displayResults(data) {
    progressSection.style.display = 'none';
    resultsSection.style.display = 'block';
    generateBtn.disabled = false;

    let html = '';

    if (data.success) {
        html += `<div class="result-summary">
            <p><strong>✅ Thành công:</strong> ${data.successful_files}/${data.total_files} files</p>
        </div>`;
    }

    data.results.forEach(result => {
        if (result.success) {
            html += `
                <div class="result-item">
                    <div class="result-filename">📄 ${result.filename}</div>
                    <div class="result-stats">
                        <div class="stat-item">
                            <span class="stat-label">Test Cases</span>
                            <span class="stat-value">${result.total_test_cases}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Coverage</span>
                            <span class="stat-value">${result.coverage_percentage}%</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Worksheet</span>
                            <span class="stat-value" style="font-size: 0.9rem;">${result.worksheet_name.substring(0, 20)}...</span>
                        </div>
                    </div>
                    <a href="${result.sheet_url}" target="_blank" class="result-link">
                        🔗 Mở Google Sheet
                    </a>
                </div>
            `;
        } else {
            html += `
                <div class="result-item error">
                    <div class="result-filename">📄 ${result.filename}</div>
                    <div class="error-message">❌ ${result.error}</div>
                </div>
            `;
        }
    });

    resultsContent.innerHTML = html;

    // Clear selected files after successful generation
    if (data.success) {
        selectedFiles = [];
        renderSelectedFiles();
        updateGenerateButton();
    }
}

// ============================================
// Utility Functions
// ============================================

console.log('Main.js loaded successfully');