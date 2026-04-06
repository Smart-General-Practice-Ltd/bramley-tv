#!/usr/bin/env python3
"""
Generate two SMART Navigation marketing posters as PDF.
4 sections: white top / blue / white / blue bottom.
Content-driven sizing. Real logos.
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
MID_GREY = HexColor('#555555')
LIGHT_TEXT = HexColor('#d0ddef')

W, H = A4
M = 45
CW = W - 2 * M

LOGO_DIR = "/home/user/bramley-tv"
SMARTNAV_LOGO = os.path.join(LOGO_DIR, "smartnavigation.logo.png")
FF_LOGO = os.path.join(LOGO_DIR, "Forbes and Fuller Transparent 3.png")
if not os.path.exists(SMARTNAV_LOGO):
    SMARTNAV_LOGO = None
if not os.path.exists(FF_LOGO):
    FF_LOGO = None


def draw_logo(c, cx, y, h=50):
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
        c.setFillColor(HexColor('#333333'))
        c.setFont("Helvetica", h * 0.48)
        c.drawString(ccx + r + h * 0.08, y - h * 0.16, "navigation")


def draw_ff(c, x, y, h=35):
    if FF_LOGO:
        img = ImageReader(FF_LOGO)
        iw, ih = img.getSize()
        tw = iw * (h / ih)
        c.drawImage(FF_LOGO, x, y - h / 2, width=tw, height=h,
                     mask='auto', preserveAspectRatio=True)
    else:
        c.setFillColor(WHITE)
        c.setFont("Helvetica", 9)
        c.drawString(x, y + 4, "Fuller and Forbes")
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x, y - 7, "Healthcare Group")


def check_bullet(c, x, y, on_blue=False):
    s = 9
    c.setFillColor(WHITE if on_blue else BLUE)
    c.circle(x, y + 3, s, fill=1, stroke=0)
    c.setStrokeColor(BLUE if on_blue else WHITE)
    c.setLineWidth(2)
    c.line(x - 4, y + 2.5, x - 1, y - 1)
    c.line(x - 1, y - 1, x + 4.5, y + 6)


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
# POSTER 1
# ═══════════════════════════════════════════════════════════════

def create_poster1(filename):
    c = canvas.Canvas(filename, pagesize=A4)

    # Fixed section positions
    top_bottom = H - 85
    blue_bottom = 455   # blue section shorter - no dead space
    white_bottom = 70

    # ── TOP WHITE BAR ──
    c.setFillColor(WHITE)
    c.rect(0, top_bottom, W, H - top_bottom, fill=1, stroke=0)
    draw_logo(c, W / 2 + 10, H - 44, h=46)

    # ── BLUE SECTION: PRICING ──
    c.setFillColor(BLUE)
    c.rect(0, blue_bottom, W, top_bottom - blue_bottom, fill=1, stroke=0)

    y = top_bottom - 30
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "STAGE 1: PRICING")

    # Headline - single line
    y -= 38
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(W / 2, y, "Simple, transparent pricing")
    y -= 20
    c.setFont("Helvetica", 13)
    c.drawCentredString(W / 2, y, "designed for NHS primary care")

    # Price box
    y -= 32
    card_h = 88
    c.setFillColor(CARD_BLUE)
    c.roundRect(M, y - card_h, CW, card_h, 10, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 46)
    c.drawString(M + 20, y - 44, "\u00a31,000")
    pw = pdfmetrics.stringWidth("\u00a31,000", "Helvetica-Bold", 46)
    c.setFont("Helvetica", 17)
    c.drawString(M + 28 + pw, y - 36, "for 12 months")

    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 11)
    c.drawString(M + 20, y - 62, "Per practice, all-inclusive. No hidden charges.")
    c.drawString(M + 20, y - 76, "No auto-renewals. Full onboarding, training & support included.")

    y -= card_h + 18
    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica-Oblique", 10.5)
    c.drawCentredString(W / 2, y, "From single-site surgeries to ICBs \u2014 one simple price.")

    # ── WHITE SECTION: USAGE & AVT ──
    c.setFillColor(WHITE)
    c.rect(0, white_bottom, W, blue_bottom - white_bottom, fill=1, stroke=0)

    y = blue_bottom - 28
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(M, y, "Usage & Adoption")

    # 2x2 stat grid
    y -= 26
    bw = (CW - 14) / 2
    bh = 64

    for row in [
        [("152,508", "Patients triaged (2024\u201325)"), ("40+", "Practices nationally")],
        [("\u00a34.7M", "NHS savings in 12 months"), ("71 hrs/wk", "GP time saved")],
    ]:
        for i, (num, lbl) in enumerate(row):
            bx = M + i * (bw + 14)
            c.setFillColor(BLUE)
            c.roundRect(bx, y - bh, bw, bh, 8, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 26)
            c.drawCentredString(bx + bw / 2, y - 27, num)
            c.setFont("Helvetica", 10)
            c.drawCentredString(bx + bw / 2, y - bh + 12, lbl)
        y -= bh + 8

    # Stage 2: AVT
    y -= 6
    c.setStrokeColor(HexColor('#c8d4e0'))
    c.setLineWidth(0.5)
    c.line(M, y + 4, W - M, y + 4)

    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(M, y - 12, "Stage 2: Automated Voice Triage")

    y -= 28
    c.setFillColor(MID_GREY)
    c.setFont("Helvetica", 10.5)
    c.drawString(M, y, "AI-powered voice agent handles patient calls 24/7, guiding")
    y -= 14
    c.drawString(M, y, "them through clinician-designed triage pathways.")

    y -= 18
    for bullet in [
        "Handles overflow and out-of-hours calls automatically",
        "Same clinically-safe pathways used by receptionists",
        "Seamless handoff to human staff when needed",
    ]:
        c.setFillColor(BLUE)
        c.setFont("Helvetica", 7)
        c.drawString(M + 4, y + 2, "\u25cf")
        c.setFillColor(BLACK)
        c.setFont("Helvetica", 10.5)
        c.drawString(M + 16, y, bullet)
        y -= 15

    # ── BLUE FOOTER ──
    c.setFillColor(BLUE)
    c.rect(0, 0, W, white_bottom, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-BoldOblique", 13)
    c.drawCentredString(W / 2, 42, "Safer triage. Less pressure on your practice.")

    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 9)
    c.drawString(M, 14, "smartnavigation.co.uk")
    draw_ff(c, W - 185, 18, h=34)

    c.save()
    print(f"Created: {filename}")


# ═══════════════════════════════════════════════════════════════
# POSTER 2
# ═══════════════════════════════════════════════════════════════

def create_poster2(filename):
    c = canvas.Canvas(filename, pagesize=A4)

    # Fixed section positions
    top = H
    top_bottom = H - 110

    blue_bottom = 370

    white_bottom = 70

    # ── TOP WHITE BAR ──
    c.setFillColor(WHITE)
    c.rect(0, top_bottom, W, top - top_bottom, fill=1, stroke=0)
    draw_logo(c, W / 2 + 10, H - 36, h=40)

    # EMIS badge
    bw = CW - 50
    by = top_bottom + 12
    c.setFillColor(BLUE)
    c.roundRect((W - bw) / 2, by, bw, 32, 6, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(W / 2, by + 10, "EMIS Partner API  \u2014  Fully Integrated")

    # ── BLUE SECTION: CASE STUDY ──
    c.setFillColor(BLUE)
    c.rect(0, blue_bottom, W, top_bottom - blue_bottom, fill=1, stroke=0)

    y = top_bottom - 32
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "CASE STUDY")

    y -= 24
    c.setFont("Helvetica", 13)
    c.drawCentredString(W / 2, y, "Real-world impact across 40+ practices nationally")

    # 43% - massive and impactful
    y -= 70
    c.setFont("Helvetica-Bold", 90)
    c.drawCentredString(W / 2, y, "43%")

    y -= 26
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(W / 2, y, "reduction in receptionist call")
    y -= 20
    c.drawCentredString(W / 2, y, "handling time")

    y -= 20
    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 11)
    c.drawCentredString(W / 2, y, "Barnstaple to Newcastle \u2014 from Leeds to 40+ nationally")

    # 3 stat boxes - bigger text
    y -= 32
    bw_s = (CW - 28) / 3
    bh_s = 65
    for i, (num, l1, l2) in enumerate([
        ("\u00a34.7M", "NHS savings", "in 12 months"),
        ("285/wk", "GP appointments", "freed up"),
        ("\u00a3300K", "Saved per practice", "per year"),
    ]):
        bx = M + i * (bw_s + 14)
        c.setFillColor(CARD_BLUE)
        c.roundRect(bx, y - bh_s, bw_s, bh_s, 8, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(bx + bw_s / 2, y - 24, num)
        c.setFillColor(LIGHT_TEXT)
        c.setFont("Helvetica", 9.5)
        c.drawCentredString(bx + bw_s / 2, y - 42, l1)
        if l2:
            c.drawCentredString(bx + bw_s / 2, y - 53, l2)

    # ── WHITE SECTION: OVERVIEW ──
    c.setFillColor(WHITE)
    c.rect(0, white_bottom, W, blue_bottom - white_bottom, fill=1, stroke=0)

    y = blue_bottom - 30
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(M, y, "Overview")

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
        check_bullet(c, M + 11, y)
        c.setFillColor(BLACK)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(M + 28, y, title)
        y -= 16
        c.setFillColor(MID_GREY)
        c.setFont("Helvetica", 9.5)
        for line in wrap(desc, "Helvetica", 9.5, CW - 32):
            c.drawString(M + 28, y, line)
            y -= 12
        y -= 8

    # ── BLUE FOOTER ──
    c.setFillColor(BLUE)
    c.rect(0, 0, W, white_bottom, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-BoldOblique", 13)
    c.drawCentredString(W / 2, 42, "Safer triage. Less pressure on your practice.")

    c.setFillColor(LIGHT_TEXT)
    c.setFont("Helvetica", 9)
    c.drawString(M, 14, "smartnavigation.co.uk")
    draw_ff(c, W - 185, 18, h=34)

    c.save()
    print(f"Created: {filename}")


if __name__ == "__main__":
    d = "/home/user/bramley-tv"
    create_poster1(os.path.join(d, "smartnav-poster-pricing.pdf"))
    create_poster2(os.path.join(d, "smartnav-poster-case-study.pdf"))
    print("Done!")
