"""
Generates clean structural diagrams for Chapter 4 of the academic report.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DIAGRAMS_DIR = BASE_DIR / 'CyberShield_AI_Diagrams'
DIAGRAMS_DIR.mkdir(parents=True, exist_ok=True)

NAVY = '#062B45'
TEAL = '#0B5268'
CYAN = '#73E3E8'
BG = '#F3FAFC'
CARD_BG = '#E5F3F6'
RED = '#E74C3C'
GREEN = '#20A67A'

# 1. FIG 4.1 - Overall System Architecture
fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
ax.set_facecolor(BG)
fig.patch.set_facecolor('#FFFFFF')

# Draw layers
boxes = [
    ("CLIENT / PRESENTATION LAYER", ["Bootstrap 5 Responsive UI", "Chart.js Visualizations", "AJAX Detection Console", "Incident Reports & Feedback"], 0.76, TEAL),
    ("DJANGO BACKEND CONTROLLER LAYER", ["URL Routing (urls.py)", "Views & Services (services.py)", "REST API Endpoints (/api/analyze/)", "Auth & RBAC Middleware"], 0.52, NAVY),
    ("AI / MACHINE LEARNING ENGINE", ["NLP Preprocessor (clean_text)", "TF-IDF Vectorizer (1-2 n-grams)", "Logistic Regression Classifier", "Trigger Word Extraction & Explainability"], 0.28, TEAL),
    ("PERSISTENCE & STORAGE LAYER", ["SQLite (Dev) / PostgreSQL (Prod)", "MessageAnalysis Table", "CyberbullyingReport Table", "Serialized Model Artifacts (.pkl)"], 0.04, NAVY)
]

for title, items, y, color in boxes:
    rect = patches.FancyBboxPatch((0.08, y), 0.84, 0.18, boxstyle="round,pad=0.02",
                                  facecolor=CARD_BG, edgecolor=color, linewidth=2)
    ax.add_patch(rect)
    ax.text(0.12, y + 0.13, title, fontsize=11, fontweight='bold', color=color)
    content = "  •  ".join(items)
    ax.text(0.12, y + 0.05, content, fontsize=8.5, color='#102D42', wrap=True)

# Connecting arrows
for y in [0.74, 0.50, 0.26]:
    ax.annotate('', xy=(0.5, y), xytext=(0.5, y + 0.02),
                arrowprops=dict(arrowstyle="->", color=RED, lw=2.5))

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
ax.set_title('Figure 4.1: CyberShield AI Overall System Architecture', fontsize=13, fontweight='bold', color=NAVY, pad=15)
plt.tight_layout()
plt.savefig(DIAGRAMS_DIR / 'FIG_4_1_Overall_System_Architecture.png')
plt.close()

# 2. FIG 4.2 - DFD Level 0 (Context Diagram)
fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
ax.set_facecolor('#FFFFFF')

# User Entity
u_rect = patches.Rectangle((0.05, 0.35), 0.2, 0.3, facecolor='#E2E8F0', edgecolor=NAVY, lw=2)
ax.add_patch(u_rect)
ax.text(0.15, 0.5, "USER /\nMODERATOR", ha='center', va='center', fontweight='bold', color=NAVY)

# Central Process
p_circle = patches.Circle((0.5, 0.5), 0.18, facecolor=CARD_BG, edgecolor=TEAL, lw=2.5)
ax.add_patch(p_circle)
ax.text(0.5, 0.52, "0.0\nCYBERSHIELD AI\nDETECTION\nSYSTEM", ha='center', va='center', fontweight='bold', color=NAVY, fontsize=9)

# Database
d_rect = patches.Rectangle((0.75, 0.35), 0.2, 0.3, facecolor='#E2E8F0', edgecolor=NAVY, lw=2)
ax.add_patch(d_rect)
ax.text(0.85, 0.5, "DATABASE\n(SQLite /\nPostgreSQL)", ha='center', va='center', fontweight='bold', color=NAVY)

# Arrows
ax.annotate('Submit Text / Batch', xy=(0.32, 0.55), xytext=(0.25, 0.55), arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.8), fontsize=8, ha='center')
ax.annotate('Detection & Reports', xy=(0.25, 0.45), xytext=(0.32, 0.45), arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.8), fontsize=8, ha='center')
ax.annotate('Store Records', xy=(0.75, 0.55), xytext=(0.68, 0.55), arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.8), fontsize=8, ha='center')
ax.annotate('Query Analytics', xy=(0.68, 0.45), xytext=(0.75, 0.45), arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.8), fontsize=8, ha='center')

ax.set_xlim(0, 1)
ax.set_ylim(0.2, 0.8)
ax.axis('off')
ax.set_title('Figure 4.2: Data Flow Diagram Level 0 (Context Diagram)', fontsize=12, fontweight='bold', color=NAVY, pad=15)
plt.tight_layout()
plt.savefig(DIAGRAMS_DIR / 'FIG_4_2_DFD_Level_0.png')
plt.close()

# 3. FIG 4.8 - Machine Learning Workflow Diagram
fig, ax = plt.subplots(figsize=(7, 9), dpi=300)
steps = [
    "1. Labeled Dataset Collection (N=290 across 7 Classes)",
    "2. Text Cleaning (Decode Emojis, Strip URLs/Mentions)",
    "3. NLP Tokenization & Negation-Aware Stopword Filtering",
    "4. Morphological Lemmatization (NLTK WordNet)",
    "5. TF-IDF Feature Vectorization (Unigrams + Bigrams)",
    "6. Multi-Model Training (Logistic Reg., SVM, MNB, RF)",
    "7. Model Evaluation & Benchmark Comparison (F1, Accuracy)",
    "8. Best Production Model Serialization (joblib .pkl)",
    "9. Real-Time Inference (Class Probability & Triggers)",
    "10. 7-Class Cyberbullying & Risk Classification Result"
]

y_pos = [0.90 - i * 0.088 for i in range(len(steps))]
for i, (step, y) in enumerate(zip(steps, y_pos)):
    color = GREEN if i in [5, 7, 9] else TEAL
    rect = patches.FancyBboxPatch((0.1, y - 0.035), 0.8, 0.07, boxstyle="round,pad=0.015",
                                  facecolor=CARD_BG, edgecolor=color, linewidth=1.8)
    ax.add_patch(rect)
    ax.text(0.5, y, step, ha='center', va='center', fontsize=9, fontweight='bold', color=NAVY)
    if i < len(steps) - 1:
        ax.annotate('', xy=(0.5, y - 0.038), xytext=(0.5, y - 0.018),
                    arrowprops=dict(arrowstyle="<-", color=RED, lw=2))

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
ax.set_title('Figure 4.8: Machine Learning & NLP Workflow Architecture', fontsize=12, fontweight='bold', color=NAVY, pad=15)
plt.tight_layout()
plt.savefig(DIAGRAMS_DIR / 'FIG_4_8_ML_Workflow.png')
plt.close()

print("All architectural diagrams generated in CyberShield_AI_Diagrams/")
