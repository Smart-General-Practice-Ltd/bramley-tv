#!/usr/bin/env python3
"""
Generate two SMART Navigation marketing posters as PDF.
4 sections: white top / blue / white / blue bottom.
Black/white text only. Straight lines. Real logos.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
import os

BLUE = HexColor('#1159A2')
CARD_BLUE = HexColor('#0e4d8e')
WHITE = white
BLACK = black
CHARCOAL = HexColor('#333333')
MID_GREY = HexColor('#555555')
LIGHT_TEXT = HexColor('#d0ddef')

W, H = A4
M = 42  # margin
CW = W - 2 * M

# Logo files
LOGO_DIR = "/home/user/bramley-tv"
SMARTNAV_LOGO = os.path.join(LOGO_DIR, "smartnavigation.logo.png")
FF_LOGO = os.path.join(LOGO_DIR, "Forbes and Fuller Transparent 3.png")
if not os.path.exists(SMARTNAV_LOGO):
    SMARTNAV_LOGO = None
if not os.path.exists(FF_LOGO):
    FF_LOGO = None


def draw_smart_logo(c, cx, y, h=50):
    """Draw SMART navigation logo centred at cx, with given height."""
    if SMARTNAV_LOGO:
        img = ImageReader(SMARTNAV_LOGO)
        iw, ih = img.getSize()
        ratio = h / ih
        tw = iw * ratio
        c.drawImage(SMARTNAV_LOGO, cx - tw / 2, y - h / 2,
                     width=tw, height=h, mask='auto', preserveAspectRatio=True)
    else:
        # Fallback drawn version
        r = h * 0.45
        c.setFillColor(BLUE)
        c.circle(cx - h * 1.1, y, r, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", h * 0.28)
        c.drawCentredString(cx - h * 1.1, y - h * 0.08, "SMART")
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica", h * 0.48)
        c.drawString(cx - h * 1.1 + r + h * 0.08, y - h * 0.16, "navigation")
        c.setFillColor(BLACK)
        c.setFont("Helvetica-Bold", h * 0.18)
        nw = pdfmetrics.stringWidth("navigation", "Helvetica", h * 0.48)
        c.drawString(cx - h * 1.1 + r + h * 0.08 + nw + 2, y + h * 0.12, "TM")


def draw_ff_logo(c, x, y, h=30):
    """Draw Fuller and Forbes logo, left-aligned at x."""
    if FF_LOGO:
        img = ImageReader(FF_LOGO)
        iw, ih = img.getSize()
        ratio = h / ih
        tw = iw * ratio
        c.drawImage(FF_LOGO, x, y - h / 2, width=tw, height=h,
                     mask='auto', preserveAspectRatio=True)
    else:
        c.setFillColor(WHITE)
        c.setFont("Helvetica", 9)
        c.drawString(x, y + 4, "Fuller and Forbes")
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x, y - 7, "Healthcare Group")


def draw_check(c, x, y, on_blue=False):
    """Check bullet."""
    s = 8
    c.setFillColor(WHITE if on_blue else BLUE)
    c.circle(x, y + 3, s, fill=1, stroke=0)
    c.setStrokeColor(BLUE if on_blue else WHITE)
    c.setLineWidth(1.8)
    c.line(x - 3.5, y + 2.5, x - 0.5, y - 0.5)
    c.line(x - 0.5, y - 0.5, x + 4, y + 5.5)


def wrap_text(text, font, size, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = cur + (" " if cur else "") + w
        if pdfmetrics.stringWidth(test, font, size) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def stat_box(c, x, y, w, h, number, label):
    """Draw a stat box on blue background."""
    c.setFillColor(CARD_BLUE)
    c.roundRect(x, y, w, h, 8, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(x + w / 2, y + h - 30, number)
    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 10)
    c.drawCentredString(x + w / 2, y + 10, label)


# ═══════════════════════════════════════════════════════════════
# POSTER 1: Pricing & Usage
# ═══════════════════════════════════════════════════════════════

def create_poster1(filename):
    c = canvas.Canvas(filename, pagesize=A4)
    c.setTitle("SMART Navigation - Pricing & Usage")

    # Section heights
    top_h = 90
    bot_h = 75
    mid = H - top_h - bot_h
    blue1_h = mid * 0.48
    white1_h = mid * 0.52

    top_y = H - top_h
    blue1_y = top_y - blue1_h
    white1_y = bot_h

    # ── TOP BAR (white) ──
    c.setFillColor(WHITE)
    c.rect(0, top_y, W, top_h, fill=1, stroke=0)
    draw_smart_logo(c, W / 2 + 10, H - 45, h=48)

    # ── SECTION 1: Blue - Pricing ──
    c.setFillColor(BLUE)
    c.rect(0, blue1_y, W, blue1_h, fill=1, stroke=0)

    y = top_y - 26
    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(M, y, "STAGE 1: PRICING")

    y -= 32
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(W / 2, y, "Simple, transparent pricing")
    y -= 20
    c.setFont("Helvetica", 13)
    c.drawCentredString(W / 2, y, "designed for NHS primary care")

    # Price card
    y -= 35
    card_h = 80
    c.setFillColor(CARD_BLUE)
    c.roundRect(M, y - card_h, CW, card_h, 10, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 44)
    c.drawString(M + 18, y - 42, "\u00a31,000")
    pw = pdfmetrics.stringWidth("\u00a31,000", "Helvetica-Bold", 44)
    c.setFont("Helvetica", 16)
    c.drawString(M + 26 + pw, y - 34, "for 12 months")

    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 10)
    c.drawString(M + 18, y - 58, "Per practice, all-inclusive. No hidden charges. No auto-renewals.")
    c.drawString(M + 18, y - 72, "Includes full onboarding, training & clinical support.")

    y -= card_h + 18
    c.setFont("Helvetica", 10)
    c.setFillColor(LIGHT_TEXT)
    c.drawCentredString(W / 2, y, "From single-site surgeries to ICBs \u2014 one simple price for everyone.")

    # ── SECTION 2: White - Usage & AVT ──
    c.setFillColor(WHITE)
    c.rect(0, white1_y, W, white1_h, fill=1, stroke=0)

    y = blue1_y - 22
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(M, y, "Usage & Adoption")

    # Stats 2x2
    y -= 30
    bw = (CW - 14) / 2
    bh = 62

    for row in [
        [("152,508", "Patients triaged (2024\u201325)"), ("40+", "Practices nationally")],
        [("\u00a34.7M", "NHS savings in 12 months"), ("71 hrs/wk", "GP time saved")],
    ]:
        for i, (num, lbl) in enumerate(row):
            bx = M + i * (bw + 14)
            stat_box(c, bx, y - bh, bw, bh, num, lbl)
        y -= bh + 8

    # AVT
    y -= 12
    c.setStrokeColor(HexColor('#c8d4e0'))
    c.setLineWidth(0.5)
    c.line(M, y + 6, W - M, y + 6)

    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(M, y - 10, "Stage 2: Automated Voice Triage")

    y -= 28
    c.setFillColor(MID_GREY)
    c.setFont("Helvetica", 10.5)
    c.drawString(M, y, "AI-powered voice agent handles patient calls 24/7,")
    y -= 14
    c.drawString(M, y, "guiding them through clinician-designed triage pathways.")

    y -= 20
    for bullet in [
        "Handles overflow and out-of-hours calls automatically",
        "Same clinically-safe pathways used by receptionists",
        "Seamless handoff to human staff when needed",
    ]:
        c.setFillColor(BLUE)
        c.setFont("Helvetica", 7)
        c.drawString(M + 4, y + 1.5, "\u25cf")
        c.setFillColor(BLACK)
        c.setFont("Helvetica", 10.5)
        c.drawString(M + 16, y, bullet)
        y -= 15

    # ── BOTTOM BAR (blue) ──
    c.setFillColor(BLUE)
    c.rect(0, 0, W, bot_h, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-BoldOblique", 13)
    c.drawCentredString(W / 2, 44, "Safer triage. Less pressure on your practice.")

    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 8.5)
    c.drawString(M, 16, "smartnavigation.co.uk")

    draw_ff_logo(c, W - 180, 18, h=32)

    c.save()
    print(f"Created: {filename}")


# ═══════════════════════════════════════════════════════════════
# POSTER 2: Case Study & Overview
# ═══════════════════════════════════════════════════════════════

def create_poster2(filename):
    c = canvas.Canvas(filename, pagesize=A4)
    c.setTitle("SMART Navigation - Case Study & Overview")

    # Section heights
    top_h = 115
    bot_h = 75
    mid = H - top_h - bot_h
    blue1_h = mid * 0.50
    white1_h = mid * 0.50

    top_y = H - top_h
    blue1_y = top_y - blue1_h
    white1_y = bot_h

    # ── TOP BAR (white) ──
    c.setFillColor(WHITE)
    c.rect(0, top_y, W, top_h, fill=1, stroke=0)
    draw_smart_logo(c, W / 2 + 10, H - 38, h=44)

    # EMIS badge
    badge_w = CW - 60
    badge_y = top_y + 10
    c.setFillColor(BLUE)
    c.roundRect((W - badge_w) / 2, badge_y, badge_w, 30, 6, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(W / 2, badge_y + 10, "EMIS Partner API  \u2014  Fully Integrated")

    # ── SECTION 1: Blue - Case Study ──
    c.setFillColor(BLUE)
    c.rect(0, blue1_y, W, blue1_h, fill=1, stroke=0)

    y = top_y - 22
    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(M, y, "CASE STUDY")

    y -= 22
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 12)
    c.drawCentredString(W / 2, y, "Real-world impact across 40+ practices nationally")

    # Big stat
    y -= 58
    c.setFont("Helvetica-Bold", 80)
    c.drawCentredString(W / 2, y, "43%")

    y -= 22
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(W / 2, y, "reduction in receptionist call handling time")

    y -= 18
    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 11)
    c.drawCentredString(W / 2, y, "Barnstaple to Newcastle \u2014 from Leeds to 40+ nationally")

    # 3 stat boxes
    y -= 30
    bw = (CW - 28) / 3
    bh = 58
    for i, (num, l1, l2) in enumerate([
        ("\u00a34.7M", "NHS savings", "in 12 months"),
        ("285/wk", "GP appointments", "freed up"),
        ("\u00a3300K", "Saved per practice", "per year"),
    ]):
        bx = M + i * (bw + 14)
        c.setFillColor(CARD_BLUE)
        c.roundRect(bx, y - bh, bw, bh, 8, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 22)
        c.drawCentredString(bx + bw / 2, y - 22, num)
        c.setFillColor(LIGHT_TEXT)
        c.setFont("Helvetica", 9)
        c.drawCentredString(bx + bw / 2, y - 38, l1)
        if l2:
            c.drawCentredString(bx + bw / 2, y - 49, l2)

    # ── SECTION 2: White - Overview ──
    c.setFillColor(WHITE)
    c.rect(0, white1_y, W, white1_h, fill=1, stroke=0)

    y = blue1_y - 22
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(M, y, "Overview")

    y -= 26
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
        draw_check(c, M + 10, y)
        c.setFillColor(BLACK)
        c.setFont("Helvetica-Bold", 11.5)
        c.drawString(M + 26, y, title)
        y -= 15
        c.setFillColor(MID_GREY)
        c.setFont("Helvetica", 9.5)
        for line in wrap_text(desc, "Helvetica", 9.5, CW - 30):
            c.drawString(M + 26, y, line)
            y -= 12
        y -= 8

    # ── BOTTOM BAR (blue) ──
    c.setFillColor(BLUE)
    c.rect(0, 0, W, bot_h, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-BoldOblique", 13)
    c.drawCentredString(W / 2, 44, "Safer triage. Less pressure on your practice.")

    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 8.5)
    c.drawString(M, 16, "smartnavigation.co.uk")

    draw_ff_logo(c, W - 180, 18, h=32)

    c.save()
    print(f"Created: {filename}")


if __name__ == "__main__":
    d = "/home/user/bramley-tv"
    create_poster1(os.path.join(d, "smartnav-poster-pricing.pdf"))
    create_poster2(os.path.join(d, "smartnav-poster-case-study.pdf"))
    print("Done!")
