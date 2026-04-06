#!/usr/bin/env python3
"""
Generate two SMART Navigation marketing posters as PDF.
Straight lines. Alternating white / blue (#1159A2) sections.
Only black and white text. No green/teal.
Layout: top bar, two large sections, bottom bar.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
import os

# ── Colours ──
BLUE = HexColor('#1159A2')
DARK_BLUE = HexColor('#0d4a8a')
NAVY = HexColor('#0B2545')
WHITE = white
BLACK = black
LIGHT_GREY = HexColor('#F0F3F7')
MID_GREY = HexColor('#666666')
LOGO_BLUE = HexColor('#1159A2')

W, H = A4
MARGIN = 40
CW = W - 2 * MARGIN


def draw_smart_logo(c, x, y, scale=1.0, dark_bg=False):
    """Logo: blue circle with SMART in white, 'navigation' beside it."""
    r = 26 * scale
    # Circle
    c.setFillColor(LOGO_BLUE if not dark_bg else WHITE)
    c.circle(x + r, y, r, fill=1, stroke=0)
    # SMART inside circle
    c.setFillColor(WHITE if not dark_bg else LOGO_BLUE)
    c.setFont("Helvetica-Bold", 10.5 * scale)
    c.drawCentredString(x + r, y - 3.5 * scale, "SMART")
    # 'navigation' text
    c.setFillColor(BLACK if not dark_bg else WHITE)
    c.setFont("Helvetica", 20 * scale)
    c.drawString(x + r * 2 + 7 * scale, y - 6.5 * scale, "navigation")
    # TM
    c.setFont("Helvetica", 7 * scale)
    nav_w = pdfmetrics.stringWidth("navigation", "Helvetica", 20 * scale)
    c.drawString(x + r * 2 + 7 * scale + nav_w + 2, y + 3 * scale, "\u2122")


def draw_fuller_forbes(c, x, y, dark_bg=False):
    col = WHITE if dark_bg else MID_GREY
    c.setFillColor(col)
    c.setFont("Helvetica", 9)
    c.drawString(x, y + 5, "Fuller and Forbes")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x, y - 7, "Healthcare Group")


def draw_check_bullet(c, x, y, size=7, dark_bg=False):
    """Draw a white or blue check circle."""
    if dark_bg:
        c.setFillColor(WHITE)
        check_col = BLUE
    else:
        c.setFillColor(BLUE)
        check_col = WHITE
    c.circle(x, y + 2, size, fill=1, stroke=0)
    c.setStrokeColor(check_col)
    c.setLineWidth(1.5)
    c.line(x - 3, y + 1.5, x - 0.5, y - 0.5)
    c.line(x - 0.5, y - 0.5, x + 3.5, y + 4.5)


def wrap_text(text, font, size, max_width):
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


# ═══════════════════════════════════════════════════════════════════
# POSTER 1: Pricing & Usage Data
# ═══════════════════════════════════════════════════════════════════

def create_poster1(filename):
    c = canvas.Canvas(filename, pagesize=A4)
    c.setTitle("SMART Navigation - Pricing & Usage")

    # ────────────────────────────────────────────
    # TOP BAR - White with logo
    # ────────────────────────────────────────────
    top_bar_h = 80
    top_bar_bottom = H - top_bar_h
    c.setFillColor(WHITE)
    c.rect(0, top_bar_bottom, W, top_bar_h, fill=1, stroke=0)
    draw_smart_logo(c, MARGIN + 5, H - 45, scale=1.1)

    # ────────────────────────────────────────────
    # SECTION 1 - BLUE: Pricing
    # ────────────────────────────────────────────
    sec1_top = top_bar_bottom
    sec1_bottom = H / 2 + 20  # roughly upper half
    sec1_h = sec1_top - sec1_bottom
    c.setFillColor(BLUE)
    c.rect(0, sec1_bottom, W, sec1_h, fill=1, stroke=0)

    y = sec1_top - 28
    # Section label
    c.setFillColor(HexColor('#ffffff80'))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN + 8, y, "STAGE 1: PRICING")

    y -= 35
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(MARGIN + 8, y, "Simple, transparent pricing")
    y -= 22
    c.setFont("Helvetica", 14)
    c.drawString(MARGIN + 8, y, "designed for NHS primary care")

    # Price highlight
    y -= 45
    # White rounded box for price
    c.setFillColor(HexColor('#ffffff18'))
    c.roundRect(MARGIN + 8, y - 85, CW - 16, 85, 10, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 42)
    c.drawString(MARGIN + 24, y - 38, "\u00a31,000")
    c.setFont("Helvetica", 16)
    c.drawString(MARGIN + 210, y - 30, "for 12 months")

    c.setFont("Helvetica", 12)
    c.drawString(MARGIN + 24, y - 58, "Per practice, all-inclusive. No hidden charges. No auto-renewals.")
    c.drawString(MARGIN + 24, y - 74, "Includes full onboarding, training & clinical support.")

    # ────────────────────────────────────────────
    # SECTION 2 - WHITE: Usage & Data
    # ────────────────────────────────────────────
    sec2_top = sec1_bottom
    sec2_bottom = 80  # leave room for footer
    c.setFillColor(WHITE)
    c.rect(0, sec2_bottom, W, sec2_top - sec2_bottom, fill=1, stroke=0)

    y = sec2_top - 28
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN + 8, y, "USAGE & ADOPTION")

    y -= 32

    # Stats boxes - 2x2 grid
    box_w = (CW - 24) / 2
    box_h = 62

    stats_row1 = [("152,508", "Patients triaged (2024\u201325)"), ("40+", "Practices nationally")]
    stats_row2 = [("\u00a34.7M", "NHS savings in 12 months"), ("71 hrs/wk", "GP time saved")]

    for stats in [stats_row1, stats_row2]:
        for col_i, (stat, label) in enumerate(stats):
            bx = MARGIN + 4 + col_i * (box_w + 16)
            by = y - box_h
            c.setFillColor(BLUE)
            c.roundRect(bx, by, box_w, box_h, 8, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 26)
            c.drawCentredString(bx + box_w / 2, by + box_h - 26, stat)
            c.setFont("Helvetica", 10)
            c.drawCentredString(bx + box_w / 2, by + 10, label)
        y -= box_h + 10

    # Stage 2: AVT
    y -= 14
    c.setStrokeColor(HexColor('#d0d8e0'))
    c.setLineWidth(0.5)
    c.line(MARGIN, y + 8, W - MARGIN, y + 8)

    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(MARGIN + 8, y - 8, "Stage 2: Automated Voice Triage (AVT)")

    y -= 30
    c.setFillColor(MID_GREY)
    c.setFont("Helvetica", 11)
    c.drawString(MARGIN + 8, y, "AI-powered voice agent handles patient calls 24/7,")
    y -= 15
    c.drawString(MARGIN + 8, y, "guiding them through clinician-designed triage pathways.")

    y -= 20
    avt_bullets = [
        "Handles overflow and out-of-hours calls automatically",
        "Same clinically-safe pathways used by receptionists",
        "Seamless handoff to human staff when needed",
    ]
    for bullet in avt_bullets:
        c.setFillColor(BLUE)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(MARGIN + 12, y + 1, "\u25cf")
        c.setFillColor(BLACK)
        c.setFont("Helvetica", 10.5)
        c.drawString(MARGIN + 24, y, bullet)
        y -= 15

    # ────────────────────────────────────────────
    # BOTTOM BAR - Blue
    # ────────────────────────────────────────────
    c.setFillColor(BLUE)
    c.rect(0, 0, W, 80, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-BoldOblique", 13)
    c.drawCentredString(W / 2, 48, "Safer triage. Less pressure on your practice.")
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN, 18, "smartnavigation.co.uk")
    draw_fuller_forbes(c, W - 155, 13, dark_bg=True)

    c.save()
    print(f"Created: {filename}")


# ═══════════════════════════════════════════════════════════════════
# POSTER 2: Case Study & Overview
# ═══════════════════════════════════════════════════════════════════

def create_poster2(filename):
    c = canvas.Canvas(filename, pagesize=A4)
    c.setTitle("SMART Navigation - Case Study & Overview")

    # ────────────────────────────────────────────
    # TOP BAR - White with logo + EMIS badge
    # ────────────────────────────────────────────
    top_bar_h = 105
    top_bar_bottom = H - top_bar_h
    c.setFillColor(WHITE)
    c.rect(0, top_bar_bottom, W, top_bar_h, fill=1, stroke=0)
    draw_smart_logo(c, MARGIN + 5, H - 42, scale=1.1)

    # EMIS badge
    badge_y = H - 75
    c.setFillColor(BLUE)
    c.roundRect(MARGIN + 25, badge_y - 22, CW - 50, 28, 6, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(W / 2, badge_y - 14, "EMIS Partner API  \u2014  Fully Integrated")

    # ────────────────────────────────────────────
    # SECTION 1 - BLUE: Case Study
    # ────────────────────────────────────────────
    sec1_top = top_bar_bottom
    sec1_bottom = H / 2 - 20
    c.setFillColor(BLUE)
    c.rect(0, sec1_bottom, W, sec1_top - sec1_bottom, fill=1, stroke=0)

    y = sec1_top - 25
    c.setFillColor(HexColor('#ffffff80'))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN + 8, y, "CASE STUDY")

    y -= 28
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 12)
    c.drawCentredString(W / 2, y, "Real-world impact across 40+ practices nationally")

    # Big stat
    y -= 58
    c.setFont("Helvetica-Bold", 72)
    c.drawCentredString(W / 2, y, "43%")

    y -= 24
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(W / 2, y, "reduction in receptionist call handling time")

    y -= 18
    c.setFont("Helvetica", 11)
    c.drawCentredString(W / 2, y, "Barnstaple to Newcastle \u2014 from Leeds practices to 40+ nationally")

    # 3 stat boxes
    y -= 35
    box_w = (CW - 40) / 3
    box_h = 60
    stats = [
        ("\u00a34.7M", "NHS savings", "in 12 months"),
        ("285/wk", "GP appointments", "freed up"),
        ("\u00a3300K", "Saved per practice", "per year"),
    ]
    for i, (stat, line1, line2) in enumerate(stats):
        bx = MARGIN + 8 + i * (box_w + 12)
        c.setFillColor(HexColor('#ffffff18'))
        c.roundRect(bx, y - box_h, box_w, box_h, 8, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 22)
        c.drawCentredString(bx + box_w / 2, y - 23, stat)
        c.setFont("Helvetica", 9.5)
        c.drawCentredString(bx + box_w / 2, y - 39, line1)
        if line2:
            c.drawCentredString(bx + box_w / 2, y - 51, line2)

    # ────────────────────────────────────────────
    # SECTION 2 - WHITE: Bullet Point Overview
    # ────────────────────────────────────────────
    sec2_top = sec1_bottom
    sec2_bottom = 80
    c.setFillColor(WHITE)
    c.rect(0, sec2_bottom, W, sec2_top - sec2_bottom, fill=1, stroke=0)

    y = sec2_top - 25
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN + 8, y, "OVERVIEW")

    y -= 28

    bullets = [
        ("AI-led patient triage",
         "Patients speak directly to the system which guides them through safe, clinician-designed navigation questions."),
        ("Reduce reception pressure",
         "Free staff from lengthy triage calls. 71 hours of GP time saved every week across practices."),
        ("Consistent, structured outcomes",
         "Every patient assessed using the same safe pathways, co-created with reception teams and aligned with NICE guidance."),
        ("Built for NHS primary care",
         "Designed around real GP workflows. Consultation pathways reviewed by GP clinical leads."),
        ("EMIS Partner API integration",
         "Seamless integration with clinical systems. Triage data uploaded directly into patient records."),
    ]

    for title, desc in bullets:
        draw_check_bullet(c, MARGIN + 16, y + 2, 7, dark_bg=False)

        c.setFillColor(BLACK)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(MARGIN + 30, y, title)

        y -= 15
        c.setFillColor(MID_GREY)
        c.setFont("Helvetica", 9.5)
        wrapped = wrap_text(desc, "Helvetica", 9.5, CW - 40)
        for line in wrapped:
            c.drawString(MARGIN + 30, y, line)
            y -= 12
        y -= 10

    # ────────────────────────────────────────────
    # BOTTOM BAR - Blue
    # ────────────────────────────────────────────
    c.setFillColor(BLUE)
    c.rect(0, 0, W, 80, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-BoldOblique", 13)
    c.drawCentredString(W / 2, 48, "Safer triage. Less pressure on your practice.")
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN, 18, "smartnavigation.co.uk")
    draw_fuller_forbes(c, W - 155, 13, dark_bg=True)

    c.save()
    print(f"Created: {filename}")


if __name__ == "__main__":
    outdir = "/home/user/bramley-tv"
    create_poster1(os.path.join(outdir, "smartnav-poster-pricing.pdf"))
    create_poster2(os.path.join(outdir, "smartnav-poster-case-study.pdf"))
    print("Done! Both posters generated.")
