#!/usr/bin/env python3
"""
Generate two SMART Navigation marketing posters as PDF.
Style reference: Canva poster with large centred logo, clean sections,
alternating white/#1159A2, generous spacing. Black/white text only.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
import os

BLUE = HexColor('#1159A2')
WHITE = white
BLACK = black
MID_GREY = HexColor('#555555')
LIGHT_TEXT = HexColor('#d0ddef')  # light text on blue bg

W, H = A4
MARGIN = 45
CW = W - 2 * MARGIN


def draw_smart_logo_large(c, cx, y, dark_bg=False):
    """Draw large centred logo like the Canva version."""
    r = 42
    circle_col = BLUE if not dark_bg else WHITE
    circle_text = WHITE if not dark_bg else BLUE
    label_col = BLACK if not dark_bg else WHITE

    # Circle
    c.setFillColor(circle_col)
    c.circle(cx - 90, y, r, fill=1, stroke=0)
    # SMART in circle
    c.setFillColor(circle_text)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(cx - 90, y - 5, "SMART")
    # 'navigation' text
    c.setFillColor(label_col)
    c.setFont("Helvetica", 32)
    c.drawString(cx - 42, y - 11, "navigation")
    # TM
    c.setFont("Helvetica", 9)
    nav_w = pdfmetrics.stringWidth("navigation", "Helvetica", 32)
    c.drawString(cx - 42 + nav_w + 3, y + 8, "\u2122")


def draw_check_bullet(c, x, y, dark_bg=False):
    """Draw a check circle bullet."""
    size = 9
    if dark_bg:
        c.setFillColor(WHITE)
        chk = BLUE
    else:
        c.setFillColor(BLUE)
        chk = WHITE
    c.circle(x, y + 3, size, fill=1, stroke=0)
    c.setStrokeColor(chk)
    c.setLineWidth(2)
    c.line(x - 4, y + 2.5, x - 1, y - 0.5)
    c.line(x - 1, y - 0.5, x + 4.5, y + 6)


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
    # TOP SECTION - White: Logo + Pricing
    # ────────────────────────────────────────────
    white_bottom = H * 0.52
    c.setFillColor(WHITE)
    c.rect(0, white_bottom, W, H - white_bottom, fill=1, stroke=0)

    # Large centred logo
    draw_smart_logo_large(c, W / 2 + 20, H - 65)

    # Headline
    y = H - 130
    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 28)
    lines = wrap_text("Simple, transparent pricing", "Helvetica-Bold", 28, CW)
    for line in lines:
        c.drawCentredString(W / 2, y, line)
        y -= 34
    c.setFillColor(MID_GREY)
    c.setFont("Helvetica", 14)
    c.drawCentredString(W / 2, y, "designed for NHS primary care")

    # Price box
    y -= 45
    box_h = 90
    c.setFillColor(BLUE)
    c.roundRect(MARGIN, y - box_h, CW, box_h, 10, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 48)
    c.drawString(MARGIN + 20, y - 50, "\u00a31,000")
    pw = pdfmetrics.stringWidth("\u00a31,000", "Helvetica-Bold", 48)
    c.setFont("Helvetica", 18)
    c.drawString(MARGIN + 30 + pw, y - 42, "for 12 months")

    c.setFont("Helvetica", 11)
    c.drawString(MARGIN + 20, y - 70, "Per practice, all-inclusive. No hidden charges. No auto-renewals.")
    c.drawString(MARGIN + 20, y - 84, "Includes full onboarding, training & clinical support.")

    # Extra details below price box
    y -= box_h + 30
    c.setFillColor(MID_GREY)
    c.setFont("Helvetica", 11)
    c.drawCentredString(W / 2, y, "From single-site surgeries to ICBs \u2014 one simple price for everyone.")

    # ────────────────────────────────────────────
    # BOTTOM SECTION - Blue: Usage & AVT
    # ────────────────────────────────────────────
    c.setFillColor(BLUE)
    c.rect(0, 0, W, white_bottom, fill=1, stroke=0)

    y = white_bottom - 30
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(W / 2, y, "Usage & Adoption")

    # Stats - 2x2
    y -= 35
    box_w = (CW - 16) / 2
    box_h = 62

    all_stats = [
        [("152,508", "Patients triaged (2024\u201325)"), ("40+", "Practices nationally")],
        [("\u00a34.7M", "NHS savings in 12 months"), ("71 hrs/wk", "GP time saved")],
    ]

    for row in all_stats:
        for col_i, (stat, label) in enumerate(row):
            bx = MARGIN + col_i * (box_w + 16)
            by = y - box_h
            # Subtle lighter box
            c.setFillColor(HexColor('#0e4d8e'))
            c.roundRect(bx, by, box_w, box_h, 8, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 26)
            c.drawCentredString(bx + box_w / 2, by + box_h - 26, stat)
            c.setFillColor(LIGHT_TEXT)
            c.setFont("Helvetica", 10)
            c.drawCentredString(bx + box_w / 2, by + 10, label)
        y -= box_h + 10

    # AVT Section
    y -= 12
    c.setStrokeColor(HexColor('#2070b8'))
    c.setLineWidth(0.5)
    c.line(MARGIN, y + 6, W - MARGIN, y + 6)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(MARGIN, y - 12, "Stage 2: Automated Voice Triage")

    y -= 32
    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 11)
    c.drawString(MARGIN, y, "AI-powered voice agent handles patient calls 24/7,")
    y -= 15
    c.drawString(MARGIN, y, "guiding them through clinician-designed triage pathways.")

    y -= 22
    avt_bullets = [
        "Handles overflow and out-of-hours calls automatically",
        "Same clinically-safe pathways used by receptionists",
        "Seamless handoff to human staff when needed",
    ]
    for bullet in avt_bullets:
        c.setFillColor(WHITE)
        c.setFont("Helvetica", 7)
        c.drawString(MARGIN + 4, y + 2, "\u25cf")
        c.setFillColor(LIGHT_TEXT)
        c.setFont("Helvetica", 10.5)
        c.drawString(MARGIN + 16, y, bullet)
        y -= 15

    # Footer
    y = 18
    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN, y, "smartnavigation.co.uk")
    c.setFont("Helvetica", 8)
    c.drawRightString(W - MARGIN, y + 5, "Fuller and Forbes")
    c.setFont("Helvetica-Bold", 8)
    c.drawRightString(W - MARGIN, y - 6, "Healthcare Group")

    c.save()
    print(f"Created: {filename}")


# ═══════════════════════════════════════════════════════════════════
# POSTER 2: Case Study & Overview
# ═══════════════════════════════════════════════════════════════════

def create_poster2(filename):
    c = canvas.Canvas(filename, pagesize=A4)
    c.setTitle("SMART Navigation - Case Study & Overview")

    # ────────────────────────────────────────────
    # TOP SECTION - White: Logo + EMIS badge
    # ────────────────────────────────────────────
    white_top_bottom = H - 130
    c.setFillColor(WHITE)
    c.rect(0, white_top_bottom, W, H - white_top_bottom, fill=1, stroke=0)

    # Large centred logo
    draw_smart_logo_large(c, W / 2 + 20, H - 55)

    # EMIS badge
    badge_w = CW - 60
    c.setFillColor(BLUE)
    c.roundRect((W - badge_w) / 2, white_top_bottom + 10, badge_w, 30, 6, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(W / 2, white_top_bottom + 20, "EMIS Partner API  \u2014  Fully Integrated")

    # ────────────────────────────────────────────
    # MIDDLE SECTION - Blue: Case Study
    # ────────────────────────────────────────────
    blue_bottom = H * 0.38
    c.setFillColor(BLUE)
    c.rect(0, blue_bottom, W, white_top_bottom - blue_bottom, fill=1, stroke=0)

    y = white_top_bottom - 30
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(W / 2, y, "Case Study")

    y -= 22
    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 12)
    c.drawCentredString(W / 2, y, "Real-world impact across 40+ practices nationally")

    # Big stat
    y -= 62
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 80)
    c.drawCentredString(W / 2, y, "43%")

    y -= 26
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(W / 2, y, "reduction in receptionist call handling time")

    y -= 20
    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 11)
    c.drawCentredString(W / 2, y, "Barnstaple to Newcastle \u2014 from Leeds practices to 40+ nationally")

    # 3 stat boxes
    y -= 35
    box_w = (CW - 32) / 3
    box_h = 62
    stats = [
        ("\u00a34.7M", "NHS savings", "in 12 months"),
        ("285/wk", "GP appointments", "freed up"),
        ("\u00a3300K", "Saved per practice", "per year"),
    ]
    for i, (stat, l1, l2) in enumerate(stats):
        bx = MARGIN + i * (box_w + 16)
        c.setFillColor(HexColor('#0e4d8e'))
        c.roundRect(bx, y - box_h, box_w, box_h, 8, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 22)
        c.drawCentredString(bx + box_w / 2, y - 24, stat)
        c.setFillColor(LIGHT_TEXT)
        c.setFont("Helvetica", 9.5)
        c.drawCentredString(bx + box_w / 2, y - 40, l1)
        if l2:
            c.drawCentredString(bx + box_w / 2, y - 52, l2)

    # ────────────────────────────────────────────
    # BOTTOM SECTION - White: Bullet Overview
    # ────────────────────────────────────────────
    c.setFillColor(WHITE)
    c.rect(0, 60, W, blue_bottom - 60, fill=1, stroke=0)

    y = blue_bottom - 28
    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(MARGIN, y, "Overview")

    y -= 28
    bullets = [
        ("AI-led patient triage",
         "Patients speak directly to the system which guides them through safe, clinician-designed navigation questions."),
        ("Reduce reception pressure",
         "Free staff from lengthy triage calls. 71 hours of GP time saved every week across practices."),
        ("Consistent, structured outcomes",
         "Every patient assessed using the same safe pathways, aligned with NICE guidance."),
        ("Built for NHS primary care",
         "Designed around real GP workflows. Pathways reviewed by GP clinical leads."),
        ("EMIS Partner API integration",
         "Seamless integration with clinical systems. Triage data uploaded into patient records."),
    ]

    for title, desc in bullets:
        draw_check_bullet(c, MARGIN + 10, y, dark_bg=False)

        c.setFillColor(BLACK)
        c.setFont("Helvetica-Bold", 11.5)
        c.drawString(MARGIN + 26, y, title)

        y -= 15
        c.setFillColor(MID_GREY)
        c.setFont("Helvetica", 9)
        wrapped = wrap_text(desc, "Helvetica", 9, CW - 30)
        for line in wrapped:
            c.drawString(MARGIN + 26, y, line)
            y -= 12
        y -= 8

    # ────────────────────────────────────────────
    # FOOTER BAR - Blue
    # ────────────────────────────────────────────
    c.setFillColor(BLUE)
    c.rect(0, 0, W, 60, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-BoldOblique", 12)
    c.drawCentredString(W / 2, 32, "Safer triage. Less pressure on your practice.")

    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 8)
    c.drawString(MARGIN, 12, "smartnavigation.co.uk")
    c.setFont("Helvetica", 7.5)
    c.drawRightString(W - MARGIN, 16, "Fuller and Forbes")
    c.setFont("Helvetica-Bold", 7.5)
    c.drawRightString(W - MARGIN, 7, "Healthcare Group")

    c.save()
    print(f"Created: {filename}")


if __name__ == "__main__":
    outdir = "/home/user/bramley-tv"
    create_poster1(os.path.join(outdir, "smartnav-poster-pricing.pdf"))
    create_poster2(os.path.join(outdir, "smartnav-poster-case-study.pdf"))
    print("Done! Both posters generated.")
