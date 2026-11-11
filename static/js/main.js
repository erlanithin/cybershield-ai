/**
 * CyberShield AI - Core Frontend Interactivity & AJAX Engine
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Textarea character counter
    const messageInput = document.getElementById('message-input');
    const charCountEl = document.getElementById('char-count');
    const wordCountEl = document.getElementById('word-count');

    if (messageInput && (charCountEl || wordCountEl)) {
        const updateCounts = () => {
            const text = messageInput.value;
            if (charCountEl) charCountEl.textContent = text.length;
            if (wordCountEl) {
                const words = text.trim() ? text.trim().split(/\s+/).length : 0;
                wordCountEl.textContent = words;
            }
        };
        messageInput.addEventListener('input', updateCounts);
        updateCounts();
    }

    // 2. Sample text click to populate
    const samplePills = document.querySelectorAll('.sample-text-pill');
    samplePills.forEach(pill => {
        pill.addEventListener('click', (e) => {
            e.preventDefault();
            const sample = pill.getAttribute('data-sample');
            if (messageInput && sample) {
                messageInput.value = sample;
                messageInput.focus();
                if (charCountEl || wordCountEl) {
                    const evt = new Event('input');
                    messageInput.dispatchEvent(evt);
                }
                // Scroll smoothly to textarea
                messageInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    });

    // 3. AJAX Real-time Analysis (if enabled on page)
    const ajaxAnalyzeBtn = document.getElementById('btn-ajax-analyze');
    const liveResultContainer = document.getElementById('live-result-container');
    const analysisSpinner = document.getElementById('analysis-spinner');

    if (ajaxAnalyzeBtn && messageInput && liveResultContainer) {
        ajaxAnalyzeBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            const text = messageInput.value.trim();
            if (!text) {
                alert('Please enter or paste a message to analyze.');
                messageInput.focus();
                return;
            }

            // Show loading state
            if (analysisSpinner) analysisSpinner.classList.remove('d-none');
            ajaxAnalyzeBtn.disabled = true;

            try {
                const response = await fetch('/api/analyze/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({ message: text })
                });

                const data = await response.json();

                if (data.success) {
                    renderLiveAnalysisResult(data, liveResultContainer);
                    liveResultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                } else {
                    alert('Error: ' + (data.error || 'Failed to analyze text.'));
                }
            } catch (err) {
                console.error('Analysis error:', err);
                alert('An unexpected network error occurred while connecting to the AI detection engine.');
            } finally {
                if (analysisSpinner) analysisSpinner.classList.add('d-none');
                ajaxAnalyzeBtn.disabled = false;
            }
        });
    }

    // 4. AJAX Feedback submission
    const feedbackForm = document.getElementById('ajax-feedback-form');
    if (feedbackForm) {
        feedbackForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(feedbackForm);

            try {
                const res = await fetch('/feedback/submit/', {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: formData
                });
                const resData = await res.json();
                if (resData.success) {
                    const fbContainer = document.getElementById('feedback-card-body');
                    if (fbContainer) {
                        fbContainer.innerHTML = `
                            <div class="alert alert-success d-flex align-items-center gap-2 mb-0">
                                <i class="bi bi-check-circle-fill fs-5"></i>
                                <div>${resData.message}</div>
                            </div>
                        `;
                    }
                }
            } catch (err) {
                console.error('Feedback submit error:', err);
            }
        });
    }
});

/**
 * Helper to retrieve CSRF token cookie in Django
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Dynamically renders live analysis results in DOM
 */
function renderLiveAnalysisResult(data, container) {
    let cardClass = 'result-card-safe';
    let iconClass = 'bi-shield-check text-success';
    let riskBadge = '<span class="badge badge-safe"><i class="bi bi-check-circle me-1"></i> Safe Content</span>';

    if (data.risk_level === 'High-Risk Content') {
        cardClass = 'result-card-danger';
        iconClass = 'bi-exclamation-triangle-fill text-danger';
        riskBadge = '<span class="badge badge-high-risk"><i class="bi bi-shield-slash me-1"></i> High-Risk Alert</span>';
    } else if (data.risk_level === 'Potentially Harmful') {
        cardClass = 'result-card-warning';
        iconClass = 'bi-exclamation-circle-fill text-warning';
        riskBadge = '<span class="badge badge-warning"><i class="bi bi-exclamation-diamond me-1"></i> Potentially Harmful</span>';
    }

    let triggersHtml = '<span class="text-muted small">None detected</span>';
    if (data.trigger_words && data.trigger_words.length > 0) {
        triggersHtml = data.trigger_words.map(w => `<span class="trigger-word-pill">${escapeHtml(w)}</span>`).join(' ');
    }

    let recsHtml = '';
    if (data.recommendations && data.recommendations.length > 0) {
        recsHtml = data.recommendations.map(r => `<li class="mb-1"><i class="bi bi-arrow-right-circle text-primary me-2"></i>${escapeHtml(r)}</li>`).join('');
    }

    // Probability breakdown bars
    let probBars = '';
    if (data.probabilities) {
        for (const [cat, pct] of Object.entries(data.probabilities)) {
            probBars += `
                <div class="mb-2">
                    <div class="d-flex justify-content-between small mb-1">
                        <span class="fw-semibold">${escapeHtml(cat)}</span>
                        <span>${pct}%</span>
                    </div>
                    <div class="progress" style="height: 6px;">
                        <div class="progress-bar ${pct > 40 ? 'bg-danger' : 'bg-primary'}" role="progressbar" style="width: ${pct}%"></div>
                    </div>
                </div>
            `;
        }
    }

    container.innerHTML = `
        <div class="card card-white shadow-md p-4 ${cardClass} mb-4">
            <div class="d-flex flex-wrap justify-content-between align-items-center border-bottom pb-3 mb-3 gap-2">
                <div class="d-flex align-items-center gap-3">
                    <i class="bi ${iconClass} fs-1"></i>
                    <div>
                        <h4 class="mb-0 fw-bold">${escapeHtml(data.predicted_category)}</h4>
                        <div class="text-muted small">Confidence Score: <strong class="text-dark">${data.confidence_score}%</strong></div>
                    </div>
                </div>
                <div>${riskBadge}</div>
            </div>

            <div class="mb-3">
                <label class="text-muted small text-uppercase fw-bold">Original Message</label>
                <div class="p-3 bg-light rounded-3 border fst-italic">"${escapeHtml(data.original_text)}"</div>
            </div>

            <div class="mb-3">
                <label class="text-muted small text-uppercase fw-bold">Trigger Signals & High-Impact Terms</label>
                <div>${triggersHtml}</div>
            </div>

            <div class="mb-3">
                <label class="text-muted small text-uppercase fw-bold">AI Rationale & Linguistic Analysis</label>
                <p class="mb-0 text-dark">${escapeHtml(data.explanation)}</p>
            </div>

            <div class="row g-4 mt-1">
                <div class="col-md-7">
                    <div class="p-3 rounded-3" style="background: rgba(11, 82, 104, 0.05); border: 1px solid rgba(11, 82, 104, 0.1);">
                        <h6 class="fw-bold mb-2 text-primary"><i class="bi bi-shield-check me-2"></i>Recommended Next Steps</h6>
                        <ul class="list-unstyled mb-0 small">${recsHtml}</ul>
                    </div>
                </div>
                <div class="col-md-5">
                    <div class="p-3 rounded-3 bg-white border">
                        <h6 class="fw-bold mb-2 text-primary"><i class="bi bi-bar-chart-fill me-2"></i>Category Probabilities</h6>
                        ${probBars}
                    </div>
                </div>
            </div>

            <div class="mt-3 pt-2 border-top text-muted small text-end">
                <i class="bi bi-info-circle me-1"></i> ${escapeHtml(data.disclaimer)}
            </div>
        </div>
    `;
    container.classList.remove('d-none');
}

function escapeHtml(text) {
    if (!text) return '';
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
