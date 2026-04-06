#!/usr/bin/env python3
"""
SMART Navigation marketing posters.
Tall format (210x495mm). 4 sections: white/blue/white/blue.
Content fills every section evenly - no dead space.
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

PW = 210 * mm
PH = 495 * mm
PAGE = (PW, PH)
M = 38
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

    # 4 sections - evenly proportioned for this tall page
    TOP_H = 110          # white logo bar
    FOOTER_H = 85        # blue footer
    MIDDLE = PH - TOP_H - FOOTER_H
    BLUE_H = MIDDLE * 0.47   # blue pricing
    WHITE_H = MIDDLE * 0.53  # white usage+AVT

    s1_top = PH - TOP_H                 # blue section top
    s1_bot = s1_top - BLUE_H            # blue section bottom
    s2_top = s1_bot                      # white section top
    s2_bot = FOOTER_H                    # white section bottom

    # ── TOP BAR (white) ──
    c.setFillColor(WHITE)
    c.rect(0, s1_top, PW, TOP_H, fill=1, stroke=0)
    draw_logo(c, PW / 2 + 12, PH - 56, h=56)

    # ── BLUE SECTION: Pricing ──
    c.setFillColor(BLUE)
    c.rect(0, s1_bot, PW, BLUE_H, fill=1, stroke=0)

    # Spread content evenly across this section
    y = s1_top - 40
    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(M, y, "STAGE 1: PRICING")

    y -= 55
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 38)
    c.drawCentredString(PW / 2, y, "Simple, transparent")
    y -= 44
    c.drawCentredString(PW / 2, y, "pricing")

    y -= 30
    c.setFont("Helvetica", 17)
    c.drawCentredString(PW / 2, y, "designed for NHS primary care")

    # Price card
    y -= 55
    card_h = 135
    c.setFillColor(CARD_BLUE)
    c.roundRect(M, y - card_h, CW, card_h, 12, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 64)
    c.drawString(M + 24, y - 60, "\u00a31,000")
    pw = pdfmetrics.stringWidth("\u00a31,000", "Helvetica-Bold", 64)
    c.setFont("Helvetica", 22)
    c.drawString(M + 34 + pw, y - 50, "for 12 months")

    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 14)
    c.drawString(M + 24, y - 88, "Per practice, all-inclusive.")
    c.drawString(M + 24, y - 106, "No hidden charges. No auto-renewals.")
    c.drawString(M + 24, y - 124, "Full onboarding, training & support included.")

    y -= card_h + 40
    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica-Oblique", 13)
    c.drawCentredString(PW / 2, y, "From single-site surgeries to ICBs \u2014 one simple price.")

    # ── WHITE SECTION: Usage & AVT ──
    c.setFillColor(WHITE)
    c.rect(0, s2_bot, PW, WHITE_H, fill=1, stroke=0)

    y = s2_top - 40
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(M, y, "Usage & Adoption")

    # 2x2 stat grid - bigger boxes
    y -= 36
    bw = (CW - 16) / 2
    bh = 88

    for row in [
        [("152,508", "Patients triaged (2024\u201325)"), ("40+", "Practices nationally")],
        [("\u00a34.7M", "NHS savings in 12 months"), ("71 hrs/wk", "GP time saved")],
    ]:
        for i, (num, lbl) in enumerate(row):
            bx = M + i * (bw + 16)
            c.setFillColor(BLUE)
            c.roundRect(bx, y - bh, bw, bh, 10, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 34)
            c.drawCentredString(bx + bw / 2, y - 38, num)
            c.setFont("Helvetica", 12)
            c.drawCentredString(bx + bw / 2, y - bh + 16, lbl)
        y -= bh + 12

    # Stage 2: AVT
    y -= 16
    c.setStrokeColor(HexColor('#c8d4e0'))
    c.setLineWidth(0.5)
    c.line(M, y + 6, PW - M, y + 6)

    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(M, y - 16, "Stage 2: Automated Voice Triage")

    y -= 44
    c.setFillColor(MID_GREY)
    c.setFont("Helvetica", 13)
    for line in wrap(
        "AI-powered voice agent handles patient calls 24/7, guiding them through clinician-designed triage pathways.",
        "Helvetica", 13, CW
    ):
        c.drawString(M, y, line)
        y -= 18

    y -= 14
    for bullet in [
        "Handles overflow and out-of-hours calls automatically",
        "Same clinically-safe pathways used by receptionists",
        "Seamless handoff to human staff when needed",
    ]:
        c.setFillColor(BLUE)
        c.setFont("Helvetica", 9)
        c.drawString(M + 5, y + 2, "\u25cf")
        c.setFillColor(BLACK)
        c.setFont("Helvetica", 13)
        c.drawString(M + 20, y, bullet)
        y -= 20

    # ── BLUE FOOTER ──
    c.setFillColor(BLUE)
    c.rect(0, 0, PW, FOOTER_H, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-BoldOblique", 15)
    c.drawCentredString(PW / 2, 50, "Safer triage. Less pressure on your practice.")

    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 10)
    c.drawString(M, 18, "smartnavigation.co.uk")
    draw_ff(c, PW - 90, 26, h=38)

    c.save()
    print(f"Created: {filename}")


# ═══════════════════════════════════════════════════════════════
# POSTER 2: CASE STUDY & OVERVIEW
# ═══════════════════════════════════════════════════════════════

def create_poster2(filename):
    c = canvas.Canvas(filename, pagesize=PAGE)

    TOP_H = 135
    FOOTER_H = 85
    MIDDLE = PH - TOP_H - FOOTER_H
    BLUE_H = MIDDLE * 0.50
    WHITE_H = MIDDLE * 0.50

    s1_top = PH - TOP_H
    s1_bot = s1_top - BLUE_H
    s2_top = s1_bot
    s2_bot = FOOTER_H

    # ── TOP BAR (white) ──
    c.setFillColor(WHITE)
    c.rect(0, s1_top, PW, TOP_H, fill=1, stroke=0)
    draw_logo(c, PW / 2 + 12, PH - 46, h=50)

    # EMIS badge
    badge_w = CW - 30
    badge_y = s1_top + 16
    c.setFillColor(BLUE)
    c.roundRect((PW - badge_w) / 2, badge_y, badge_w, 38, 8, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(PW / 2, badge_y + 12, "EMIS Partner API  \u2014  Fully Integrated")

    # ── BLUE SECTION: Case Study ──
    c.setFillColor(BLUE)
    c.rect(0, s1_bot, PW, BLUE_H, fill=1, stroke=0)

    y = s1_top - 38
    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(M, y, "CASE STUDY")

    y -= 32
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 15)
    c.drawCentredString(PW / 2, y, "Real-world impact across 40+ practices nationally")

    # 43% - massive and impactful
    y -= 95
    c.setFont("Helvetica-Bold", 110)
    c.drawCentredString(PW / 2, y, "43%")

    y -= 34
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(PW / 2, y, "reduction in receptionist")
    y -= 26
    c.drawCentredString(PW / 2, y, "call handling time")

    y -= 28
    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 13)
    c.drawCentredString(PW / 2, y, "Barnstaple to Newcastle \u2014 from Leeds to 40+ nationally")

    # 3 stat boxes
    y -= 40
    bw_s = (CW - 24) / 3
    bh_s = 82
    for i, (num, l1, l2) in enumerate([
        ("\u00a34.7M", "NHS savings", "in 12 months"),
        ("285/wk", "GP appointments", "freed up"),
        ("\u00a3300K", "Saved per practice", "per year"),
    ]):
        bx = M + i * (bw_s + 12)
        c.setFillColor(CARD_BLUE)
        c.roundRect(bx, y - bh_s, bw_s, bh_s, 10, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(bx + bw_s / 2, y - 30, num)
        c.setFillColor(LIGHT_TEXT)
        c.setFont("Helvetica", 11)
        c.drawCentredString(bx + bw_s / 2, y - 50, l1)
        if l2:
            c.drawCentredString(bx + bw_s / 2, y - 64, l2)

    # ── WHITE SECTION: Overview ──
    c.setFillColor(WHITE)
    c.rect(0, s2_bot, PW, WHITE_H, fill=1, stroke=0)

    y = s2_top - 40
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(M, y, "Overview")

    y -= 36
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
        check_bullet(c, M + 14, y)
        c.setFillColor(BLACK)
        c.setFont("Helvetica-Bold", 15)
        c.drawString(M + 32, y, title)
        y -= 22
        c.setFillColor(MID_GREY)
        c.setFont("Helvetica", 12)
        for line in wrap(desc, "Helvetica", 12, CW - 38):
            c.drawString(M + 32, y, line)
            y -= 16
        y -= 16

    # ── BLUE FOOTER ──
    c.setFillColor(BLUE)
    c.rect(0, 0, PW, FOOTER_H, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-BoldOblique", 15)
    c.drawCentredString(PW / 2, 50, "Safer triage. Less pressure on your practice.")

    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 10)
    c.drawString(M, 18, "smartnavigation.co.uk")
    draw_ff(c, PW - 90, 26, h=38)

    c.save()
    print(f"Created: {filename}")


if __name__ == "__main__":
    d = "/home/user/bramley-tv"
    create_poster1(os.path.join(d, "smartnav-poster-pricing.pdf"))
    create_poster2(os.path.join(d, "smartnav-poster-case-study.pdf"))
    print("Done!")
