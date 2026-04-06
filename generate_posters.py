#!/usr/bin/env python3
"""
Generate two SMART Navigation marketing posters as PDF.
Clean straight-line sections, no diagonals. Real verified data.
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

W, H = A4
MARGIN = 40
CW = W - 2 * MARGIN


def draw_smart_logo(c, x, y, scale=1.0):
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
    c.setFillColor(TEXT_GREY)
    c.setFont("Helvetica", 9 * scale)
    c.drawString(x, y + 5, "Fuller and Forbes")
    c.setFont("Helvetica-Bold", 9 * scale)
    c.drawString(x, y - 7, "Healthcare Group")


def draw_check_bullet(c, x, y, size=8):
    c.setFillColor(CHECK_BLUE)
    c.circle(x, y + 2, size, fill=1, stroke=0)
    c.setStrokeColor(WHITE)
    c.setLineWidth(1.5)
    c.line(x - 3.5, y + 1.5, x - 1, y - 1)
    c.line(x - 1, y - 1, x + 4, y + 5)


def draw_footer(c):
    c.setFillColor(FOOTER_BG)
    c.rect(0, 35, W, 50, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-BoldOblique", 13)
    c.drawCentredString(W / 2, 55, "Safer triage. Less pressure on your practice.")

    c.setFillColor(WHITE)
    c.rect(0, 0, W, 35, fill=1, stroke=0)
    c.setFillColor(TEXT_GREY)
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN, 13, "smartnavigation.co.uk")
    draw_fuller_forbes(c, W - 155, 8, scale=0.9)


def draw_section_line(c, y):
    c.setStrokeColor(HexColor('#1a3a6a'))
    c.setLineWidth(0.5)
    c.line(MARGIN, y, W - MARGIN, y)


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

    # ── WHITE HEADER ──
    header_bottom = H - 165
    c.setFillColor(WHITE)
    c.rect(0, header_bottom, W, H - header_bottom, fill=1, stroke=0)

    draw_smart_logo(c, MARGIN + 5, H - 50, scale=1.15)

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN + 5, H - 82, "Voice")
    c.setFillColor(TEXT_GREY)
    c.setFont("Helvetica", 10.5)
    c.drawString(MARGIN + 47, H - 82, "AI-led telephone triage for primary care")

    # Stage 1 label
    c.setFillColor(LIGHT_GREY)
    c.roundRect(MARGIN, header_bottom + 10, CW, 38, 6, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(MARGIN + 14, header_bottom + 23, "Stage 1: Pricing")

    # ── NAVY MAIN SECTION ──
    c.setFillColor(NAVY)
    c.rect(0, 85, W, header_bottom - 85, fill=1, stroke=0)

    # Headline
    y = header_bottom - 30
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(W / 2, y, "Simple, transparent pricing")
    y -= 22
    c.setFillColor(TEAL)
    c.setFont("Helvetica", 15)
    c.drawCentredString(W / 2, y, "designed for NHS primary care")

    # Pricing card
    y -= 38
    card_h = 130
    c.setFillColor(CARD_BG)
    c.roundRect(MARGIN + 8, y - card_h, CW - 16, card_h, 10, fill=1, stroke=0)

    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 36)
    c.drawString(MARGIN + 26, y - 38, "\u00a31,000")
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN + 175, y - 30, "for 12 months")

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 11.5)
    c.drawString(MARGIN + 26, y - 58, "Per practice, all-inclusive")

    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN + 26, y - 82, "No hidden charges  |  No auto-renewals")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(MARGIN + 26, y - 100, "Includes full onboarding, training & clinical support")
    c.drawString(MARGIN + 26, y - 116, "From single-site surgeries to ICBs")

    # Usage & Adoption
    y -= card_h + 28
    draw_section_line(c, y + 10)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(MARGIN + 8, y - 8, "Usage & Adoption")

    y -= 32
    box_w = (CW - 30) / 2
    box_h = 68

    stats_row1 = [("152,508", "Patients triaged (2024-25)"), ("40+", "Practices nationally")]
    stats_row2 = [("\u00a34.7M", "NHS savings in 12 months"), ("71 hrs/wk", "GP time saved")]

    for stats in [stats_row1, stats_row2]:
        for col_i, (stat, label) in enumerate(stats):
            bx = MARGIN + 8 + col_i * (box_w + 14)
            by = y - box_h
            c.setFillColor(CARD_BG)
            c.roundRect(bx, by, box_w, box_h, 10, fill=1, stroke=0)
            c.setFillColor(TEAL)
            c.setFont("Helvetica-Bold", 26)
            c.drawCentredString(bx + box_w / 2, by + box_h - 26, stat)
            c.setFillColor(MUTED)
            c.setFont("Helvetica", 10.5)
            c.drawCentredString(bx + box_w / 2, by + 12, label)
        y -= box_h + 12

    # Stage 2: AVT
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
        c.drawString(MARGIN + 12, y + 1, "\u25cf")
        c.setFillColor(HexColor('#c0d0e0'))
        c.setFont("Helvetica", 10.5)
        c.drawString(MARGIN + 24, y, bullet)
        y -= 15

    draw_footer(c)
    c.save()
    print(f"Created: {filename}")


# ═══════════════════════════════════════════════════════════════════
# POSTER 2: Case Study & Overview
# ═══════════════════════════════════════════════════════════════════

def create_poster2(filename):
    c = canvas.Canvas(filename, pagesize=A4)
    c.setTitle("SMART Navigation - Case Study & Overview")

    # ── WHITE HEADER ──
    header_bottom = H - 190
    c.setFillColor(WHITE)
    c.rect(0, header_bottom, W, H - header_bottom, fill=1, stroke=0)

    draw_smart_logo(c, MARGIN + 5, H - 50, scale=1.15)

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN + 5, H - 82, "Voice")
    c.setFillColor(TEXT_GREY)
    c.setFont("Helvetica", 10.5)
    c.drawString(MARGIN + 47, H - 82, "Clinician-designed AI telephone triage")

    # EMIS / Integration badge
    badge_y = H - 120
    c.setFillColor(BRAND_BLUE)
    c.roundRect(MARGIN + 30, badge_y - 48, CW - 60, 42, 8, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(W / 2, badge_y - 32, "EMIS Partner API  \u2014  Fully Integrated")

    # ── NAVY MAIN SECTION ──
    c.setFillColor(NAVY)
    c.rect(0, 85, W, header_bottom - 85, fill=1, stroke=0)

    # Case Study headline
    y = header_bottom - 28
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(W / 2, y, "Case Study")

    y -= 22
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 12)
    c.drawCentredString(W / 2, y, "Real-world impact across 40+ practices nationally")

    # Big stat: 43%
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
    c.drawCentredString(W / 2, y, "Barnstaple to Newcastle \u2014 from a handful of Leeds practices to 40+ nationally")

    # 3 stat boxes
    y -= 38
    box_w = (CW - 40) / 3
    box_h = 65
    stats = [
        ("\u00a34.7M", "NHS savings", "in 12 months"),
        ("285/wk", "GP appointments", "freed up"),
        ("\u00a3300K", "Saved per practice", "per year"),
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

    # Bullet Point Overview
    y -= box_h + 22
    draw_section_line(c, y + 8)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(MARGIN + 8, y - 8, "Bullet Point Overview")

    y -= 32
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

    draw_footer(c)
    c.save()
    print(f"Created: {filename}")


if __name__ == "__main__":
    outdir = "/home/user/bramley-tv"
    create_poster1(os.path.join(outdir, "smartnav-poster-pricing.pdf"))
    create_poster2(os.path.join(outdir, "smartnav-poster-case-study.pdf"))
    print("Done! Both posters generated.")
