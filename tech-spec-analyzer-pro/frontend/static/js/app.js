/**
 * Tech Spec Analyzer Pro - Advanced Frontend Application
 * Interactive UI with real-time analysis and enhanced user experience
 */

class TechSpecAnalyzer {
    constructor() {
        this.initializeElements();
        this.setupEventListeners();
        this.initializeFeatures();
        this.loadExampleData();
    }

    initializeElements() {
        // Input elements
        this.documentTextEl = document.getElementById('document_text');
        this.userQueryEl = document.getElementById('user_query');
        this.analyzeButtonEl = document.getElementById('analyze_button');
        this.buttonSpinner = this.analyzeButtonEl.querySelector('.spinner-border');
        this.buttonText = this.analyzeButtonEl.querySelector('.button-text');

        // Control elements
        this.loadExampleEl = document.getElementById('load_example');
        this.clearInputEl = document.getElementById('clear_input');
        this.copyJsonEl = document.getElementById('copy_json');
        this.formatToggleEl = document.getElementById('format_toggle');
        this.exportResultsEl = document.getElementById('export_results');

        // Output elements
        this.jsonOutputEl = document.getElementById('json_output');
        this.formattedResultsEl = document.getElementById('formatted_results');
        this.analysisStatusEl = document.getElementById('analysis_status');
        this.resultSummaryEl = document.getElementById('result_summary');
        this.parameterPreviewEl = document.getElementById('parameter_preview');
        this.parameterCardsEl = document.getElementById('parameter_cards');

        // Stats elements
        this.charCountEl = document.getElementById('char_count');
        this.lineCountEl = document.getElementById('line_count');

        // State
        this.currentResults = null;
        this.isFormatted = false;
        this.isAnalyzing = false;
    }

    setupEventListeners() {
        // Main functionality
        this.analyzeButtonEl.addEventListener('click', () => this.performAnalysis());
        this.loadExampleEl.addEventListener('click', () => this.loadExample());
        this.clearInputEl.addEventListener('click', () => this.clearInputs());

        // Input tracking
        this.documentTextEl.addEventListener('input', () => this.updateInputStats());
        this.userQueryEl.addEventListener('input', () => this.validateInput());

        // Result controls
        this.copyJsonEl.addEventListener('click', () => this.copyResults());
        this.formatToggleEl.addEventListener('click', () => this.toggleFormat());
        this.exportResultsEl.addEventListener('click', () => this.exportResults());

        // Query suggestions
        document.querySelectorAll('[data-query]').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                this.userQueryEl.value = item.dataset.query;
                this.validateInput();
            });
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch(e.key) {
                    case 'Enter':
                        if (!this.isAnalyzing) {
                            e.preventDefault();
                            this.performAnalysis();
                        }
                        break;
                    case 'l':
                        e.preventDefault();
                        this.loadExample();
                        break;
                    case 'k':
                        e.preventDefault();
                        this.clearInputs();
                        break;
                }
            }
        });

        // Auto-save to localStorage
        this.documentTextEl.addEventListener('input', debounce(() => {
            localStorage.setItem('tech_spec_document', this.documentTextEl.value);
        }, 1000));

        this.userQueryEl.addEventListener('input', debounce(() => {
            localStorage.setItem('tech_spec_query', this.userQueryEl.value);
        }, 1000));
    }

    initializeFeatures() {
        // Restore saved content
        const savedDocument = localStorage.getItem('tech_spec_document');
        const savedQuery = localStorage.getItem('tech_spec_query');
        
        if (savedDocument && savedDocument.trim()) {
            this.documentTextEl.value = savedDocument;
        }
        if (savedQuery && savedQuery.trim()) {
            this.userQueryEl.value = savedQuery;
        }

        // Initialize input stats
        this.updateInputStats();
        this.validateInput();
        this.updateStatus('Ready', 'secondary');

        // Add tooltips
        this.initializeTooltips();
    }

    initializeTooltips() {
        // Add helpful tooltips for better UX
        const tooltips = [
            { element: this.analyzeButtonEl, text: 'Ctrl+Enter to analyze quickly' },
            { element: this.loadExampleEl, text: 'Ctrl+L to load example data' },
            { element: this.clearInputEl, text: 'Ctrl+K to clear all inputs' },
            { element: this.copyJsonEl, text: 'Copy analysis results to clipboard' }
        ];

        tooltips.forEach(({ element, text }) => {
            if (element) {
                element.setAttribute('title', text);
                element.setAttribute('data-bs-toggle', 'tooltip');
                element.setAttribute('data-bs-placement', 'top');
            }
        });

        // Initialize Bootstrap tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }

    loadExampleData() {
        this.exampleDocument = `Datasheet for "Power Supply Unit X100"
1. Input Voltage: 100-240V AC, 50/60Hz
2. Output Voltage: 12V DC
3. Max Output Current: 5 Amps
4. Operating Temperature: 0°C to 50°C
5. Dimensions: 10cm x 5cm x 3cm
6. Efficiency: 85%
7. Certifications: CE, FCC, RoHS

Datasheet for "LED Strip Light Alpha"
1. Required Input Voltage: 12V DC
2. Current Draw: 4 Amps (at full brightness)
3. Operating Temperature Range: -10°C to 60°C
4. Dimensions: Flexible strip, 5m length
5. Power Consumption: 48W
6. Color Temperature: 3000K warm white
7. Certification: CE, RoHS
8. IP Rating: IP65 (weatherproof)

Technical Specifications for "High-Power LED Module Beta"
1. Forward Voltage: 12V DC ± 0.5V
2. Forward Current: 3.5A typical, 4A maximum
3. Thermal Resistance: 2.5°C/W
4. Operating Temperature: -20°C to 85°C
5. Luminous Flux: 5000 lumens
6. Lifespan: 50,000 hours`;

        this.exampleQuery = `Analyze the compatibility between Power Supply Unit X100 and LED Strip Light Alpha. Check if the PSU can safely power the LED strip considering voltage matching and current capacity.`;
    }

    loadExample() {
        this.documentTextEl.value = this.exampleDocument;
        this.userQueryEl.value = this.exampleQuery;
        this.updateInputStats();
        this.validateInput();
        this.updateStatus('Example Loaded', 'info');
        
        // Visual feedback
        this.documentTextEl.classList.add('success-glow');
        setTimeout(() => this.documentTextEl.classList.remove('success-glow'), 2000);
    }

    clearInputs() {
        this.documentTextEl.value = '';
        this.userQueryEl.value = '';
        this.updateInputStats();
        this.validateInput();
        this.updateStatus('Inputs Cleared', 'secondary');
        
        // Clear localStorage
        localStorage.removeItem('tech_spec_document');
        localStorage.removeItem('tech_spec_query');
        
        // Hide results
        this.hideResults();
    }

    updateInputStats() {
        const text = this.documentTextEl.value;
        const charCount = text.length;
        const lineCount = text.split('\n').length;
        
        this.charCountEl.textContent = charCount.toLocaleString();
        this.lineCountEl.textContent = lineCount.toLocaleString();
        
        // Update character count color based on length
        if (charCount > 10000) {
            this.charCountEl.className = 'text-warning';
        } else if (charCount > 5000) {
            this.charCountEl.className = 'text-info';
        } else {
            this.charCountEl.className = 'text-muted';
        }
    }

    validateInput() {
        const hasDocument = this.documentTextEl.value.trim().length > 0;
        const hasQuery = this.userQueryEl.value.trim().length > 0;
        const isValid = hasDocument && hasQuery && !this.isAnalyzing;
        
        this.analyzeButtonEl.disabled = !isValid;
        
        if (isValid) {
            this.analyzeButtonEl.classList.remove('btn-secondary');
            this.analyzeButtonEl.classList.add('btn-success');
        } else {
            this.analyzeButtonEl.classList.remove('btn-success');
            this.analyzeButtonEl.classList.add('btn-secondary');
        }
    }

    async performAnalysis() {
        if (this.isAnalyzing) return;
        
        const documentText = this.documentTextEl.value.trim();
        const userQuery = this.userQueryEl.value.trim();

        if (!documentText || !userQuery) {
            this.showError('Please provide both document content and analysis query.');
            return;
        }

        this.startAnalysis();

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    document_text: documentText,
                    user_query: userQuery,
                }),
            });

            if (!response.ok) {
                throw new Error(`Analysis failed with status: ${response.status}`);
            }

            const data = await response.json();
            this.handleAnalysisResults(data);

        } catch (error) {
            console.error('Analysis error:', error);
            this.handleAnalysisError(error.message);
        } finally {
            this.endAnalysis();
        }
    }

    startAnalysis() {
        this.isAnalyzing = true;
        this.analyzeButtonEl.disabled = true;
        this.analyzeButtonEl.classList.add('analyzing');
        this.buttonSpinner.classList.remove('d-none');
        this.buttonText.textContent = 'Analyzing...';
        
        this.updateStatus('Analyzing Document...', 'primary');
        this.hideResults();
        
        // Show loading in JSON output
        this.jsonOutputEl.textContent = 'Processing technical analysis...\nExtracting parameters...\nPerforming compatibility checks...';
        
        // Add progress simulation
        this.simulateProgress();
    }

    simulateProgress() {
        const messages = [
            'Scanning document structure...',
            'Extracting technical parameters...',
            'Analyzing voltage specifications...',
            'Checking current requirements...',
            'Calculating compatibility scores...',
            'Generating detailed report...'
        ];

        let index = 0;
        this.progressInterval = setInterval(() => {
            if (index < messages.length && this.isAnalyzing) {
                this.jsonOutputEl.textContent = messages[index];
                index++;
            } else {
                clearInterval(this.progressInterval);
            }
        }, 800);
    }

    endAnalysis() {
        this.isAnalyzing = false;
        this.analyzeButtonEl.disabled = false;
        this.analyzeButtonEl.classList.remove('analyzing');
        this.buttonSpinner.classList.add('d-none');
        this.buttonText.textContent = 'Analyze Compatibility';
        
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
        }
    }

    handleAnalysisResults(data) {
        this.currentResults = data;
        
        // Update JSON output
        this.jsonOutputEl.textContent = JSON.stringify(data, null, 2);
        
        // Show copy and export buttons
        this.copyJsonEl.style.display = 'inline-block';
        this.exportResultsEl.disabled = false;
        
        // Update summary
        this.updateResultSummary(data);
        
        // Show parameter preview if available
        this.updateParameterPreview(data);
        
        // Update status based on results
        if (data.Decision === 'Compatible') {
            this.updateStatus('Analysis Complete - Compatible', 'success');
            this.jsonOutputEl.classList.add('success-glow');
        } else if (data.Decision === 'Incompatible') {
            this.updateStatus('Analysis Complete - Incompatible', 'warning');
        } else if (data.Decision === 'Error') {
            this.updateStatus('Analysis Error', 'danger');
            this.jsonOutputEl.classList.add('error-glow');
        } else {
            this.updateStatus('Analysis Complete', 'info');
        }
        
        // Remove glow effects after delay
        setTimeout(() => {
            this.jsonOutputEl.classList.remove('success-glow', 'error-glow');
        }, 3000);
        
        // Add fade-in animation
        this.resultSummaryEl.classList.add('fade-in');
        this.parameterPreviewEl.classList.add('slide-up');
    }

    handleAnalysisError(errorMessage) {
        this.updateStatus('Analysis Failed', 'danger');
        this.jsonOutputEl.textContent = JSON.stringify({
            "error": "Analysis failed",
            "message": errorMessage,
            "timestamp": new Date().toISOString(),
            "suggestion": "Please check your document format and try again"
        }, null, 2);
        
        this.jsonOutputEl.classList.add('error-glow');
        setTimeout(() => this.jsonOutputEl.classList.remove('error-glow'), 3000);
    }

    updateResultSummary(data) {
        if (!data.Decision || data.Decision === 'Error') {
            this.resultSummaryEl.style.display = 'none';
            return;
        }

        const decisionIcons = {
            'Compatible': { icon: 'bi-check-circle-fill text-success', class: 'alert-success' },
            'Incompatible': { icon: 'bi-x-circle-fill text-danger', class: 'alert-danger' },
            'Not Explicitly Covered': { icon: 'bi-question-circle-fill text-warning', class: 'alert-warning' }
        };

        const config = decisionIcons[data.Decision] || { icon: 'bi-info-circle-fill text-info', class: 'alert-info' };

        const confidenceColor = {
            'High': 'text-success',
            'Medium': 'text-warning',
            'Low': 'text-danger'
        }[data.Confidence_Score] || 'text-muted';

        this.resultSummaryEl.innerHTML = `
            <div class="${config.class} d-flex align-items-start">
                <div class="me-3">
                    <i class="${config.icon} fs-3"></i>
                </div>
                <div class="flex-grow-1">
                    <h5 class="alert-heading mb-2">
                        Analysis Result: ${data.Decision}
                        <span class="badge ${confidenceColor.replace('text-', 'bg-')} ms-2">${data.Confidence_Score} Confidence</span>
                    </h5>
                    <p class="mb-0">${data.Justification}</p>
                    ${data.Referenced_Sections && data.Referenced_Sections.length > 0 ? `
                        <hr class="my-2">
                        <small class="text-muted">
                            <i class="bi bi-link-45deg me-1"></i>
                            Based on ${data.Referenced_Sections.length} referenced section(s)
                        </small>
                    ` : ''}
                </div>
            </div>
        `;
        
        this.resultSummaryEl.style.display = 'block';
    }

    updateParameterPreview(data) {
        if (!data.Extracted_Technical_Data) {
            this.parameterPreviewEl.style.display = 'none';
            return;
        }

        const parameters = Object.entries(data.Extracted_Technical_Data)
            .filter(([key, value]) => value && value !== 'Not Found');

        if (parameters.length === 0) {
            this.parameterPreviewEl.style.display = 'none';
            return;
        }

        this.parameterCardsEl.innerHTML = parameters.map(([key, value]) => {
            const displayName = key.replace(/_/g, ' ').replace(/([A-Z])/g, ' $1').trim();
            const [numValue, unit] = this.extractValueAndUnit(value);
            
            return `
                <div class="col-md-6 col-lg-3">
                    <div class="parameter-card interactive-hover">
                        <div class="parameter-name text-muted small">${displayName}</div>
                        <div class="parameter-value">${numValue}</div>
                        <div class="parameter-unit">${unit}</div>
                    </div>
                </div>
            `;
        }).join('');

        this.parameterPreviewEl.style.display = 'block';
    }

    extractValueAndUnit(value) {
        const match = value.match(/([0-9.]+)\s*([A-Za-z]*)/);
        if (match) {
            return [match[1], match[2] || ''];
        }
        return [value, ''];
    }

    updateStatus(text, type) {
        this.analysisStatusEl.textContent = text;
        this.analysisStatusEl.className = `badge bg-${type} status-${type}`;
    }

    hideResults() {
        this.resultSummaryEl.style.display = 'none';
        this.parameterPreviewEl.style.display = 'none';
        this.copyJsonEl.style.display = 'none';
        this.exportResultsEl.disabled = true;
    }

    async copyResults() {
        try {
            const textToCopy = this.isFormatted && this.formattedResultsEl.style.display !== 'none' 
                ? this.formattedResultsEl.textContent 
                : this.jsonOutputEl.textContent;

            await navigator.clipboard.writeText(textToCopy);
            
            const originalHtml = this.copyJsonEl.innerHTML;
            this.copyJsonEl.innerHTML = '<i class="bi bi-check me-1"></i>Copied!';
            this.copyJsonEl.classList.remove('btn-outline-secondary');
            this.copyJsonEl.classList.add('btn-success');
            
            setTimeout(() => {
                this.copyJsonEl.innerHTML = originalHtml;
                this.copyJsonEl.classList.remove('btn-success');
                this.copyJsonEl.classList.add('btn-outline-secondary');
            }, 2000);
        } catch (err) {
            console.error('Failed to copy:', err);
            this.showError('Failed to copy to clipboard');
        }
    }

    toggleFormat() {
        if (!this.currentResults) return;

        this.isFormatted = !this.isFormatted;
        
        if (this.isFormatted) {
            this.showFormattedResults();
            this.formatToggleEl.innerHTML = '<i class="bi bi-code-square me-1"></i>JSON';
            this.jsonOutputEl.style.display = 'none';
            this.formattedResultsEl.style.display = 'block';
        } else {
            this.formatToggleEl.innerHTML = '<i class="bi bi-file-text me-1"></i>Format';
            this.jsonOutputEl.style.display = 'block';
            this.formattedResultsEl.style.display = 'none';
        }
    }

    showFormattedResults() {
        const data = this.currentResults;
        const formatted = `
TECHNICAL COMPATIBILITY ANALYSIS REPORT
========================================

ANALYSIS DECISION: ${data.Decision}
CONFIDENCE LEVEL: ${data.Confidence_Score}

SUMMARY
-------
${data.Justification}

EXTRACTED TECHNICAL DATA
------------------------
${Object.entries(data.Extracted_Technical_Data || {})
    .map(([key, value]) => `${key.replace(/_/g, ' ')}: ${value}`)
    .join('\n')}

${data.Referenced_Sections && data.Referenced_Sections.length > 0 ? `
REFERENCED SECTIONS
------------------
${data.Referenced_Sections.map((section, index) => 
    `${index + 1}. ${section.section_name}\n   "${section.details}"`
).join('\n\n')}
` : ''}

ANALYSIS TIMESTAMP
-----------------
${new Date().toLocaleString()}
        `.trim();

        this.formattedResultsEl.innerHTML = `<pre class="json-output">${formatted}</pre>`;
    }

    exportResults() {
        if (!this.currentResults) return;

        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const filename = `tech-spec-analysis-${timestamp}.json`;
        
        const dataStr = JSON.stringify(this.currentResults, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = filename;
        link.click();
        
        URL.revokeObjectURL(link.href);
    }

    showError(message) {
        this.updateStatus('Error', 'danger');
        console.error(message);
        
        // Could implement toast notifications here
        alert(message);
    }
}

// Utility function for debouncing
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.techSpecAnalyzer = new TechSpecAnalyzer();
});

// Export for global access
window.TechSpecAnalyzer = TechSpecAnalyzer;