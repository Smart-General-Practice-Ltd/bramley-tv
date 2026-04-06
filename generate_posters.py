#!/usr/bin/env python3
"""
Generate two SMART Navigation marketing posters as PDF.
Clean straight-line sections, no diagonals. Matches wireframe layout.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
import os

# ── Colours ──
NAVY = HexColor('#0B2545')
DARK_BLUE = HexColor('#13315C')
BRAND_BLUE = HexColor('#1B4F8A')
TEAL = HexColor('#00A499')
WHITE = white
LIGHT_GREY = HexColor('#F5F7FA')
TEXT_GREY = HexColor('#6B7B8D')
CHECK_BLUE = HexColor('#2E7DD1')
CARD_BG = HexColor('#142d54')
MUTED = HexColor('#a0b4cc')
FOOTER_BG = HexColor('#0a1e3d')

W, H = A4  # 595.27 x 841.89 points
MARGIN = 40
CW = W - 2 * MARGIN  # content width


def draw_smart_logo(c, x, y, scale=1.0):
    """Draw the SMART navigation logo."""
    r = 28 * scale
    c.setFillColor(BRAND_BLUE)
    c.circle(x + r, y, r, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 11 * scale)
    c.drawCentredString(x + r, y - 4 * scale, "SMART")
    c.setFillColor(NAVY)
    c.setFont("Helvetica", 22 * scale)
    c.drawString(x + r * 2 + 8 * scale, y - 7 * scale, "navigation")
    c.setFont("Helvetica", 8 * scale)
    nav_w = pdfmetrics.stringWidth("navigation", "Helvetica", 22 * scale)
    c.drawString(x + r * 2 + 8 * scale + nav_w + 2, y + 4 * scale, "\u2122")


def draw_fuller_forbes(c, x, y, scale=1.0):
    """Draw Fuller and Forbes Healthcare Group text."""
    c.setFillColor(TEXT_GREY)
    c.setFont("Helvetica", 9 * scale)
    c.drawString(x, y + 5, "Fuller and Forbes")
    c.setFont("Helvetica-Bold", 9 * scale)
    c.drawString(x, y - 7, "Healthcare Group")


def draw_check_bullet(c, x, y, size=8):
    """Draw a blue check circle."""
    c.setFillColor(CHECK_BLUE)
    c.circle(x, y + 2, size, fill=1, stroke=0)
    c.setStrokeColor(WHITE)
    c.setLineWidth(1.5)
    c.line(x - 3.5, y + 1.5, x - 1, y - 1)
    c.line(x - 1, y - 1, x + 4, y + 5)


def draw_footer(c):
    """Draw the bottom footer bar with URL and logo - straight lines only."""
    # Tagline bar
    c.setFillColor(FOOTER_BG)
    c.rect(0, 35, W, 50, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-BoldOblique", 13)
    c.drawCentredString(W / 2, 55, "Safer triage. Less pressure on your practice.")

    # Bottom footer
    c.setFillColor(WHITE)
    c.rect(0, 0, W, 35, fill=1, stroke=0)
    c.setFillColor(TEXT_GREY)
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN, 13, "smartnavigation.co.uk")
    draw_fuller_forbes(c, W - 155, 8, scale=0.9)


def wrap_text(text, font, size, max_width):
    """Simple word-wrap."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = current + (" " if current else "") + word
        if pdfmetrics.stringWidth(test, font, size) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_section_line(c, y):
    """Draw a subtle horizontal separator."""
    c.setStrokeColor(HexColor('#1a3a6a'))
    c.setLineWidth(0.5)
    c.line(MARGIN, y, W - MARGIN, y)


# ═══════════════════════════════════════════════════════════════════
# POSTER 1: Pricing & Usage Data
# ═══════════════════════════════════════════════════════════════════

def create_poster1(filename):
    c = canvas.Canvas(filename, pagesize=A4)
    c.setTitle("SMART Navigation - Pricing & Usage")

    # ── WHITE HEADER ──
    header_bottom = H - 165
    c.setFillColor(WHITE)
    c.rect(0, header_bottom, W, H - header_bottom, fill=1, stroke=0)

    # Logo top-left
    draw_smart_logo(c, MARGIN + 5, H - 50, scale=1.15)

    # "Voice" sub-label
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN + 5, H - 82, "Voice")
    c.setFillColor(TEXT_GREY)
    c.setFont("Helvetica", 10.5)
    c.drawString(MARGIN + 47, H - 82, "AI-led telephone triage for primary care")

    # ── Stage 1 label ──
    c.setFillColor(LIGHT_GREY)
    c.roundRect(MARGIN, header_bottom + 10, CW, 38, 6, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(MARGIN + 14, header_bottom + 23, "Stage 1: Pricing")

    # ── NAVY MAIN SECTION (straight edge) ──
    c.setFillColor(NAVY)
    c.rect(0, 85, W, header_bottom - 85, fill=1, stroke=0)

    # ── Headline ──
    y = header_bottom - 30
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(W / 2, y, "Simple, transparent pricing")
    y -= 22
    c.setFillColor(TEAL)
    c.setFont("Helvetica", 15)
    c.drawCentredString(W / 2, y, "designed for NHS primary care")

    # ── Pricing card ──
    y -= 38
    card_h = 120
    c.setFillColor(CARD_BG)
    c.roundRect(MARGIN + 8, y - card_h, CW - 16, card_h, 10, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN + 26, y - 24, "Per-patient pricing model")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 11.5)
    c.drawString(MARGIN + 26, y - 42, "Scales with your practice list size")

    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN + 26, y - 68, "No setup fees  |  No long-term contracts")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(MARGIN + 26, y - 86, "Includes full onboarding, training & clinical support")
    c.drawString(MARGIN + 26, y - 102, "Month-to-month flexibility")

    # ── Usage & Adoption header ──
    y -= card_h + 28
    draw_section_line(c, y + 10)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(MARGIN + 8, y - 8, "Usage & Adoption")

    # ── Stat boxes (2x2 grid) ──
    y -= 32
    box_w = (CW - 30) / 2
    box_h = 68

    stats_row1 = [("120,000+", "Calls handled"), ("13", "GP sites live")]
    stats_row2 = [("98%", "Patient completion rate"), ("< 4 min", "Average call duration")]

    for row_i, stats in enumerate([stats_row1, stats_row2]):
        for col_i, (stat, label) in enumerate(stats):
            bx = MARGIN + 8 + col_i * (box_w + 14)
            by = y - box_h
            c.setFillColor(CARD_BG)
            c.roundRect(bx, by, box_w, box_h, 10, fill=1, stroke=0)
            c.setFillColor(TEAL)
            c.setFont("Helvetica-Bold", 28)
            c.drawCentredString(bx + box_w / 2, by + box_h - 28, stat)
            c.setFillColor(MUTED)
            c.setFont("Helvetica", 12)
            c.drawCentredString(bx + box_w / 2, by + 12, label)
        y -= box_h + 12

    # ── Stage 2: AVT section ──
    y -= 10
    draw_section_line(c, y + 8)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(MARGIN + 8, y - 10, "Stage 2: Automated Voice Triage (AVT)")

    y -= 32
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 11.5)
    desc_lines = [
        "AI-powered voice agent handles patient calls 24/7,",
        "guiding them through clinician-designed triage pathways.",
    ]
    for line in desc_lines:
        c.drawString(MARGIN + 8, y, line)
        y -= 16

    y -= 6
    avt_bullets = [
        "Handles overflow and out-of-hours calls automatically",
        "Same clinically-safe pathways used by receptionists",
        "Seamless handoff to human staff when needed",
    ]
    for bullet in avt_bullets:
        c.setFillColor(TEAL)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(MARGIN + 12, y + 1, "\u25CF")
        c.setFillColor(HexColor('#c0d0e0'))
        c.setFont("Helvetica", 10.5)
        c.drawString(MARGIN + 24, y, bullet)
        y -= 15

    # ── Footer ──
    draw_footer(c)

    c.save()
    print(f"Created: {filename}")


# ═══════════════════════════════════════════════════════════════════
# POSTER 2: EMIS Partner & Case Study
# ═══════════════════════════════════════════════════════════════════

def create_poster2(filename):
    c = canvas.Canvas(filename, pagesize=A4)
    c.setTitle("SMART Navigation - EMIS Partner & Case Study")

    # ── WHITE HEADER ──
    header_bottom = H - 190
    c.setFillColor(WHITE)
    c.rect(0, header_bottom, W, H - header_bottom, fill=1, stroke=0)

    # Logo
    draw_smart_logo(c, MARGIN + 5, H - 50, scale=1.15)

    # Sub label
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN + 5, H - 82, "Voice")
    c.setFillColor(TEXT_GREY)
    c.setFont("Helvetica", 10.5)
    c.drawString(MARGIN + 47, H - 82, "Clinician-designed AI telephone triage")

    # ── EMIS Partner badge ──
    badge_y = H - 120
    c.setFillColor(BRAND_BLUE)
    c.roundRect(MARGIN + 30, badge_y - 48, CW - 60, 42, 8, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(W / 2, badge_y - 32, "EMIS Partner API  \u2014  Fully Integrated")

    # ── NAVY MAIN SECTION (straight edge) ──
    c.setFillColor(NAVY)
    c.rect(0, 85, W, header_bottom - 85, fill=1, stroke=0)

    # ── Case Study headline ──
    y = header_bottom - 28
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(W / 2, y, "Case Study")

    y -= 22
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 12)
    c.drawCentredString(W / 2, y, "Real-world impact from a multi-site GP practice")

    # ── Big stat: 43% ──
    y -= 55
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 68)
    c.drawCentredString(W / 2, y, "43%")

    y -= 24
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(W / 2, y, "reduction in receptionist call handling time")

    y -= 18
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 11)
    c.drawCentredString(W / 2, y, "across 13 sites after deploying SMART Navigation Voice")

    # ── 3 stat boxes ──
    y -= 38
    box_w = (CW - 40) / 3
    box_h = 65
    stats = [
        ("92%", "Patient", "satisfaction"),
        ("3.2 min", "Avg call", "duration"),
        ("24/7", "Availability", ""),
    ]
    for i, (stat, line1, line2) in enumerate(stats):
        bx = MARGIN + 8 + i * (box_w + 12)
        c.setFillColor(CARD_BG)
        c.roundRect(bx, y - box_h, box_w, box_h, 10, fill=1, stroke=0)
        c.setFillColor(TEAL)
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(bx + box_w / 2, y - 25, stat)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 10)
        c.drawCentredString(bx + box_w / 2, y - 42, line1)
        if line2:
            c.drawCentredString(bx + box_w / 2, y - 54, line2)

    # ── Bullet Point Overview ──
    y -= box_h + 22
    draw_section_line(c, y + 8)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(MARGIN + 8, y - 8, "Overview")

    y -= 32
    bullets = [
        ("AI-led patient triage",
         "Patients speak directly to the system which guides them through safe navigation questions."),
        ("Reduce reception pressure",
         "Free staff from lengthy triage calls, allowing them to focus on in-practice patient care."),
        ("Consistent, structured outcomes",
         "Every patient assessed using the same safe, clinician-designed pathways."),
        ("Built for NHS primary care",
         "Designed around real GP workflows with EMIS integration and clinical governance built in."),
        ("EMIS Partner API integration",
         "Seamless read/write access to patient records, appointments, and clinical data."),
    ]

    for title, desc in bullets:
        draw_check_bullet(c, MARGIN + 18, y + 2, 7)

        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(MARGIN + 32, y, title)

        y -= 16
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 10)
        wrapped = wrap_text(desc, "Helvetica", 10, CW - 45)
        for line in wrapped:
            c.drawString(MARGIN + 32, y, line)
            y -= 13
        y -= 10

    # ── Footer ──
    draw_footer(c)

    c.save()
    print(f"Created: {filename}")


if __name__ == "__main__":
    outdir = "/home/user/bramley-tv"
    create_poster1(os.path.join(outdir, "smartnav-poster-pricing.pdf"))
    create_poster2(os.path.join(outdir, "smartnav-poster-case-study.pdf"))
    print("Done! Both posters generated.")
