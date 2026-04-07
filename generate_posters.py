#!/usr/bin/env python3
"""Generate two SMART Navigation posters as HTML->PDF.
Poster 1: The Contract Poster
Poster 2: The Proof Poster
All stats from smartnavigation.co.uk."""
import os
from weasyprint import HTML
from base64 import b64encode

LOGO_DIR = "/home/user/bramley-tv"

def img_to_data_uri(path):
    with open(path, "rb") as f:
        data = b64encode(f.read()).decode()
    return f"data:image/png;base64,{data}"

SN_LOGO = img_to_data_uri(os.path.join(LOGO_DIR, "smartnavigation.logo.png"))
FF_LOGO = img_to_data_uri(os.path.join(LOGO_DIR, "Forbes and Fuller Transparent 3.png"))

# ═══════════════════════════════════════════════════════════════
# POSTER 1: THE CONTRACT POSTER
# ═══════════════════════════════════════════════════════════════

POSTER1_HTML = f"""<!DOCTYPE html>
<html>
<head>
<style>
  @page {{ size: 210mm 495mm; margin: 0; }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: Helvetica, Arial, sans-serif; width: 210mm; height: 495mm; color: #222; }}

  /* ── TOP BANNER (blue) ── */
  .top-banner {{
    background: #1159A2;
    color: #fff;
    padding: 36px 40px 32px;
    text-align: center;
  }}
  .top-banner img {{
    height: 70px;
    margin-bottom: 28px;
  }}
  .contract-quote {{
    font-size: 22px;
    font-weight: 700;
    line-height: 1.35;
    margin-bottom: 10px;
  }}
  .contract-attrib {{
    font-size: 13px;
    opacity: 0.65;
    font-style: italic;
  }}

  /* ── SUB-HEADLINE (white) ── */
  .sub-headline {{
    background: #fff;
    padding: 28px 40px;
    text-align: center;
  }}
  .sub-headline h2 {{
    font-size: 26px;
    font-weight: 800;
    color: #1159A2;
    line-height: 1.3;
  }}

  /* ── TABLE SECTION (white) ── */
  .table-section {{
    background: #fff;
    padding: 10px 40px 36px;
  }}
  .req-table {{
    width: 100%;
    border-collapse: separate;
    border-spacing: 0 10px;
  }}
  .req-table th {{
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 10px 14px;
    text-align: left;
    color: #888;
  }}
  .req-table td {{
    padding: 18px 18px;
    font-size: 15px;
    line-height: 1.45;
    vertical-align: top;
  }}
  .req-table tr td:first-child {{
    background: #f0f4f8;
    border-radius: 10px 0 0 10px;
    font-weight: 700;
    color: #333;
    width: 45%;
  }}
  .req-table tr td:last-child {{
    background: #1159A2;
    color: #fff;
    border-radius: 0 10px 10px 0;
    font-weight: 600;
  }}

  /* ── BOTTOM STRIP (blue) ── */
  .bottom-strip {{
    background: #1159A2;
    color: #fff;
    padding: 30px 40px 20px;
  }}
  .strip-features {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px 20px;
    justify-content: center;
    margin-bottom: 20px;
  }}
  .strip-feat {{
    font-size: 14px;
    font-weight: 600;
    white-space: nowrap;
  }}
  .strip-feat .dot {{
    opacity: 0.5;
    margin: 0 2px;
  }}
  .strip-url {{
    text-align: center;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 18px;
  }}
  .strip-qr {{
    text-align: center;
    font-size: 13px;
    opacity: 0.7;
    margin-bottom: 8px;
  }}

  /* ── FOOTER (white) ── */
  .footer-white {{
    background: #fff;
    padding: 20px 40px;
    border-top: 1px solid #e0e0e0;
  }}
  .footer-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .footer-url {{
    font-size: 13px;
    color: #999;
  }}
  .footer-row img {{
    height: 110px;
  }}
</style>
</head>
<body>

<div class="top-banner">
  <img src="{SN_LOGO}" alt="SMART navigation">
  <div class="contract-quote">
    &ldquo;From 1 April 2026, every clinically urgent<br>
    request must be dealt with the same day.&rdquo;
  </div>
  <div class="contract-attrib">NHS England, GP Contract 2026/27</div>
</div>

<div class="sub-headline">
  <h2>SMARTnavigation is how<br>EMIS practices deliver it.</h2>
</div>

<div class="table-section">
  <table class="req-table">
    <tr>
      <th>Contract requirement</th>
      <th>How SMARTnavigation delivers it</th>
    </tr>
    <tr>
      <td>Same-day urgent response</td>
      <td>GP-designed, NICE CKS aligned triage from the first call</td>
    </tr>
    <tr>
      <td>No &ldquo;call back tomorrow&rdquo;</td>
      <td>Structured pathway on every contact, first time</td>
    </tr>
    <tr>
      <td>Auditable same-day % for NHSE metrics</td>
      <td>Every triage logged, GPAD-mapped</td>
    </tr>
    <tr>
      <td>Online consultations uncapped</td>
      <td>Reception-led navigation absorbs the 8am rush</td>
    </tr>
  </table>
</div>

<div class="bottom-strip">
  <div class="strip-features">
    <span class="strip-feat">EMIS Partner API &mdash; fully integrated</span>
    <span class="strip-feat"><span class="dot">&bull;</span> Set up in 30 mins</span>
    <span class="strip-feat"><span class="dot">&bull;</span> 3 months free</span>
    <span class="strip-feat"><span class="dot">&bull;</span> 100+ practices</span>
    <span class="strip-feat"><span class="dot">&bull;</span> 500k+ patients</span>
  </div>
  <div class="strip-url">smartnavigation.co.uk</div>
  <div class="strip-qr">\u25a1 Scan QR to book a demo</div>
</div>

<div class="footer-white">
  <div class="footer-row">
    <span class="footer-url">smartnavigation.co.uk</span>
    <img src="{FF_LOGO}" alt="Fuller and Forbes Healthcare Group">
  </div>
</div>

</body>
</html>"""

# ═══════════════════════════════════════════════════════════════
# POSTER 2: THE PROOF POSTER
# ═══════════════════════════════════════════════════════════════

POSTER2_HTML = f"""<!DOCTYPE html>
<html>
<head>
<style>
  @page {{ size: 210mm 495mm; margin: 0; }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: Helvetica, Arial, sans-serif; width: 210mm; height: 495mm; color: #222; }}

  /* ── TOP BAR (white) ── */
  .top-bar {{
    background: #fff;
    padding: 36px 40px 24px;
    text-align: center;
  }}
  .top-bar img {{
    height: 70px;
    margin-bottom: 16px;
  }}
  .strapline {{
    font-size: 24px;
    font-weight: 800;
    color: #1159A2;
  }}

  /* ── HERO STAT SECTION (blue) ── */
  .hero-section {{
    background: #1159A2;
    color: #fff;
    padding: 40px 40px 44px;
    text-align: center;
  }}
  .case-label {{
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.5px;
    opacity: 0.6;
    margin-bottom: 6px;
  }}
  .case-sub {{
    font-size: 14px;
    opacity: 0.7;
    margin-bottom: 24px;
  }}
  .hero-num {{
    font-size: 120px;
    font-weight: 800;
    line-height: 1;
  }}
  .hero-text {{
    font-size: 22px;
    font-weight: 700;
    margin-top: 10px;
    margin-bottom: 28px;
  }}

  /* Breakdown */
  .breakdown {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 28px;
  }}
  .bd-box {{
    flex: 1 1 calc(50% - 10px);
    max-width: calc(50% - 5px);
    background: rgba(255,255,255,0.12);
    border-radius: 12px;
    padding: 16px 10px;
    text-align: center;
  }}
  .bd-box .num {{
    font-size: 32px;
    font-weight: 800;
  }}
  .bd-box .lbl {{
    font-size: 13px;
    opacity: 0.7;
    margin-top: 4px;
  }}

  /* Impact row */
  .impact-row {{
    display: flex;
    gap: 10px;
  }}
  .impact-box {{
    flex: 1;
    background: rgba(255,255,255,0.12);
    border-radius: 12px;
    padding: 16px 8px;
    text-align: center;
  }}
  .impact-box .num {{
    font-size: 24px;
    font-weight: 800;
  }}
  .impact-box .lbl {{
    font-size: 10px;
    opacity: 0.7;
    margin-top: 4px;
    line-height: 1.3;
  }}

  /* ── TESTIMONIAL (white) ── */
  .testimonial {{
    background: #fff;
    padding: 36px 40px;
  }}
  .quote-text {{
    font-size: 19px;
    font-style: italic;
    color: #333;
    line-height: 1.5;
    margin-bottom: 14px;
    position: relative;
    padding-left: 24px;
    border-left: 4px solid #1159A2;
  }}
  .quote-attr {{
    font-size: 14px;
    color: #888;
    padding-left: 28px;
  }}
  .quote-attr strong {{
    color: #333;
  }}

  /* ── PRICING STRIP (blue) ── */
  .pricing-strip {{
    background: #1159A2;
    color: #fff;
    padding: 28px 40px;
    text-align: center;
  }}
  .pricing-main {{
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 8px;
  }}
  .pricing-details {{
    font-size: 15px;
    opacity: 0.8;
    margin-bottom: 16px;
  }}
  .pricing-url {{
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 12px;
  }}
  .pricing-qr {{
    font-size: 13px;
    opacity: 0.7;
  }}

  /* ── FOOTER (white) ── */
  .footer-white {{
    background: #fff;
    padding: 20px 40px;
    border-top: 1px solid #e0e0e0;
  }}
  .footer-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .footer-url {{
    font-size: 13px;
    color: #999;
  }}
  .footer-row img {{
    height: 110px;
  }}
</style>
</head>
<body>

<div class="top-bar">
  <img src="{SN_LOGO}" alt="SMART navigation">
  <div class="strapline">Contract-ready. Already proven.</div>
</div>

<div class="hero-section">
  <div class="case-label">12-MONTH CASE STUDY</div>
  <div class="case-sub">April 2024 \u2013 March 2025 &bull; 17 practices &bull; 152,508 patients triaged</div>

  <div class="hero-num">47%</div>
  <div class="hero-text">of patients safely redirected<br>away from the GP</div>

  <div class="breakdown">
    <div class="bd-box">
      <div class="num">15%</div>
      <div class="lbl">eConsultations</div>
    </div>
    <div class="bd-box">
      <div class="num">12%</div>
      <div class="lbl">Community Pharmacy</div>
    </div>
    <div class="bd-box">
      <div class="num">11%</div>
      <div class="lbl">Other clinicians<br>(Nurse, HCA)</div>
    </div>
    <div class="bd-box">
      <div class="num">9%</div>
      <div class="lbl">A&amp;E / Walk-in</div>
    </div>
  </div>

  <div class="impact-row">
    <div class="impact-box">
      <div class="num">&pound;1.36M</div>
      <div class="lbl">GP cost<br>reallocated</div>
    </div>
    <div class="impact-box">
      <div class="num">71,679</div>
      <div class="lbl">GP appts<br>avoided</div>
    </div>
    <div class="impact-box">
      <div class="num">17,920</div>
      <div class="lbl">GP hours<br>saved</div>
    </div>
    <div class="impact-box">
      <div class="num">79:1</div>
      <div class="lbl">ROI</div>
    </div>
  </div>
</div>

<div class="testimonial">
  <div class="quote-text">
    &ldquo;We don&rsquo;t get the same 8am rush anymore&hellip;
    reception feel safer and more confident.&rdquo;
  </div>
  <div class="quote-attr">
    <strong>Adam Bolton</strong>, Practice Manager<br>
    Bramley Surgery, Leeds
  </div>
</div>

<div class="pricing-strip">
  <div class="pricing-main">&pound;1,000 / practice / year</div>
  <div class="pricing-details">3 months free trial &bull; EMIS Partner API integrated</div>
  <div class="pricing-url">smartnavigation.co.uk</div>
  <div class="pricing-qr">\u25a1 Scan QR to book a demo</div>
</div>

<div class="footer-white">
  <div class="footer-row">
    <span class="footer-url">smartnavigation.co.uk</span>
    <img src="{FF_LOGO}" alt="Fuller and Forbes Healthcare Group">
  </div>
</div>

</body>
</html>"""

if __name__ == "__main__":
    d = "/home/user/bramley-tv"
    HTML(string=POSTER1_HTML).write_pdf(os.path.join(d, "smartnav-poster-pricing.pdf"))
    print("Created: smartnav-poster-pricing.pdf")
    HTML(string=POSTER2_HTML).write_pdf(os.path.join(d, "smartnav-poster-case-study.pdf"))
    print("Created: smartnav-poster-case-study.pdf")
    print("Done!")
