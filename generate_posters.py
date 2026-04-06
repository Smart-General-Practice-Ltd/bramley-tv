#!/usr/bin/env python3
"""
SMART Navigation marketing posters.
Tall narrow format matching Canva (210mm x 495mm).
4 sections: white / blue / white / blue.
Everything large and readable.
"""

from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
import os

BLUE = HexColor('#1159A2')
CARD_BLUE = HexColor('#0e4d8e')
WHITE = white
BLACK = black
MID_GREY = HexColor('#555555')
LIGHT_TEXT = HexColor('#d0ddef')

# Page size matching Canva tall poster
PW = 210 * mm   # 595pt
PH = 495 * mm   # 1403pt
PAGE = (PW, PH)
M = 35           # margin
CW = PW - 2 * M

LOGO_DIR = "/home/user/bramley-tv"
SMARTNAV_LOGO = os.path.join(LOGO_DIR, "smartnavigation.logo.png")
FF_LOGO = os.path.join(LOGO_DIR, "Forbes and Fuller Transparent 3.png")
if not os.path.exists(SMARTNAV_LOGO):
    SMARTNAV_LOGO = None
if not os.path.exists(FF_LOGO):
    FF_LOGO = None


def draw_logo(c, cx, y, h=65):
    if SMARTNAV_LOGO:
        img = ImageReader(SMARTNAV_LOGO)
        iw, ih = img.getSize()
        tw = iw * (h / ih)
        c.drawImage(SMARTNAV_LOGO, cx - tw / 2, y - h / 2,
                     width=tw, height=h, mask='auto', preserveAspectRatio=True)
    else:
        r = h * 0.45
        ccx = cx - h * 1.1
        c.setFillColor(BLUE)
        c.circle(ccx, y, r, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", h * 0.28)
        c.drawCentredString(ccx, y - h * 0.08, "SMART")
        c.setFillColor(HexColor('#333'))
        c.setFont("Helvetica", h * 0.48)
        c.drawString(ccx + r + h * 0.08, y - h * 0.16, "navigation")


def draw_ff(c, cx, y, h=40):
    if FF_LOGO:
        img = ImageReader(FF_LOGO)
        iw, ih = img.getSize()
        tw = iw * (h / ih)
        c.drawImage(FF_LOGO, cx - tw / 2, y - h / 2,
                     width=tw, height=h, mask='auto', preserveAspectRatio=True)
    else:
        c.setFillColor(WHITE)
        c.setFont("Helvetica", 11)
        c.drawCentredString(cx, y + 5, "Fuller and Forbes")
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(cx, y - 8, "Healthcare Group")


def check_bullet(c, x, y, on_blue=False):
    s = 10
    c.setFillColor(WHITE if on_blue else BLUE)
    c.circle(x, y + 3, s, fill=1, stroke=0)
    c.setStrokeColor(BLUE if on_blue else WHITE)
    c.setLineWidth(2.2)
    c.line(x - 4, y + 2, x - 1, y - 1.5)
    c.line(x - 1, y - 1.5, x + 5, y + 6)


def wrap(text, font, size, max_w):
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


# ═══════════════════════════════════════════════════════════════
# POSTER 1: PRICING & USAGE
# ═══════════════════════════════════════════════════════════════

def create_poster1(filename):
    c = canvas.Canvas(filename, pagesize=PAGE)

    # Section boundaries (from top down)
    top_bar_bottom = PH - 130       # white logo bar
    blue1_bottom = PH * 0.52       # blue pricing section
    white1_bottom = 90              # white usage section
    # blue footer = 0 to white1_bottom

    # ── TOP BAR (white) - Logo ──
    c.setFillColor(WHITE)
    c.rect(0, top_bar_bottom, PW, PH - top_bar_bottom, fill=1, stroke=0)
    draw_logo(c, PW / 2 + 12, PH - 65, h=60)

    # ── SECTION 1 (blue) - Pricing ──
    c.setFillColor(BLUE)
    c.rect(0, blue1_bottom, PW, top_bar_bottom - blue1_bottom, fill=1, stroke=0)

    y = top_bar_bottom - 40
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(M, y, "STAGE 1: PRICING")

    # Big headline
    y -= 55
    c.setFont("Helvetica-Bold", 36)
    for line in wrap("Simple, transparent pricing", "Helvetica-Bold", 36, CW - 20):
        c.drawCentredString(PW / 2, y, line)
        y -= 42
    y += 18
    c.setFont("Helvetica", 16)
    c.drawCentredString(PW / 2, y, "designed for NHS primary care")

    # Price card - big and bold
    y -= 50
    card_h = 120
    c.setFillColor(CARD_BLUE)
    c.roundRect(M, y - card_h, CW, card_h, 12, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 60)
    c.drawString(M + 24, y - 55, "\u00a31,000")
    pw = pdfmetrics.stringWidth("\u00a31,000", "Helvetica-Bold", 60)
    c.setFont("Helvetica", 22)
    c.drawString(M + 34 + pw, y - 46, "for 12 months")

    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 13)
    c.drawString(M + 24, y - 78, "Per practice, all-inclusive. No hidden charges.")
    c.drawString(M + 24, y - 95, "No auto-renewals. Full onboarding & support included.")

    y -= card_h + 30
    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica-Oblique", 12)
    c.drawCentredString(PW / 2, y, "From single-site surgeries to ICBs \u2014 one simple price.")

    # ── SECTION 2 (white) - Usage & AVT ──
    c.setFillColor(WHITE)
    c.rect(0, white1_bottom, PW, blue1_bottom - white1_bottom, fill=1, stroke=0)

    y = blue1_bottom - 38
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(M, y, "Usage & Adoption")

    # 2x2 stat grid
    y -= 32
    bw = (CW - 16) / 2
    bh = 80

    for row in [
        [("152,508", "Patients triaged (2024\u201325)"), ("40+", "Practices nationally")],
        [("\u00a34.7M", "NHS savings in 12 months"), ("71 hrs/wk", "GP time saved")],
    ]:
        for i, (num, lbl) in enumerate(row):
            bx = M + i * (bw + 16)
            c.setFillColor(BLUE)
            c.roundRect(bx, y - bh, bw, bh, 10, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 32)
            c.drawCentredString(bx + bw / 2, y - 34, num)
            c.setFont("Helvetica", 12)
            c.drawCentredString(bx + bw / 2, y - bh + 16, lbl)
        y -= bh + 10

    # Stage 2: AVT
    y -= 10
    c.setStrokeColor(HexColor('#c8d4e0'))
    c.setLineWidth(0.5)
    c.line(M, y + 5, PW - M, y + 5)

    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(M, y - 16, "Stage 2: Automated Voice Triage")

    y -= 40
    c.setFillColor(MID_GREY)
    c.setFont("Helvetica", 13)
    for line in wrap(
        "AI-powered voice agent handles patient calls 24/7, guiding them through clinician-designed triage pathways.",
        "Helvetica", 13, CW
    ):
        c.drawString(M, y, line)
        y -= 17

    y -= 10
    for bullet in [
        "Handles overflow and out-of-hours calls automatically",
        "Same clinically-safe pathways used by receptionists",
        "Seamless handoff to human staff when needed",
    ]:
        c.setFillColor(BLUE)
        c.setFont("Helvetica", 9)
        c.drawString(M + 5, y + 2, "\u25cf")
        c.setFillColor(BLACK)
        c.setFont("Helvetica", 12.5)
        c.drawString(M + 18, y, bullet)
        y -= 18

    # ── BOTTOM BAR (blue) - Footer ──
    c.setFillColor(BLUE)
    c.rect(0, 0, PW, white1_bottom, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-BoldOblique", 14)
    c.drawCentredString(PW / 2, 52, "Safer triage. Less pressure on your practice.")

    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 10)
    c.drawString(M, 18, "smartnavigation.co.uk")
    draw_ff(c, PW - 95, 26, h=38)

    c.save()
    print(f"Created: {filename}")


# ═══════════════════════════════════════════════════════════════
# POSTER 2: CASE STUDY & OVERVIEW
# ═══════════════════════════════════════════════════════════════

def create_poster2(filename):
    c = canvas.Canvas(filename, pagesize=PAGE)

    # Section boundaries
    top_bar_bottom = PH - 150      # white logo + EMIS badge
    blue1_bottom = PH * 0.48      # blue case study
    white1_bottom = 90             # white overview
    # blue footer = 0 to white1_bottom

    # ── TOP BAR (white) - Logo + EMIS ──
    c.setFillColor(WHITE)
    c.rect(0, top_bar_bottom, PW, PH - top_bar_bottom, fill=1, stroke=0)
    draw_logo(c, PW / 2 + 12, PH - 52, h=55)

    # EMIS badge
    badge_w = CW - 40
    badge_y = top_bar_bottom + 18
    c.setFillColor(BLUE)
    c.roundRect((PW - badge_w) / 2, badge_y, badge_w, 38, 8, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(PW / 2, badge_y + 12, "EMIS Partner API  \u2014  Fully Integrated")

    # ── SECTION 1 (blue) - Case Study ──
    c.setFillColor(BLUE)
    c.rect(0, blue1_bottom, PW, top_bar_bottom - blue1_bottom, fill=1, stroke=0)

    y = top_bar_bottom - 35
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(M, y, "CASE STUDY")

    y -= 30
    c.setFont("Helvetica", 14)
    c.drawCentredString(PW / 2, y, "Real-world impact across 40+ practices nationally")

    # 43% - massive
    y -= 85
    c.setFont("Helvetica-Bold", 100)
    c.drawCentredString(PW / 2, y, "43%")

    y -= 30
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(PW / 2, y, "reduction in receptionist")
    y -= 22
    c.drawCentredString(PW / 2, y, "call handling time")

    y -= 24
    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 12)
    c.drawCentredString(PW / 2, y, "Barnstaple to Newcastle \u2014 from Leeds to 40+ nationally")

    # 3 stat boxes
    y -= 38
    bw_s = (CW - 24) / 3
    bh_s = 75
    for i, (num, l1, l2) in enumerate([
        ("\u00a34.7M", "NHS savings", "in 12 months"),
        ("285/wk", "GP appointments", "freed up"),
        ("\u00a3300K", "Saved per practice", "per year"),
    ]):
        bx = M + i * (bw_s + 12)
        c.setFillColor(CARD_BLUE)
        c.roundRect(bx, y - bh_s, bw_s, bh_s, 10, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 26)
        c.drawCentredString(bx + bw_s / 2, y - 28, num)
        c.setFillColor(LIGHT_TEXT)
        c.setFont("Helvetica", 11)
        c.drawCentredString(bx + bw_s / 2, y - 46, l1)
        if l2:
            c.drawCentredString(bx + bw_s / 2, y - 59, l2)

    # ── SECTION 2 (white) - Overview ──
    c.setFillColor(WHITE)
    c.rect(0, white1_bottom, PW, blue1_bottom - white1_bottom, fill=1, stroke=0)

    y = blue1_bottom - 35
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(M, y, "Overview")

    y -= 30
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
        check_bullet(c, M + 12, y)
        c.setFillColor(BLACK)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(M + 30, y, title)
        y -= 20
        c.setFillColor(MID_GREY)
        c.setFont("Helvetica", 11)
        for line in wrap(desc, "Helvetica", 11, CW - 34):
            c.drawString(M + 30, y, line)
            y -= 14
        y -= 12

    # ── BOTTOM BAR (blue) - Footer ──
    c.setFillColor(BLUE)
    c.rect(0, 0, PW, white1_bottom, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-BoldOblique", 14)
    c.drawCentredString(PW / 2, 52, "Safer triage. Less pressure on your practice.")

    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 10)
    c.drawString(M, 18, "smartnavigation.co.uk")
    draw_ff(c, PW - 95, 26, h=38)

    c.save()
    print(f"Created: {filename}")


if __name__ == "__main__":
    d = "/home/user/bramley-tv"
    create_poster1(os.path.join(d, "smartnav-poster-pricing.pdf"))
    create_poster2(os.path.join(d, "smartnav-poster-case-study.pdf"))
    print("Done!")
