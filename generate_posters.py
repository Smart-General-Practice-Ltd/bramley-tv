#!/usr/bin/env python3
"""Generate posters as HTML then convert to PDF with weasyprint.
All stats from smartnavigation.co.uk only."""
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

SHARED_CSS = """
  @page { size: 210mm 495mm; margin: 0; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: Helvetica, Arial, sans-serif; width: 210mm; height: 495mm; }

  .top-bar {
    background: #fff;
    padding: 44px 0 36px;
    text-align: center;
  }
  .top-bar img { height: 90px; }

  .blue-section {
    background: #1159A2;
    color: #fff;
    padding: 44px 44px 48px;
  }

  .white-section {
    background: #fff;
    color: #222;
    padding: 42px 44px 36px;
  }
  .white-section h3 {
    color: #1159A2;
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 28px;
  }

  .bullet {
    display: flex;
    align-items: flex-start;
    gap: 18px;
    margin-bottom: 22px;
  }
  .bullet-check {
    width: 32px;
    height: 32px;
    min-width: 32px;
    background: #1159A2;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 18px;
    font-weight: 700;
    margin-top: 2px;
  }
  .bullet-text b {
    font-size: 18px;
    display: block;
    margin-bottom: 4px;
  }
  .bullet-text span {
    font-size: 15px;
    color: #555;
    line-height: 1.5;
  }

  .footer-white {
    background: #fff;
    padding: 28px 44px 28px;
    border-top: 1px solid #e0e0e0;
  }
  .tagline {
    font-size: 20px;
    font-style: italic;
    color: #1159A2;
    text-align: center;
    margin-bottom: 24px;
  }
  .footer-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .footer-url {
    font-size: 14px;
    color: #888;
  }
  .footer-row img { height: 110px; }

  .stats-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
  }
  .stat-box {
    flex: 1 1 calc(50% - 14px);
    max-width: calc(50% - 7px);
    background: rgba(255,255,255,0.12);
    border-radius: 14px;
    padding: 24px 16px;
    text-align: center;
  }
  .stat-num {
    font-size: 38px;
    font-weight: 800;
  }
  .stat-label {
    font-size: 14px;
    opacity: 0.7;
    margin-top: 6px;
  }
"""

POSTER1_HTML = f"""<!DOCTYPE html>
<html>
<head>
<style>
  {SHARED_CSS}

  .section-label {{
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 1.5px;
    opacity: 0.7;
    margin-bottom: 22px;
  }}
  .headline {{
    font-size: 44px;
    font-weight: 800;
    line-height: 1.15;
    margin-bottom: 10px;
  }}
  .headline-sub {{
    font-size: 22px;
    font-weight: 400;
    opacity: 0.8;
    margin-bottom: 14px;
  }}
  .desc {{
    font-size: 17px;
    line-height: 1.6;
    opacity: 0.75;
    margin-bottom: 32px;
  }}
  .price-card {{
    background: rgba(255,255,255,0.12);
    border-radius: 14px;
    padding: 30px 34px;
    margin-bottom: 34px;
  }}
  .price-big {{
    font-size: 68px;
    font-weight: 800;
    display: inline;
  }}
  .price-period {{
    font-size: 24px;
    font-weight: 400;
    margin-left: 12px;
  }}
  .price-details {{
    font-size: 16px;
    opacity: 0.75;
    margin-top: 14px;
    line-height: 1.7;
  }}
  .price-trial {{
    font-size: 18px;
    font-weight: 700;
    margin-top: 12px;
    opacity: 0.9;
  }}
</style>
</head>
<body>

<div class="top-bar">
  <img src="{SN_LOGO}" alt="SMART navigation">
</div>

<div class="blue-section">
  <div class="section-label">STAGE 1: PRICING</div>
  <div class="headline">Simple, transparent pricing</div>
  <div class="headline-sub">designed for NHS primary care</div>
  <div class="desc">
    SMART Navigation Voice guides patients through structured,
    clinician-designed triage pathways over the phone, safely and consistently.
  </div>

  <div class="price-card">
    <div class="price-big">&pound;1,000</div>
    <span class="price-period">per practice / year</span>
    <div class="price-details">
      Flat rate. No hidden or variable costs.<br>
      Free technical support and updates included.
    </div>
    <div class="price-trial">\u2713 3 months free trial</div>
  </div>

  <div class="stats-grid">
    <div class="stat-box">
      <div class="stat-num">100+</div>
      <div class="stat-label">Practices across England</div>
    </div>
    <div class="stat-box">
      <div class="stat-num">500k+</div>
      <div class="stat-label">Patients covered</div>
    </div>
    <div class="stat-box">
      <div class="stat-num">79:1</div>
      <div class="stat-label">Return on investment</div>
    </div>
    <div class="stat-box">
      <div class="stat-num">&lt;&pound;3/day</div>
      <div class="stat-label">For a 7,000 patient practice</div>
    </div>
  </div>
</div>

<div class="white-section">
  <h3>Stage 2: Ambient Voice Technology</h3>
  <div class="bullet">
    <div class="bullet-check">\u2713</div>
    <div class="bullet-text">
      <b>Receptionist-led patient triage</b>
      <span>Patients speak directly to the system which guides them through safe navigation questions.</span>
    </div>
  </div>
  <div class="bullet">
    <div class="bullet-check">\u2713</div>
    <div class="bullet-text">
      <b>Reduce reception pressure</b>
      <span>Free staff from lengthy triage calls.</span>
    </div>
  </div>
  <div class="bullet">
    <div class="bullet-check">\u2713</div>
    <div class="bullet-text">
      <b>Consistent, structured outcomes</b>
      <span>Every patient assessed using the same safe pathways.</span>
    </div>
  </div>
  <div class="bullet">
    <div class="bullet-check">\u2713</div>
    <div class="bullet-text">
      <b>Built for NHS primary care</b>
    </div>
  </div>
</div>

<div class="footer-white">
  <div class="tagline">Safer triage.<br>Less pressure on your practice.</div>
  <div class="footer-row">
    <span class="footer-url">smartnavigation.co.uk</span>
    <img src="{FF_LOGO}" alt="Fuller and Forbes Healthcare Group">
  </div>
</div>

</body>
</html>"""

POSTER2_HTML = f"""<!DOCTYPE html>
<html>
<head>
<style>
  {SHARED_CSS}

  .emis-badge {{
    background: rgba(255,255,255,0.15);
    border-radius: 12px;
    padding: 18px 28px;
    text-align: center;
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 32px;
  }}
  .case-label {{
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 1.5px;
    opacity: 0.7;
    margin-bottom: 14px;
  }}
  .case-sub {{
    font-size: 16px;
    opacity: 0.8;
    text-align: center;
    margin-bottom: 28px;
  }}
  .big-stat {{
    text-align: center;
    margin-bottom: 16px;
  }}
  .big-stat-num {{
    font-size: 120px;
    font-weight: 800;
    line-height: 1;
  }}
  .big-stat-text {{
    font-size: 22px;
    font-weight: 700;
    margin-top: 12px;
  }}
  .big-stat-sub {{
    font-size: 14px;
    opacity: 0.7;
    margin-top: 10px;
  }}
  .breakdown {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 24px;
    margin-bottom: 10px;
  }}
  .breakdown-box {{
    flex: 1 1 calc(50% - 10px);
    max-width: calc(50% - 5px);
    background: rgba(255,255,255,0.12);
    border-radius: 12px;
    padding: 18px 12px;
    text-align: center;
  }}
  .breakdown-box .num {{
    font-size: 30px;
    font-weight: 800;
  }}
  .breakdown-box .lbl {{
    font-size: 12px;
    opacity: 0.7;
    margin-top: 4px;
  }}
  .stats-row {{
    display: flex;
    gap: 12px;
    margin-top: 14px;
  }}
  .stats-row .stat-box {{
    flex: 1;
    padding: 18px 10px;
  }}
  .stats-row .stat-num {{
    font-size: 28px;
  }}
  .stats-row .stat-label {{
    font-size: 11px;
  }}
</style>
</head>
<body>

<div class="top-bar">
  <img src="{SN_LOGO}" alt="SMART navigation">
</div>

<div class="blue-section">
  <div class="emis-badge">EMIS Partner API \u2014 Fully Integrated</div>

  <div class="case-label">12-MONTH CASE STUDY</div>
  <div class="case-sub">April 2024 \u2013 March 2025 &bull; 17 practices &bull; 152,508 patients triaged</div>

  <div class="big-stat">
    <div class="big-stat-num">47%</div>
    <div class="big-stat-text">of patients redirected<br>away from the GP</div>
  </div>

  <div class="breakdown">
    <div class="breakdown-box">
      <div class="num">15%</div>
      <div class="lbl">to eConsultations</div>
    </div>
    <div class="breakdown-box">
      <div class="num">12%</div>
      <div class="lbl">to Community Pharmacy</div>
    </div>
    <div class="breakdown-box">
      <div class="num">11%</div>
      <div class="lbl">to other clinicians<br>(Nurse, HCA)</div>
    </div>
    <div class="breakdown-box">
      <div class="num">9%</div>
      <div class="lbl">to A&amp;E / Walk-in</div>
    </div>
  </div>

  <div class="stats-row">
    <div class="stat-box">
      <div class="stat-num">&pound;1.36M</div>
      <div class="stat-label">GP cost<br>reallocated</div>
    </div>
    <div class="stat-box">
      <div class="stat-num">71,679</div>
      <div class="stat-label">GP appointments<br>avoided</div>
    </div>
    <div class="stat-box">
      <div class="stat-num">79:1</div>
      <div class="stat-label">ROI for a 7,000<br>patient practice</div>
    </div>
  </div>
</div>

<div class="white-section">
  <h3>Overview</h3>
  <div class="bullet">
    <div class="bullet-check">\u2713</div>
    <div class="bullet-text">
      <b>Receptionist-led patient triage</b>
      <span>Structured, GP-designed scripts guide your reception team to direct patients to the right care, first time.</span>
    </div>
  </div>
  <div class="bullet">
    <div class="bullet-check">\u2713</div>
    <div class="bullet-text">
      <b>Replaces the duty doctor system</b>
      <span>Frees GPs and makes better use of the whole practice team.</span>
    </div>
  </div>
  <div class="bullet">
    <div class="bullet-check">\u2713</div>
    <div class="bullet-text">
      <b>NICE CKS aligned guidance</b>
      <span>Every pathway reviewed by GP clinical leads and aligned with NICE guidance.</span>
    </div>
  </div>
  <div class="bullet">
    <div class="bullet-check">\u2713</div>
    <div class="bullet-text">
      <b>2026/27 GP contract ready</b>
      <span>Safe, consistent, auditable process for same-day access and care navigation.</span>
    </div>
  </div>
  <div class="bullet">
    <div class="bullet-check">\u2713</div>
    <div class="bullet-text">
      <b>Set up in 30 minutes</b>
      <span>Your reception team begins using structured triage immediately.</span>
    </div>
  </div>
</div>

<div class="footer-white">
  <div class="tagline">Safer triage.<br>Less pressure on your practice.</div>
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
