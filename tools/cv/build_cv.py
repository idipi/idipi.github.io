# -*- coding: utf-8 -*-
"""
Builds cv.pdf from cv_data.py.

Reconstructed from the original ReportLab-generated PDF by extracting its
content stream (fonts, sizes, colors, margins, leading) and rebuilding the
same layout with reportlab's own Paragraph/justify engine, so line-wrapping
and spacing match the source rather than approximating it in a different
typesetting engine.

Usage:
    python build_cv.py [output_path]
"""
import sys
import os
import subprocess
from pathlib import Path

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY

import cv_data as d

# ---------------------------------------------------------------- geometry
PAGE_W, PAGE_H = A4  # 595.276, 841.89
LEFT = 51.35433
RIGHT = 51.35433
CONTENT_W = PAGE_W - LEFT - RIGHT  # 492.567
BULLET_INDENT = 74.03 - LEFT       # 22.68
TOP_NAME_Y = 782.04

# ---------------------------------------------------------------- colors
C_NAME = (0.101961, 0.101961, 0.101961)      # #1A1A1A
C_SECTION = (0.239216, 0.239216, 0.239216)   # #3D3D3D
C_JOBTITLE = (0.101961, 0.101961, 0.101961)  # #1A1A1A
C_MUTED = (0.352941, 0.352941, 0.352941)     # #5A5A5A  (company/date, separators)
C_LINK = (0.239216, 0.419608, 0.313725)      # #3D6B50
C_BODY = (0.176471, 0.176471, 0.176471)      # #2D2D2D
C_RULE = (0.784314, 0.784314, 0.784314)      # #C8C8C8
C_PAGENUM = (0.666667, 0.666667, 0.666667)   # #AAAAAA

FONT_FILES = {
    "regular": "LiberationSans-Regular.ttf",
    "bold": "LiberationSans-Bold.ttf",
    "italic": "LiberationSans-Italic.ttf",
}
FONT_DIRS = [
    Path("/usr/share/fonts/truetype/liberation"),
    Path("/usr/share/fonts/truetype/liberation2"),
    Path("/Library/Fonts"),
    Path("/System/Library/Fonts"),
    Path.home() / "Library/Fonts",
]


def find_font_file(filename):
    for font_dir in FONT_DIRS:
        candidate = font_dir / filename
        if candidate.exists():
            return candidate

    fc_match = shutil_which("fc-match")
    if fc_match:
        try:
            result = subprocess.run(
                [fc_match, "-f", "%{file}", filename],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.SubprocessError:
            return None
        path = Path(result.stdout.strip())
        if path.exists():
            return path

    return None


def shutil_which(command):
    for path in os.environ.get("PATH", "").split(os.pathsep):
        candidate = Path(path) / command
        if candidate.exists() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


RESOLVED_FONTS = {style: find_font_file(filename) for style, filename in FONT_FILES.items()}
HAS_LIBERATION = all(RESOLVED_FONTS.values())

# ---------------------------------------------------------------- fonts
def register_fonts():
    if not HAS_LIBERATION:
        print(
            "Warning: Liberation Sans fonts were not found; using Helvetica fallback. "
            "Install fonts-liberation for the production layout.",
            file=sys.stderr,
        )
        return

    pdfmetrics.registerFont(TTFont("LiberationSans", str(RESOLVED_FONTS["regular"])))
    pdfmetrics.registerFont(TTFont("LiberationSans-Bold", str(RESOLVED_FONTS["bold"])))
    pdfmetrics.registerFont(TTFont("LiberationSans-Italic", str(RESOLVED_FONTS["italic"])))


F_REG = "LiberationSans" if HAS_LIBERATION else "Helvetica"
F_BOLD = "LiberationSans-Bold" if HAS_LIBERATION else "Helvetica-Bold"
F_ITALIC = "LiberationSans-Italic" if HAS_LIBERATION else "Helvetica-Oblique"

STYLE_BODY = ParagraphStyle(
    "body", fontName=F_REG, fontSize=9, leading=12, textColor="#2D2D2D",
    alignment=TA_JUSTIFY, spaceAfter=0,
)
STYLE_BULLET = ParagraphStyle(
    "bullet", parent=STYLE_BODY, leftIndent=BULLET_INDENT, firstLineIndent=0,
    bulletIndent=BULLET_INDENT - 12, spaceBefore=0,
)


def hexcolor(rgb):
    return "#%02X%02X%02X" % tuple(round(c * 255) for c in rgb)


def draw_line_segments(c, x, y, segments, font, size):
    """Draw consecutive text runs on one baseline, each its own color,
    with no gap - mirrors the original file's contact/meta lines."""
    c.setFont(font, size)
    cx = x
    for text, color in segments:
        c.setFillColor(hexcolor(color))
        c.drawString(cx, y, text)
        cx += c.stringWidth(text, font, size)
    return cx


def draw_paragraph(c, text, x, y, width, style):
    """Draws a justified Paragraph and returns the y just below it."""
    p = Paragraph(text, style)
    w, h = p.wrap(width, 1000)
    p.drawOn(c, x, y - h)
    return y - h


def section_header(c, title, y):
    c.setFont(F_BOLD, 10)
    c.setFillColor(hexcolor(C_SECTION))
    c.drawString(LEFT, y, title)
    rule_y = y - 5.33
    c.setLineWidth(0.5)
    c.setStrokeColor(hexcolor(C_RULE))
    c.line(LEFT, rule_y, LEFT + CONTENT_W, rule_y)
    return rule_y


def build(output_path):
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    register_fonts()
    c = canvas.Canvas(str(output), pagesize=A4)
    c.setTitle(d.PDF_TITLE)
    c.setSubject(d.PDF_SUBJECT)
    c.setAuthor(d.PDF_AUTHOR)

    # faint page number, top right (matches original)
    c.setFont(F_REG, 7.5)
    c.setFillColor(hexcolor(C_PAGENUM))
    c.drawString(346.9, 25.51, "1")

    # --- name
    c.setFont(F_BOLD, 17)
    c.setFillColor(hexcolor(C_NAME))
    c.drawString(LEFT, TOP_NAME_Y, d.NAME)

    # --- contact line (location · email(link) · site(link))
    # NB: uses middle-dot U+00B7, not bullet U+2022 - matches the glyph
    # width (333/1000 em) found in the original file's font subset.
    sep = "  \u00b7  "
    segs = [
        (d.LOCATION + "  ", C_MUTED),
        (sep, C_MUTED),
        (d.EMAIL, C_LINK),
        ("  ", C_MUTED),
        (sep, C_MUTED),
        (d.SITE, C_LINK),
    ]
    contact_y = 767.70
    x = LEFT
    positions = []  # (text, x0, x1, url) for link annotations
    cx = x
    c.setFont(F_REG, 8.5)
    for text, color in segs:
        c.setFillColor(hexcolor(color))
        c.drawString(cx, contact_y, text)
        w = c.stringWidth(text, F_REG, 8.5)
        positions.append((text, cx, cx + w))
        cx += w

    # clickable areas for email + site (skip the bullet separators)
    email_pos = positions[2]
    site_pos = positions[5]
    c.linkURL(d.EMAIL_LINK, (email_pos[1], contact_y - 1.5, email_pos[2], contact_y + 8.7), relative=0)
    c.linkURL(d.SITE_LINK, (site_pos[1], contact_y - 1.5, site_pos[2], contact_y + 8.7), relative=0)

    # --- summary
    y = draw_paragraph(c, d.SUMMARY, LEFT, 754.5, CONTENT_W, STYLE_BODY)

    # --- EXPERIENCE
    y = section_header(c, "EXPERIENCE", y - 15)
    y -= 12  # gap to first job title baseline

    for i, job in enumerate(d.EXPERIENCE):
        c.setFont(F_BOLD, 9.5)
        c.setFillColor(hexcolor(C_JOBTITLE))
        c.drawString(LEFT, y, job["title"])
        y -= 10.5
        c.setFont(F_ITALIC, 8.5)
        c.setFillColor(hexcolor(C_MUTED))
        c.drawString(LEFT, y, job["company"] + "   |   " + job["dates"])
        y -= 12
        for j, bullet_text in enumerate(job["bullets"]):
            html = "\u2022 " + bullet_text
            y2 = draw_paragraph(c, html, LEFT, y, CONTENT_W, STYLE_BULLET)
            y = y2 - (0 if j == len(job["bullets"]) - 1 else 3)
        if i != len(d.EXPERIENCE) - 1:
            y -= 14  # gap before next job title

    # --- TECHNICAL SKILLS
    y = section_header(c, "TECHNICAL SKILLS", y - 15)
    y -= 12
    label_x = LEFT
    value_x = 138.90
    for label, value in d.SKILLS:
        c.setFont(F_BOLD, 8.5)
        c.setFillColor(hexcolor(C_JOBTITLE))
        c.drawString(label_x, y, label)
        c.setFont(F_REG, 8.5)
        c.setFillColor(hexcolor(C_BODY))
        c.drawString(value_x, y, value)
        y -= 13.4

    # --- EDUCATION & LANGUAGES
    y = section_header(c, "EDUCATION & LANGUAGES", y + 13.4 - 15)
    y -= 12
    c.setFont(F_BOLD, 9)
    c.setFillColor(hexcolor(C_BODY))
    c.drawString(LEFT, y, d.EDUCATION_SCHOOL)
    w = c.stringWidth(d.EDUCATION_SCHOOL, F_BOLD, 9)
    c.setFont(F_REG, 9)
    c.drawString(LEFT + w, y, d.EDUCATION_DEGREE)
    y -= 14

    c.setFont(F_REG, 9)
    c.setFillColor(hexcolor(C_BODY))
    cx = LEFT
    for i, lang in enumerate(d.LANGUAGES):
        text = lang + ("  " if i < len(d.LANGUAGES) - 1 else "")
        c.drawString(cx, y, text)
        cx += c.stringWidth(text, F_REG, 9)
        if i < len(d.LANGUAGES) - 1:
            c.drawString(cx, y, "\u00b7")
            cx += c.stringWidth("\u00b7  ", F_REG, 9)

    c.showPage()
    c.save()


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "cv.pdf"
    build(out)
    print(f"Wrote {out}")
