#!/usr/bin/env python3
"""
Generate two SMART Navigation marketing posters as PDF.
4 sections: top bar (white), section 1 (blue), section 2 (white), bottom bar (blue).
Black/white text only. Straight lines.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
import os

BLUE = HexColor('#1159A2')
CARD_BLUE = HexColor('#0e4d8e')
LOGO_CIRCLE = HexColor('#2157A8')
WHITE = white
BLACK = black
CHARCOAL = HexColor('#333333')
MID_GREY = HexColor('#555555')
LIGHT_TEXT = HexColor('#d0ddef')
FF_NAVY = HexColor('#003B7C')
FF_DARK = HexColor('#0B2545')
FF_MID = HexColor('#1565A0')
FF_LIGHT = HexColor('#5CB8D6')

W, H = A4
MARGIN = 45
CW = W - 2 * MARGIN

# Logo files
LOGO_DIR = "/home/user/bramley-tv"
SMARTNAV_LOGO = os.path.join(LOGO_DIR, "smartnavigation.logo.png")
FF_LOGO = os.path.join(LOGO_DIR, "Forbes and Fuller Transparent 3.png")

if not os.path.exists(SMARTNAV_LOGO):
    SMARTNAV_LOGO = None
if not os.path.exists(FF_LOGO):
    FF_LOGO = None


def draw_smart_logo(c, cx, y, scale=1.0, dark_bg=False):
    """Draw SMART navigation logo using real image file."""
    if SMARTNAV_LOGO:
        img = ImageReader(SMARTNAV_LOGO)
        iw, ih = img.getSize()
        target_h = 50 * scale
        ratio = target_h / ih
        target_w = iw * ratio
        c.drawImage(SMARTNAV_LOGO, cx - target_w / 2, y - target_h / 2,
                     width=target_w, height=target_h, mask='auto',
                     preserveAspectRatio=True)
    else:
        # Accurate reproduction from reference image
        r = 34 * scale
        circle_col = LOGO_CIRCLE if not dark_bg else WHITE
        circle_text = WHITE if not dark_bg else LOGO_CIRCLE
        # "navigation" is dark charcoal/grey, not black
        label_col = CHARCOAL if not dark_bg else WHITE

        # Large blue circle - positioned so text overlaps slightly
        circle_cx = cx - 85 * scale
        c.setFillColor(circle_col)
        c.circle(circle_cx, y, r, fill=1, stroke=0)

        # "SMART" in white bold inside circle
        c.setFillColor(circle_text)
        c.setFont("Helvetica-Bold", 14.5 * scale)
        c.drawCentredString(circle_cx, y - 5 * scale, "SMART")

        # "navigation" in charcoal, regular weight, positioned next to circle
        c.setFillColor(label_col)
        c.setFont("Helvetica", 28 * scale)
        nav_x = circle_cx + r + 4 * scale
        c.drawString(nav_x, y - 10 * scale, "navigation")

        # TM superscript in black
        c.setFillColor(BLACK if not dark_bg else WHITE)
        c.setFont("Helvetica-Bold", 10 * scale)
        nav_w = pdfmetrics.stringWidth("navigation", "Helvetica", 28 * scale)
        c.drawString(nav_x + nav_w + 2, y + 8 * scale, "TM")


def draw_ff_swirl(c, cx, cy, size=12, dark_bg=False):
    """Draw a simplified swirl/knot icon for Fuller and Forbes."""
    # Three interlocking loops in light blue, mid blue, dark blue
    colors = [FF_LIGHT, FF_MID, FF_NAVY] if not dark_bg else [
        HexColor('#8ed4e8'), HexColor('#5ca8d0'), WHITE]
    c.saveState()
    import math
    for i, col in enumerate(colors):
        c.setStrokeColor(col)
        c.setLineWidth(2.5)
        c.setLineCap(1)
        # Draw overlapping arcs to suggest a knot
        angle = i * 120
        ox = cx + math.cos(math.radians(angle)) * size * 0.25
        oy = cy + math.sin(math.radians(angle)) * size * 0.25
        p = c.beginPath()
        # Simple ellipse arc
        for t in range(0, 360, 5):
            rad = math.radians(t + angle)
            px = ox + math.cos(rad) * size * 0.55
            py = oy + math.sin(rad) * size * 0.4
            if t == 0:
                p.moveTo(px, py)
            else:
                p.lineTo(px, py)
        p.close()
        c.setFillColor(col)
        c.setFillAlpha(0.35)
        c.drawPath(p, fill=1, stroke=1)
    c.setFillAlpha(1.0)
    c.restoreState()


def draw_ff_logo(c, cx, y, scale=1.0, dark_bg=False):
    """Draw Fuller and Forbes Healthcare Group logo using real image."""
    if FF_LOGO:
        img = ImageReader(FF_LOGO)
        iw, ih = img.getSize()
        target_h = 28 * scale
        ratio = target_h / ih
        target_w = iw * ratio
        c.drawImage(FF_LOGO, cx - target_w / 2, y - target_h / 2,
                     width=target_w, height=target_h, mask='auto',
                     preserveAspectRatio=True)
    else:
        # Swirl icon
        draw_ff_swirl(c, cx - 55, y, size=10, dark_bg=dark_bg)
        # Text in navy blue (or white on dark bg)
        col = FF_NAVY if not dark_bg else WHITE
        c.setFillColor(col)
        c.setFont("Helvetica", 8.5)
        c.drawString(cx - 40, y + 4, "Fuller and Forbes")
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(cx - 40, y - 7, "Healthcare Group")


def draw_check_bullet(c, x, y, dark_bg=False):
    size = 8
    if dark_bg:
        c.setFillColor(WHITE)
        chk = BLUE
    else:
        c.setFillColor(BLUE)
        chk = WHITE
    c.circle(x, y + 3, size, fill=1, stroke=0)
    c.setStrokeColor(chk)
    c.setLineWidth(1.8)
    c.line(x - 3.5, y + 2.5, x - 0.5, y - 0.5)
    c.line(x - 0.5, y - 0.5, x + 4, y + 5.5)


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

    # Layout: 4 bands
    top_bar_h = 100       # white - logo
    bottom_bar_h = 70     # blue - footer
    middle = H - top_bar_h - bottom_bar_h
    sec1_h = middle * 0.52  # blue - pricing
    sec2_h = middle * 0.48  # white - usage & AVT

    sec1_top = H - top_bar_h
    sec1_bottom = sec1_top - sec1_h
    sec2_top = sec1_bottom
    sec2_bottom = bottom_bar_h

    # ── TOP BAR (white) ──
    c.setFillColor(WHITE)
    c.rect(0, sec1_top, W, top_bar_h, fill=1, stroke=0)
    draw_smart_logo(c, W / 2 + 15, H - 50, scale=1.0)

    # ── SECTION 1 (blue) - Pricing ──
    c.setFillColor(BLUE)
    c.rect(0, sec1_bottom, W, sec1_h, fill=1, stroke=0)

    y = sec1_top - 28
    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN, y, "STAGE 1: PRICING")

    y -= 35
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(W / 2, y, "Simple, transparent pricing")
    y -= 22
    c.setFont("Helvetica", 13)
    c.drawCentredString(W / 2, y, "designed for NHS primary care")

    # Price box
    y -= 40
    box_h = 85
    c.setFillColor(CARD_BLUE)
    c.roundRect(MARGIN, y - box_h, CW, box_h, 10, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 44)
    c.drawString(MARGIN + 18, y - 45, "\u00a31,000")
    pw = pdfmetrics.stringWidth("\u00a31,000", "Helvetica-Bold", 44)
    c.setFont("Helvetica", 17)
    c.drawString(MARGIN + 26 + pw, y - 38, "for 12 months")

    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 10.5)
    c.drawString(MARGIN + 18, y - 64, "Per practice, all-inclusive. No hidden charges. No auto-renewals.")
    c.drawString(MARGIN + 18, y - 78, "Includes full onboarding, training & clinical support.")

    # Extra line
    y -= box_h + 22
    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 10.5)
    c.drawCentredString(W / 2, y, "From single-site surgeries to ICBs \u2014 one simple price for everyone.")

    # ── SECTION 2 (white) - Usage & AVT ──
    c.setFillColor(WHITE)
    c.rect(0, sec2_bottom, W, sec2_h, fill=1, stroke=0)

    y = sec2_top - 25
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN, y, "USAGE & ADOPTION")

    # Stats 2x2
    y -= 28
    box_w = (CW - 16) / 2
    box_h_stat = 58

    all_stats = [
        [("152,508", "Patients triaged (2024\u201325)"), ("40+", "Practices nationally")],
        [("\u00a34.7M", "NHS savings in 12 months"), ("71 hrs/wk", "GP time saved")],
    ]

    for row in all_stats:
        for col_i, (stat, label) in enumerate(row):
            bx = MARGIN + col_i * (box_w + 16)
            by = y - box_h_stat
            c.setFillColor(BLUE)
            c.roundRect(bx, by, box_w, box_h_stat, 8, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 24)
            c.drawCentredString(bx + box_w / 2, by + box_h_stat - 24, stat)
            c.setFont("Helvetica", 9.5)
            c.drawCentredString(bx + box_w / 2, by + 10, label)
        y -= box_h_stat + 8

    # AVT
    y -= 8
    c.setStrokeColor(HexColor('#c0ccd8'))
    c.setLineWidth(0.5)
    c.line(MARGIN, y + 4, W - MARGIN, y + 4)

    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN, y - 12, "Stage 2: Automated Voice Triage")

    y -= 30
    c.setFillColor(MID_GREY)
    c.setFont("Helvetica", 10.5)
    c.drawString(MARGIN, y, "AI-powered voice agent handles patient calls 24/7,")
    y -= 14
    c.drawString(MARGIN, y, "guiding them through clinician-designed triage pathways.")

    y -= 18
    avt_bullets = [
        "Handles overflow and out-of-hours calls automatically",
        "Same clinically-safe pathways used by receptionists",
        "Seamless handoff to human staff when needed",
    ]
    for bullet in avt_bullets:
        c.setFillColor(BLUE)
        c.setFont("Helvetica", 7)
        c.drawString(MARGIN + 4, y + 1.5, "\u25cf")
        c.setFillColor(BLACK)
        c.setFont("Helvetica", 10)
        c.drawString(MARGIN + 15, y, bullet)
        y -= 14

    # ── BOTTOM BAR (blue) ──
    c.setFillColor(BLUE)
    c.rect(0, 0, W, bottom_bar_h, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-BoldOblique", 12)
    c.drawCentredString(W / 2, 42, "Safer triage. Less pressure on your practice.")

    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 8)
    c.drawString(MARGIN, 15, "smartnavigation.co.uk")
    draw_ff_logo(c, W - 90, 20, dark_bg=True)

    c.save()
    print(f"Created: {filename}")


# ═══════════════════════════════════════════════════════════════════
# POSTER 2: Case Study & Overview
# ═══════════════════════════════════════════════════════════════════

def create_poster2(filename):
    c = canvas.Canvas(filename, pagesize=A4)
    c.setTitle("SMART Navigation - Case Study & Overview")

    # Layout: 4 bands
    top_bar_h = 120      # white - logo + EMIS badge
    bottom_bar_h = 70    # blue - footer
    middle = H - top_bar_h - bottom_bar_h
    sec1_h = middle * 0.50  # blue - case study
    sec2_h = middle * 0.50  # white - overview

    sec1_top = H - top_bar_h
    sec1_bottom = sec1_top - sec1_h
    sec2_top = sec1_bottom
    sec2_bottom = bottom_bar_h

    # ── TOP BAR (white) ──
    c.setFillColor(WHITE)
    c.rect(0, sec1_top, W, top_bar_h, fill=1, stroke=0)
    draw_smart_logo(c, W / 2 + 15, H - 42, scale=1.0)

    # EMIS badge
    badge_w = CW - 80
    badge_y = sec1_top + 12
    c.setFillColor(BLUE)
    c.roundRect((W - badge_w) / 2, badge_y, badge_w, 28, 6, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W / 2, badge_y + 9, "EMIS Partner API  \u2014  Fully Integrated")

    # ── SECTION 1 (blue) - Case Study ──
    c.setFillColor(BLUE)
    c.rect(0, sec1_bottom, W, sec1_h, fill=1, stroke=0)

    y = sec1_top - 25
    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN, y, "CASE STUDY")

    y -= 25
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 12)
    c.drawCentredString(W / 2, y, "Real-world impact across 40+ practices nationally")

    # Big stat
    y -= 58
    c.setFont("Helvetica-Bold", 76)
    c.drawCentredString(W / 2, y, "43%")

    y -= 24
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(W / 2, y, "reduction in receptionist call handling time")

    y -= 18
    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 10.5)
    c.drawCentredString(W / 2, y, "Barnstaple to Newcastle \u2014 from Leeds practices to 40+ nationally")

    # 3 stat boxes
    y -= 32
    box_w = (CW - 32) / 3
    box_h_stat = 58
    stats = [
        ("\u00a34.7M", "NHS savings", "in 12 months"),
        ("285/wk", "GP appointments", "freed up"),
        ("\u00a3300K", "Saved per practice", "per year"),
    ]
    for i, (stat, l1, l2) in enumerate(stats):
        bx = MARGIN + i * (box_w + 16)
        c.setFillColor(CARD_BLUE)
        c.roundRect(bx, y - box_h_stat, box_w, box_h_stat, 8, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 21)
        c.drawCentredString(bx + box_w / 2, y - 22, stat)
        c.setFillColor(LIGHT_TEXT)
        c.setFont("Helvetica", 9)
        c.drawCentredString(bx + box_w / 2, y - 38, l1)
        if l2:
            c.drawCentredString(bx + box_w / 2, y - 49, l2)

    # ── SECTION 2 (white) - Overview ──
    c.setFillColor(WHITE)
    c.rect(0, sec2_bottom, W, sec2_h, fill=1, stroke=0)

    y = sec2_top - 25
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN, y, "OVERVIEW")

    y -= 24
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
        c.setFont("Helvetica-Bold", 11)
        c.drawString(MARGIN + 24, y, title)

        y -= 14
        c.setFillColor(MID_GREY)
        c.setFont("Helvetica", 9)
        wrapped = wrap_text(desc, "Helvetica", 9, CW - 28)
        for line in wrapped:
            c.drawString(MARGIN + 24, y, line)
            y -= 11
        y -= 9

    # ── BOTTOM BAR (blue) ──
    c.setFillColor(BLUE)
    c.rect(0, 0, W, bottom_bar_h, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-BoldOblique", 12)
    c.drawCentredString(W / 2, 42, "Safer triage. Less pressure on your practice.")

    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 8)
    c.drawString(MARGIN, 15, "smartnavigation.co.uk")
    draw_ff_logo(c, W - 90, 20, dark_bg=True)

    c.save()
    print(f"Created: {filename}")


if __name__ == "__main__":
    outdir = "/home/user/bramley-tv"
    create_poster1(os.path.join(outdir, "smartnav-poster-pricing.pdf"))
    create_poster2(os.path.join(outdir, "smartnav-poster-case-study.pdf"))
    print("Done! Both posters generated.")
