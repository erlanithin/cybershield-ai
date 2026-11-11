# CyberShield AI — AI-Powered Cyberbullying Detection & Prevention System

![Python](https://img.shields.io/badge/Python-3.14%20%7C%203.11%2B-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2-green.svg)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.9-orange.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)
![License](https://img.shields.io/badge/License-MIT-teal.svg)

**CyberShield AI** is a full-stack, enterprise-grade AI cyberbullying detection and moderation platform built with Python, Django, Natural Language Processing (NLP), and Scikit-Learn. It analyzes social media comments, chat messages, and forum discussions to classify online toxicity, protect digital citizens, and assist moderators in upholding safe online communities.

---

## 🎨 UI/UX Design System & Color Palette

Designed following a modern cybersecurity visual theme with glassmorphism dashboard cards, gradient hero sections, and high-contrast accessibility:

- **Primary**: `#062B45` (Deep Navy)
- **Secondary**: `#0B5268` (Teal Slate)
- **Accent**: `#73E3E8` (Cyber Cyan)
- **Background**: `#F3FAFC` (Clean Light Ice)
- **Card Background**: `#E5F3F6` (Glass Ice)
- **Text Primary**: `#102D42`
- **Danger (High-Risk)**: `#E74C3C`
- **Warning (Harmful)**: `#F39C12`
- **Success (Safe)**: `#20A67A`

---

## 🌟 Key Features

1. **Real-Time Single Text Analysis**:
   - Sub-second inference evaluating input text for hostility, slurs, and threats.
   - Outputs: Predicted Category, Calibrated Confidence Score, Risk Rating (Safe, Potentially Harmful, High-Risk), Key Trigger Signals, Transparent AI Rationale, and Actionable Recommended Next Steps.
   - Interactive sample pills for immediate one-click testing.
   - REST API endpoint (`/api/analyze/`) with asynchronous AJAX capability.

2. **Multi-Class NLP Classification (7 Categories)**:
   - `Normal / Safe`
   - `Harassment`
   - `Hate Speech`
   - `Threatening Language`
   - `Personal Attack`
   - `Sexual Harassment`
   - `Toxic / Abusive Language`

3. **Batch Message & CSV Upload Processing**:
   - Analyze hundreds of comments simultaneously either via multi-line text blocks or direct `.csv` / `.txt` dataset file upload.
   - Instant aggregate metric summaries and one-click downloadable audit CSV reports.

4. **Moderator & Admin Command Dashboard**:
   - Interactive **Chart.js** data visualizations:
     - 7-Day Daily Detection Activity Timeline.
     - Safe vs Harmful Ratio Doughnut Chart.
     - Bullying Category Distribution Bar Chart.
   - Detection history moderation table with:
     - Search by message keywords.
     - Filter by risk level, category, and review status.
     - Pagination.
     - Direct CSV export for audit trails.
     - Inline review status updates (`Unreviewed`, `Flagged`, `Verified`, `Dismissed`).

5. **Empirical Model Performance Analytics**:
   - Displays genuine evaluation metrics computed during machine learning training:
     - Test Accuracy, Weighted F1-Score, Macro Precision & Recall.
     - Multi-Model Benchmark (Logistic Regression, Multinomial Naive Bayes, Calibrated Linear SVM, Random Forest).
     - Full 7x7 Multi-Class Confusion Matrix Heatmap.
     - Per-category Precision, Recall, and F1-Score breakdown.

6. **Cyberbullying Incident Reporting System**:
   - File formal reports citing offensive messages, social platforms (Twitter/X, Instagram, Discord, TikTok, etc.), incident descriptions, and screenshot evidence.
   - Track case status (`Pending`, `Under Investigation`, `Resolved`, `Dismissed`).
   - Moderator case notes and resolution logging.

7. **User Authentication & Role-Based Access (RBAC)**:
   - Built on Django's native authentication framework.
   - Custom `UserProfile` with role assignment (`user`, `moderator`, `admin`).
   - User profile management and personal detection history archive.

---

## 🏗️ Project Architecture

```
cyberbullying_detection/
│
├── manage.py                     # Django management CLI
├── requirements.txt              # Project dependencies
├── README.md                     # Documentation & setup guide
│
├── config/                       # Project configuration
│   ├── settings.py               # Django settings, security & app declarations
│   ├── urls.py                   # Master URL routing
│   └── wsgi.py                   # WSGI deployment gateway
│
├── ml_engine/                    # Machine Learning & NLP core
│   ├── preprocessing.py          # Emojis, slang, URLs, punctuation, lemmatization
│   ├── train_model.py            # Dataset curation, multi-model training & evaluation
│   ├── predict.py                # Single & batch inference, triggers, explainability
│   └── evaluate.py               # Metrics extraction and confusion matrix loader
│
├── detection/                    # Core Detection application
│   ├── models.py                 # MessageAnalysis & Feedback models
│   ├── views.py                  # Single/batch views, REST API, dashboard, CSV export
│   ├── services.py               # Analysis persistence, analytics aggregation, CSV exporter
│   ├── forms.py                  # SingleMessage, Batch, CSV Upload, Feedback forms
│   ├── urls.py                   # Detection app URL routes
│   ├── admin.py                  # Django Admin customization
│   └── context_processors.py     # Global platform health stats for all views
│
├── accounts/                     # Authentication & User Management
│   ├── models.py                 # UserProfile with RBAC
│   ├── views.py                  # Register, Login, Logout, Profile views
│   ├── forms.py                  # Registration and profile forms
│   └── management/commands/
│       └── seed_data.py          # Database seeder with admin & sample data
│
├── reports/                      # Cyberbullying Incident Reporting
│   ├── models.py                 # CyberbullyingReport model
│   ├── views.py                  # Report creation, listing, detail & status update
│   ├── forms.py                  # CyberbullyingReportForm & ReportStatusUpdateForm
│   └── urls.py                   # Reports URL routing
│
├── templates/                    # HTML5 / Bootstrap 5 templates
│   ├── base.html                 # Navigation, alerts, footer layout
│   ├── home.html                 # Landing page (Hero, Features, How it works, Preview, Why us)
│   ├── detection.html            # Interactive detection console
│   ├── batch_detection.html      # Batch and CSV upload interface
│   ├── dashboard.html            # Moderator & Admin Analytics Dashboard
│   ├── model_analytics.html      # True ML evaluation & Confusion Matrix
│   ├── reports.html              # Incident reports listing
│   ├── report_create.html        # Incident report submission form
│   ├── report_detail.html        # Incident report case detail & moderator controls
│   ├── login.html                # Sign in page
│   ├── register.html             # User registration page
│   ├── profile.html              # User profile & bio management
│   └── user_dashboard.html       # Personal analysis history
│
├── static/
│   ├── css/style.css             # Custom CyberShield design system
│   └── js/main.js                # Character counts, AJAX inference, Chart.js configs
│
├── datasets/
│   └── cyberbullying_dataset.csv # Labeled 7-class training dataset
│
└── models/
    ├── cyberbullying_model.pkl   # Serialized best ML classifier (joblib)
    ├── tfidf_vectorizer.pkl      # Trained TF-IDF vectorizer (joblib)
    └── model_metrics.json        # True evaluation metrics & confusion matrix
```

---

## 🚀 Quickstart Installation & Execution

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Git

### 2. Clone Repository & Setup Virtual Environment
```bash
git clone <repository-url>
cd "detection of cyberbulling"

# Optional: Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Train Models & Verify Artifacts
```bash
python -m ml_engine.train_model
```
*This generates `datasets/cyberbullying_dataset.csv`, trains 4 classifiers (Logistic Regression, Naive Bayes, Linear SVM, Random Forest), selects the best-performing model, and saves artifacts into `models/`.*

### 5. Apply Database Migrations
```bash
python manage.py makemigrations accounts detection reports
python manage.py migrate
```

### 6. Seed Demo Data & Admin Account
```bash
python manage.py seed_data
```
This automatically provisions:
- **Admin**: `admin` / `admin123`
- **Moderator**: `moderator_alice` / `moderator123`
- **Standard User**: `john_doe` / `user1234`
- 18+ realistic sample analyses spread across the past 7 days.
- 4 sample incident reports across Instagram, Discord, WhatsApp, and YouTube.

### 7. Run the Local Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 🧪 Running Automated Tests
Run the comprehensive test suite verifying NLP preprocessing, inference accuracy, view routing, database operations, and REST APIs:

```bash
python manage.py test
```

---

## 📡 REST API Reference

### Real-Time Text Analysis Endpoint
- **URL**: `/api/analyze/`
- **Method**: `POST`
- **Content-Type**: `application/json`

#### Request Payload:
```json
{
  "message": "I will find where you live and beat you bloody tonight."
}
```

#### Response Example:
```json
{
  "success": true,
  "original_text": "I will find where you live and beat you bloody tonight.",
  "cleaned_text": "find live beat bloody tonight",
  "predicted_category": "Threatening Language",
  "confidence_score": 88.5,
  "risk_level": "High-Risk Content",
  "badge_class": "badge-high-risk",
  "color_hex": "#E74C3C",
  "severity_rank": 3,
  "trigger_words": ["beat"],
  "explanation": "The AI model identified direct or implied physical harm, violence, or intimidation...",
  "recommendations": [
    "Do not engage or respond to the aggressor directly.",
    "Take immediate screenshots with visible timestamps and username handles.",
    "File an urgent report with the platform safety team and consider law enforcement if physical danger is imminent.",
    "Block the sender across all communication channels."
  ],
  "disclaimer": "Predictions are AI-generated indicators to assist human review, not definitive legal judgments."
}
```

---

## 🛡️ Security & Privacy Architecture
- **CSRF Protection**: All form submissions and state-changing actions are guarded with Django CSRF tokens.
- **SQL Injection Prevention**: 100% ORM-parameterized database queries.
- **XSS Prevention**: Automatic HTML template escaping, safe DOM insertion, and input sanitation.
- **Zero Sarcastic / Fabricated Metrics**: True metrics computed and serialized from actual stratified test splits.
- **Human-in-the-Loop AI**: Clear disclaimers stating predictions are indicators for review rather than automatic punishment.

---

## 📄 License
This project is open-source under the MIT License.
