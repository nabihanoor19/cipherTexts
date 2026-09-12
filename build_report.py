from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

source = Path("report_source.md").read_text(encoding="utf-8")
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="SmallCode", parent=styles["BodyText"], fontName="Courier", fontSize=8.5, leading=11, spaceAfter=6))
styles["Title"].fontSize = 20
styles["Heading1"].spaceBefore = 12
styles["Heading2"].spaceBefore = 8

def inline_markup(text):
    escaped = escape(text)
    return escaped.replace("**", "<b>", 1).replace("**", "</b>", 1) if "**" in text else escaped

story = []
for line in source.splitlines():
    if not line.strip():
        story.append(Spacer(1, 6))
    elif line.startswith("# "):
        story.append(Paragraph(escape(line[2:]), styles["Title"]))
    elif line.startswith("## "):
        story.append(Paragraph(escape(line[3:]), styles["Heading1"]))
    elif line.startswith("### "):
        story.append(Paragraph(escape(line[4:]), styles["Heading2"]))
    elif line.startswith("- "):
        story.append(Paragraph("&bull; " + inline_markup(line[2:]), styles["BodyText"]))
    else:
        story.append(Paragraph(inline_markup(line), styles["BodyText"]))

doc = SimpleDocTemplate(
    "report.pdf",
    pagesize=LETTER,
    rightMargin=0.75 * inch,
    leftMargin=0.75 * inch,
    topMargin=0.7 * inch,
    bottomMargin=0.7 * inch,
    title="Offline Cryptography CTF Report",
)
doc.build(story)
