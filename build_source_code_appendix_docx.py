"""
Generates CyberShield_AI_Source_Code_Appendix.docx containing complete, formatted
source code of all key modules for college project report submission.
"""
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

BASE_DIR = Path(__file__).resolve().parent
doc = Document()

# Set standard margins
for section in doc.sections:
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.2)
    section.right_margin = Inches(1.0)

COLOR_NAVY = RGBColor(6, 43, 69)
COLOR_TEAL = RGBColor(11, 82, 104)

p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_title.add_run("CYBERSHIELD AI - SOURCE CODE APPENDIX")
r.font.name = "Times New Roman"
r.font.size = Pt(18)
r.bold = True
r.font.color.rgb = COLOR_NAVY

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_sub = p_sub.add_run("Complete Core Source Code Implementation\nFinal-Year B.Tech Computer Science & Engineering Project")
r_sub.font.name = "Times New Roman"
r_sub.font.size = Pt(11)
r_sub.italic = True
p_sub.paragraph_format.space_after = Pt(25)

files_to_include = [
    ("1. ML Preprocessing Pipeline (ml_engine/preprocessing.py)", BASE_DIR / "ml_engine" / "preprocessing.py"),
    ("2. ML Model Training & Evaluation Engine (ml_engine/train_model.py)", BASE_DIR / "ml_engine" / "train_model.py"),
    ("3. Inference & Prediction Service (ml_engine/predict.py)", BASE_DIR / "ml_engine" / "predict.py"),
    ("4. Detection Database Models (detection/models.py)", BASE_DIR / "detection" / "models.py"),
    ("5. Detection Services & Analytics (detection/services.py)", BASE_DIR / "detection" / "services.py"),
    ("6. Detection Controllers & REST API (detection/views.py)", BASE_DIR / "detection" / "views.py"),
    ("7. Incident Reporting Models (reports/models.py)", BASE_DIR / "reports" / "models.py"),
    ("8. Incident Reporting Controllers (reports/views.py)", BASE_DIR / "reports" / "views.py"),
    ("9. User Profile & RBAC Models (accounts/models.py)", BASE_DIR / "accounts" / "models.py"),
    ("10. Django Core Configuration (config/settings.py)", BASE_DIR / "config" / "settings.py")
]

for title, file_path in files_to_include:
    if file_path.exists():
        p_sec = doc.add_paragraph()
        r_sec = p_sec.add_run(title)
        r_sec.font.name = "Times New Roman"
        r_sec.font.size = Pt(13)
        r_sec.bold = True
        r_sec.font.color.rgb = COLOR_TEAL
        p_sec.paragraph_format.space_before = Pt(14)
        p_sec.paragraph_format.space_after = Pt(4)

        with open(file_path, "r", encoding="utf-8") as f:
            code_text = f.read()

        p_code = doc.add_paragraph()
        p_code.paragraph_format.line_spacing = 1.0
        p_code.paragraph_format.space_after = Pt(10)
        # Background shading for code block
        pPr = p_code._p.get_or_add_pPr()
        shading = parse_xml(r'<w:shd {} w:fill="F3FAFC"/>'.format(nsdecls('w')))
        pPr.append(shading)

        r_code = p_code.add_run(code_text)
        r_code.font.name = "Consolas"
        r_code.font.size = Pt(8.0)
        r_code.font.color.rgb = RGBColor(20, 45, 65)

out_file = BASE_DIR / "CyberShield_AI_Source_Code_Appendix.docx"
doc.save(out_file)
print(f"Generated Source Code Appendix at: {out_file}")
