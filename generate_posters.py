#!/usr/bin/env python3
"""Generate posters as HTML then convert to PDF with weasyprint."""
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

# ── Shared CSS for both posters ──
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
    <span class="price-period">for 12 months</span>
    <div class="price-details">
      Per practice, all-inclusive. No hidden charges.<br>
      No auto-renewals. Full onboarding, training &amp; support included.
    </div>
  </div>

  <div class="stats-grid">
    <div class="stat-box">
      <div class="stat-num">152,508</div>
      <div class="stat-label">Patients triaged (2024\u201325)</div>
    </div>
    <div class="stat-box">
      <div class="stat-num">40+</div>
      <div class="stat-label">Practices nationally</div>
    </div>
    <div class="stat-box">
      <div class="stat-num">&pound;4.7M</div>
      <div class="stat-label">NHS savings in 12 months</div>
    </div>
    <div class="stat-box">
      <div class="stat-num">71 hrs/wk</div>
      <div class="stat-label">GP time saved</div>
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
    font-size: 18px;
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
    font-size: 15px;
    opacity: 0.7;
    margin-top: 10px;
  }}
  .stats-row {{
    display: flex;
    gap: 14px;
    margin-top: 30px;
  }}
  .stats-row .stat-box {{
    flex: 1;
    padding: 22px 12px;
  }}
  .stats-row .stat-num {{
    font-size: 32px;
  }}
  .stats-row .stat-label {{
    font-size: 12px;
  }}
</style>
</head>
<body>

<div class="top-bar">
  <img src="{SN_LOGO}" alt="SMART navigation">
</div>

<div class="blue-section">
  <div class="emis-badge">EMIS Partner API \u2014 Fully Integrated</div>

  <div class="case-label">CASE STUDY</div>
  <div class="case-sub">Real-world impact across 40+ practices nationally</div>

  <div class="big-stat">
    <div class="big-stat-num">43%</div>
    <div class="big-stat-text">reduction in receptionist<br>call handling time</div>
    <div class="big-stat-sub">Barnstaple to Newcastle \u2014 from Leeds practices to 40+ nationally</div>
  </div>

  <div class="stats-row">
    <div class="stat-box">
      <div class="stat-num">&pound;4.7M</div>
      <div class="stat-label">NHS savings<br>in 12 months</div>
    </div>
    <div class="stat-box">
      <div class="stat-num">285/wk</div>
      <div class="stat-label">GP appointments<br>freed up</div>
    </div>
    <div class="stat-box">
      <div class="stat-num">&pound;300K</div>
      <div class="stat-label">Saved per practice<br>per year</div>
    </div>
  </div>
</div>

<div class="white-section">
  <h3>Overview</h3>
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
      <span>Free staff from lengthy triage calls. 71 hours of GP time saved every week.</span>
    </div>
  </div>
  <div class="bullet">
    <div class="bullet-check">\u2713</div>
    <div class="bullet-text">
      <b>Consistent, structured outcomes</b>
      <span>Every patient assessed using the same safe pathways, aligned with NICE guidance.</span>
    </div>
  </div>
  <div class="bullet">
    <div class="bullet-check">\u2713</div>
    <div class="bullet-text">
      <b>Built for NHS primary care</b>
      <span>Designed around real GP workflows. Pathways reviewed by GP clinical leads.</span>
    </div>
  </div>
  <div class="bullet">
    <div class="bullet-check">\u2713</div>
    <div class="bullet-text">
      <b>EMIS Partner API integration</b>
      <span>Seamless integration with clinical systems. Triage data uploaded into patient records.</span>
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
