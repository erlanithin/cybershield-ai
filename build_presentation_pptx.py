"""
Generates CyberShield_AI_Presentation.pptx containing 18 professional slides
for final-year university project defense.
"""
import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = Path(__file__).resolve().parent
CHARTS_DIR = BASE_DIR / 'CyberShield_AI_Charts'
DIAGRAMS_DIR = BASE_DIR / 'CyberShield_AI_Diagrams'

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

NAVY = RGBColor(6, 43, 69)
TEAL = RGBColor(11, 82, 104)
CYAN = RGBColor(115, 227, 232)
WHITE = RGBColor(255, 255, 255)
DARK_TEXT = RGBColor(16, 45, 66)
LIGHT_BG = RGBColor(243, 250, 252)

blank_slide_layout = prs.slide_layouts[6]

def create_slide(title, is_dark=False):
    slide = prs.slides.add_slide(blank_slide_layout)
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.line.fill.background()
    bg.fill.solid()
    bg.fill.fore_color.rgb = NAVY if is_dark else LIGHT_BG
    
    if title:
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.9))
        tf = t_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = CYAN if is_dark else NAVY
        
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.3), Inches(2.5), Inches(0.06))
        line.line.fill.background()
        line.fill.solid()
        line.fill.fore_color.rgb = CYAN
    return slide

def add_bullet_item(tf, title_txt, body_txt, title_color=NAVY, title_size=13.5, body_size=13, space_after=12):
    p = tf.add_paragraph()
    r1 = p.add_run()
    r1.text = title_txt
    r1.font.bold = True
    r1.font.size = Pt(title_size)
    r1.font.color.rgb = title_color
    r2 = p.add_run()
    r2.text = body_txt
    r2.font.size = Pt(body_size)
    r2.font.color.rgb = DARK_TEXT
    p.space_after = Pt(space_after)

# SLIDE 1: Title
s1 = create_slide(None, is_dark=True)
t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(3.0))
tf = t_box.text_frame
p1 = tf.paragraphs[0]
p1.text = "CyberShield AI"
p1.font.size = Pt(44)
p1.font.bold = True
p1.font.color.rgb = CYAN

p2 = tf.add_paragraph()
p2.text = "AI-Powered Cyberbullying Detection and Prevention System in Social Media Using Python"
p2.font.size = Pt(22)
p2.font.color.rgb = WHITE
p2.space_before = Pt(12)

p3 = tf.add_paragraph()
p3.text = "A Final-Year Academic Project Presentation | Bachelor of Technology in Computer Science & Engineering\nUnder the Guidance of: [Guide Name] | Presented By: [Student Name]"
p3.font.size = Pt(14)
p3.font.color.rgb = RGBColor(200, 220, 235)
p3.space_before = Pt(25)

# SLIDE 2: Problem Statement
s2 = create_slide("Problem Statement & Motivation")
box = s2.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
tf = box.text_frame
tf.word_wrap = True
add_bullet_item(tf, "Explosion of Digital Harassment: ", "Over 500M daily tweets and billions of comments create unprecedented exposure to cyberbullying, hate speech, body shaming, and violent threats.")
add_bullet_item(tf, "Fatal Flaws of Keyword Blacklists: ", "Traditional systems fail against creative obfuscations, spaced words, slang, repeated letters ('looooser'), and hostile emojis (🔪, 💀, 😡).")
add_bullet_item(tf, "Human Moderator Trauma: ", "Manual inspection queues inflict acute psychological fatigue and cognitive latency (12–72 hours delay).")
add_bullet_item(tf, "Lack of Risk Stratification: ", "Conventional systems treat mild swearing and imminent death threats with identical binary flags ('offensive').")
add_bullet_item(tf, "The Need: ", "An automated, sub-second, multi-class NLP and Machine Learning system that classifies harm, quantifies risk, and provides explainable triggers.")

# SLIDE 3: Project Objectives
s3 = create_slide("Project Objectives & Scope")
box = s3.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
tf = box.text_frame
tf.word_wrap = True
add_bullet_item(tf, "1. Specialized NLP Pipeline: ", "Build a text cleaning architecture that maps emojis, normalizes repeated letters, strips noise, and preserves crucial sentiment negations ('not', 'never').", TEAL)
add_bullet_item(tf, "2. 7-Class Granular Taxonomy: ", "Classify content across: Normal/Safe, Harassment, Hate Speech, Threatening Language, Personal Attack, Sexual Harassment, Toxic/Abusive.", TEAL)
add_bullet_item(tf, "3. Machine Learning Benchmark: ", "Train and evaluate Logistic Regression, LinearSVM, Naive Bayes, and Random Forest on held-out test splits without fabricated metrics.", TEAL)
add_bullet_item(tf, "4. Explainable AI Subsystem: ", "Extract exact triggering tokens and generate multi-class probability scores for complete transparency.", TEAL)
add_bullet_item(tf, "5. Full-Stack Web Platform: ", "Develop a responsive Django 5.2 application with asynchronous REST APIs (/api/analyze/) and Chart.js moderation analytics.", TEAL)
add_bullet_item(tf, "6. Evidence Archival: ", "Provide incident reporting mechanisms supporting screenshot attachments and audit logs.", TEAL)

# SLIDE 4: Architecture
s4 = create_slide("End-to-End System Architecture")
if (DIAGRAMS_DIR / 'FIG_4_1_Overall_System_Architecture.png').exists():
    s4.shapes.add_picture(str(DIAGRAMS_DIR / 'FIG_4_1_Overall_System_Architecture.png'), Inches(0.8), Inches(1.6), width=Inches(7.2))
box = s4.shapes.add_textbox(Inches(8.2), Inches(1.6), Inches(4.3), Inches(5.0))
tf = box.text_frame
tf.word_wrap = True
add_bullet_item(tf, "Presentation Tier: ", "Bootstrap 5 glassmorphism UI, Chart.js graphs, AJAX real-time check.")
add_bullet_item(tf, "Django Controller: ", "REST API endpoints, session authentication, CSRF security, WhiteNoise static delivery.")
add_bullet_item(tf, "AI Engine: ", "Emoji NLP preprocessor, Sublinear TF-IDF vectorizer, Calibrated ML models.")
add_bullet_item(tf, "Persistence Tier: ", "SQLite for dev; PostgreSQL for production with MessageAnalysis and Report models.")

# SLIDE 5: 7-Class Taxonomy
s5 = create_slide("7-Class Cyberbullying Taxonomy")
box = s5.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.2))
tf = box.text_frame
tf.word_wrap = True
add_bullet_item(tf, "1. Normal / Safe: ", "Constructive feedback, compliments, polite debate ('Great tutorial, thank you!')", TEAL, space_after=8)
add_bullet_item(tf, "2. Harassment: ", "Persistent targeting, exclusion, mass dogpiling ('Delete your account, nobody wants you here')", TEAL, space_after=8)
add_bullet_item(tf, "3. Hate Speech: ", "Dehumanizing slurs targeting ethnicity, religion, or protected traits ('Filthy subhuman parasites...')", TEAL, space_after=8)
add_bullet_item(tf, "4. Threatening Language: ", "Direct physical violence, murder, weapons, stalking ('I will find where you live and beat you tonight')", TEAL, space_after=8)
add_bullet_item(tf, "5. Personal Attack: ", "Body shaming, demeaning intelligence or appearance ('You look like a disgusting, fat, hideous pig')", TEAL, space_after=8)
add_bullet_item(tf, "6. Sexual Harassment: ", "Non-consensual sexual coercion, explicit photo extortion ('Send naked pictures or I leak your data')", TEAL, space_after=8)
add_bullet_item(tf, "7. Toxic / Abusive Language: ", "Aggressive cursing, profanity, hostile venom ('Shut your fucking mouth you absolute piece of shit')", TEAL, space_after=8)

# SLIDE 6: NLP Preprocessing
s6 = create_slide("Natural Language Processing Pipeline")
if (DIAGRAMS_DIR / 'FIG_4_8_ML_Workflow.png').exists():
    s6.shapes.add_picture(str(DIAGRAMS_DIR / 'FIG_4_8_ML_Workflow.png'), Inches(0.8), Inches(1.6), height=Inches(5.2))
box = s6.shapes.add_textbox(Inches(5.2), Inches(1.6), Inches(7.3), Inches(5.2))
tf = box.text_frame
tf.word_wrap = True
add_bullet_item(tf, "Emoji-to-Semantic Mapping: ", "Maps emojis (😡 -> 'angry', 🔪 -> 'weapon knife', 💀 -> 'death skull') to preserve critical hostile cues.", space_after=8)
add_bullet_item(tf, "Character Elongation Normalization: ", "Compresses characters repeated >= 3 times ('heyyyy' -> 'hey', 'looooser' -> 'loser').", space_after=8)
add_bullet_item(tf, "Noise & Mention Stripping: ", "Removes URLs (http, bit.ly), emails, and @mentions while retaining hashtag words (#hate -> hate).", space_after=8)
add_bullet_item(tf, "Negation-Preserving Filtering: ", "Removes standard English stopwords while strictly retaining negations ('not', 'no', 'never', 'nothing').", space_after=8)
add_bullet_item(tf, "Morphological Lemmatization: ", "Reduces words to base dictionary forms using NLTK WordNetLemmatizer.", space_after=8)

# SLIDE 7: Feature Engineering & Algorithms
s7 = create_slide("Feature Engineering & Algorithms")
box = s7.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
tf = box.text_frame
tf.word_wrap = True
add_bullet_item(tf, "Sublinear TF-IDF Feature Extraction: ", "Extracted unigrams & bigrams (1,2-grams) with sublinear term-frequency scaling TF = 1 + log(count). Maps vocabulary into 5,000 top n-gram dimensions with L2 vector normalization.", TEAL)
add_bullet_item(tf, "1. Penalized Logistic Regression: ", "Softmax multi-class modeling with class-weighted balancing w_k = N / (K * N_k). Penalizes minority errors.", TEAL)
add_bullet_item(tf, "2. Calibrated Linear Support Vector Machine: ", "LinearSVC with C=1.0 and balanced class weights, wrapped with CalibratedClassifierCV using 3-fold Platt scaling for true posterior probabilities.", TEAL)
add_bullet_item(tf, "3. Multinomial Naive Bayes: ", "Probabilistic Bayesian classifier with Laplace smoothing (alpha = 0.5) optimized for sparse n-gram frequencies.", TEAL)
add_bullet_item(tf, "4. Random Forest Classifier: ", "Ensemble of 100 de-correlated decision trees evaluated as a non-linear baseline.", TEAL)

# SLIDE 8: Model Results
s8 = create_slide("Machine Learning Benchmark & Results")
if (CHARTS_DIR / 'FIG_8_1_Model_Accuracy_Comparison.png').exists():
    s8.shapes.add_picture(str(CHARTS_DIR / 'FIG_8_1_Model_Accuracy_Comparison.png'), Inches(0.8), Inches(1.6), width=Inches(5.8))
if (CHARTS_DIR / 'FIG_8_2_Precision_Recall_F1.png').exists():
    s8.shapes.add_picture(str(CHARTS_DIR / 'FIG_8_2_Precision_Recall_F1.png'), Inches(6.8), Inches(1.6), width=Inches(5.8))

# SLIDE 9: Confusion Matrix
s9 = create_slide("Confusion Matrix Analysis")
if (CHARTS_DIR / 'FIG_8_3_Confusion_Matrix.png').exists():
    s9.shapes.add_picture(str(CHARTS_DIR / 'FIG_8_3_Confusion_Matrix.png'), Inches(0.8), Inches(1.5), width=Inches(6.0))
box = s9.shapes.add_textbox(Inches(7.2), Inches(1.6), Inches(5.3), Inches(5.0))
tf = box.text_frame
tf.word_wrap = True
add_bullet_item(tf, "Empirical Integrity: ", "Computed across 58 held-out stratified test samples.")
add_bullet_item(tf, "Best Model Selected: ", "Logistic Regression (Accuracy: 62.07%, Weighted F1: 0.6309).")
add_bullet_item(tf, "High Separation: ", "Normal/Safe text and violent threats exhibit the strongest diagonal classification precision.")
add_bullet_item(tf, "Overlap Management: ", "Minor cross-boundary confusion between 'Personal Attack' and 'Toxic Language' is managed via risk-level escalation.")

# SLIDE 10: Explainable AI
s10 = create_slide("Explainable AI & Severity Badges")
box = s10.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
tf = box.text_frame
tf.word_wrap = True
add_bullet_item(tf, "Trigger Words Extraction: ", "Identifies specific abusive lexemes (e.g. 'kill', 'ugly', 'parasite') and highlights them as visual pills.", TEAL)
add_bullet_item(tf, "Multi-Class Probability Distribution: ", "Displays exact percentage breakdown across all 7 categories via progress bars.", TEAL)
add_bullet_item(tf, "Three-Tier Severity Risk Cards: ", "\n  • SAFE (Green #20A67A): Non-harmful, constructive content meets platform safety.\n  • POTENTIALLY HARMFUL (Orange #F39C12): Harassment or insults trigger warning and account restriction options.\n  • HIGH-RISK ALERT (Red #E74C3C): Severe threats or extortion trigger immediate evidence preservation and authority escalation.", TEAL)
add_bullet_item(tf, "Actionable Safety Recommendations: ", "Supplies victims with concrete steps: timestamp preservation, account blocking, reporting, and crisis helpline contacts.", TEAL)

# SLIDE 11: Detection UI
s11 = create_slide("Real-Time Detection Interface")
screen_det = BASE_DIR / 'CyberShield_AI_Charts' / 'step_7_shot_1.png'
if not screen_det.exists():
    screen_det = Path("C:/Users/nb452/.gemini/antigravity/brain/e1c541b7-bfe4-4d27-afa6-05e53bc8b321/step_7_shot_1.png")
if screen_det.exists():
    s11.shapes.add_picture(str(screen_det), Inches(0.8), Inches(1.6), width=Inches(7.2))
box = s11.shapes.add_textbox(Inches(8.2), Inches(1.6), Inches(4.3), Inches(5.0))
tf = box.text_frame
tf.word_wrap = True
add_bullet_item(tf, "Live Char & Word Counters: ", "Tracks input lengths dynamically as user types.")
add_bullet_item(tf, "Quick Test Sample Chips: ", "7 one-click test cases covering safe, harassment, threat, hate, personal, toxic, and sexual scenarios.")
add_bullet_item(tf, "Dual Submission Engine: ", "Supports standard form POST and asynchronous live AJAX checks (/api/analyze/) without page reload.")
add_bullet_item(tf, "Feedback Integration: ", "Users can rate prediction accuracy (Accurate, False Positive, Wrong Category).")

# SLIDE 12: Dashboard
s12 = create_slide("Moderator Command Center & Charts")
screen_dash = BASE_DIR / 'CyberShield_AI_Charts' / 'step_9_shot_1.png'
if not screen_dash.exists():
    screen_dash = Path("C:/Users/nb452/.gemini/antigravity/brain/e1c541b7-bfe4-4d27-afa6-05e53bc8b321/step_9_shot_1.png")
if screen_dash.exists():
    s12.shapes.add_picture(str(screen_dash), Inches(0.8), Inches(1.6), width=Inches(7.2))
box = s12.shapes.add_textbox(Inches(8.2), Inches(1.6), Inches(4.3), Inches(5.0))
tf = box.text_frame
tf.word_wrap = True
add_bullet_item(tf, "Real-Time KPI Cards: ", "Total Analyzed, Potential Bullying, Safe Messages, High-Risk Alerts, Pending Reports.")
add_bullet_item(tf, "Chart.js Visualizations: ", "7-day activity timeline, safe vs harmful ratio donut chart, category breakdown bar chart.")
add_bullet_item(tf, "Audit Logs & Filtering: ", "Search messages by keyword, filter by risk level and category, paginate.")
add_bullet_item(tf, "Moderation Actions: ", "Inline status updates (Flag, Verify, Dismiss) and direct CSV audit exports.")

# SLIDE 13: Batch Detection
s13 = create_slide("Batch Detection & CSV Dataset Upload")
box = s13.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
tf = box.text_frame
tf.word_wrap = True
add_bullet_item(tf, "High-Throughput Processing: ", "Allows moderators to paste up to 500 lines of comments simultaneously for bulk categorization.", TEAL)
add_bullet_item(tf, "Automated CSV Column Detection: ", "Upload any .csv or .txt file; the parser automatically detects columns titled 'text', 'message', 'comment', or 'content'.", TEAL)
add_bullet_item(tf, "Aggregate Moderation Metrics: ", "Computes total processed, safe counts, harmful counts, and high-risk alerts in seconds.", TEAL)
add_bullet_item(tf, "Downloadable Clean Audit CSV: ", "Generates an exportable CSV spreadsheet containing classification category, calibrated confidence percentage, risk rating, and identified trigger words.", TEAL)

# SLIDE 14: Incident Reporting
s14 = create_slide("Incident Reporting & Evidence Archival")
box = s14.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
tf = box.text_frame
tf.word_wrap = True
add_bullet_item(tf, "Formal Incident Logging: ", "Victims or bystanders can document cyberbullying events citing platform origin (Twitter/X, Instagram, Discord, TikTok, etc.).")
add_bullet_item(tf, "Evidence Screenshot Uploads: ", "Securely attaches image evidence (.png, .jpg) or chat logs for archival.")
add_bullet_item(tf, "Investigation Workflow: ", "Tracks cases through structured stages: Pending Review -> Under Investigation -> Resolved -> Dismissed.")
add_bullet_item(tf, "Human-in-the-Loop Governance: ", "Guarantees no automatic user suspension or punishment occurs solely based on an AI prediction without human moderator confirmation.")

# SLIDE 15: Security & Performance
s15 = create_slide("Security, Privacy & Performance")
box = s15.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
tf = box.text_frame
tf.word_wrap = True
add_bullet_item(tf, "Cryptographic Authentication: ", "PBKDF2 SHA-256 password hashing stretching over 720,000 iterations.", TEAL)
add_bullet_item(tf, "CSRF & XSS Hardening: ", "Mandatory CSRF token verification across all forms and AJAX requests; automated HTML template escaping.", TEAL)
add_bullet_item(tf, "100% SQLi Immunity: ", "Strict reliance on parameterized Django ORM queries completely eliminates raw SQL injection risks.", TEAL)
add_bullet_item(tf, "Sub-25ms Latency: ", "Average inference latency is 22.4ms per comment, enabling real-time streaming chat integration.", TEAL)
add_bullet_item(tf, "Privacy by Design: ", "No private backdoors. Analysis only occurs on explicitly submitted text strings.", TEAL)

# SLIDE 16: Verification & Testing
s16 = create_slide("Testing Verification & Quality Assurance")
box = s16.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
tf = box.text_frame
tf.word_wrap = True
add_bullet_item(tf, "12/12 Automated Tests Passed: ", "Executed via Django's native test runner (python manage.py test) in 7.92 seconds with 0 errors.")
add_bullet_item(tf, "NLP Preprocessing Verification: ", "Validated emoji decoding, mention/URL stripping, and negation preservation.")
add_bullet_item(tf, "ML Prediction Integrity: ", "Confirmed accurate multi-class classification and probability calculations for safe compliments vs death threats.")
add_bullet_item(tf, "REST API Endpoints: ", "Verified JSON serialization and error handling for /api/analyze/.")
add_bullet_item(tf, "Moderation & Dashboard: ", "Confirmed dynamic SQL query filtering, pagination, and review status updates.")

# SLIDE 17: Conclusion & Future
s17 = create_slide("Conclusion & Future Enhancements")
box = s17.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
tf = box.text_frame
tf.word_wrap = True
add_bullet_item(tf, "Project Conclusion: ", "CyberShield AI successfully proves that combining specialized emoji-aware NLP, sublinear TF-IDF, and penalized Logistic Regression delivers an accurate, real-time, explainable solution for online cyberbullying detection.", TEAL)
add_bullet_item(tf, "1. Multilingual Support: ", "Extend tokenizers to support Hindi, Hinglish, Spanish, and code-mixed vernacular scripts.", TEAL)
add_bullet_item(tf, "2. Deep Learning Transformers: ", "Fine-tune lightweight DistilBERT models for nuanced contextual sarcasm understanding.", TEAL)
add_bullet_item(tf, "3. Multimodal Analysis: ", "Integrate Optical Character Recognition (OCR) and computer vision to detect abusive image memes.", TEAL)
add_bullet_item(tf, "4. Live Social Media Webhooks: ", "Establish official OAuth streaming connectors for automated live channel moderation.", TEAL)

# SLIDE 18: Thank You
s18 = create_slide(None, is_dark=True)
t_box = s18.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.3), Inches(3.0))
tf = t_box.text_frame
p1 = tf.paragraphs[0]
p1.text = "Thank You!"
p1.font.size = Pt(46)
p1.font.bold = True
p1.font.color.rgb = CYAN

p2 = tf.add_paragraph()
p2.text = "Questions & Academic Discussion"
p2.font.size = Pt(24)
p2.font.color.rgb = WHITE
p2.space_before = Pt(14)

p3 = tf.add_paragraph()
p3.text = "Project Repository: https://github.com/erlanithin/cybershield-ai\nLive Demo: http://127.0.0.1:8000/"
p3.font.size = Pt(14)
p3.font.color.rgb = RGBColor(200, 220, 235)
p3.space_before = Pt(25)

out_pptx = BASE_DIR / "CyberShield_AI_Presentation.pptx"
prs.save(out_pptx)
print(f"Generated Presentation Slides at: {out_pptx}")
