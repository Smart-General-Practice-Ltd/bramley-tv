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

POSTER1_HTML = f"""<!DOCTYPE html>
<html>
<head>
<style>
  @page {{ size: 210mm 495mm; margin: 0; }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: Helvetica, Arial, sans-serif; width: 210mm; height: 495mm; }}

  .top-bar {{
    background: #fff;
    padding: 40px 0 30px;
    text-align: center;
  }}
  .top-bar img {{ height: 80px; }}

  .blue-section {{
    background: #1159A2;
    color: #fff;
    padding: 40px 42px 45px;
  }}

  .section-label {{
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 1.5px;
    opacity: 0.7;
    margin-bottom: 20px;
  }}

  .headline {{
    font-size: 40px;
    font-weight: 800;
    line-height: 1.15;
    margin-bottom: 8px;
  }}
  .headline-sub {{
    font-size: 20px;
    font-weight: 400;
    opacity: 0.8;
    margin-bottom: 12px;
  }}
  .desc {{
    font-size: 15px;
    line-height: 1.6;
    opacity: 0.75;
    margin-bottom: 30px;
  }}

  .price-card {{
    background: rgba(255,255,255,0.12);
    border-radius: 14px;
    padding: 28px 32px;
    margin-bottom: 30px;
  }}
  .price-big {{
    font-size: 62px;
    font-weight: 800;
    display: inline;
  }}
  .price-period {{
    font-size: 22px;
    font-weight: 400;
    margin-left: 10px;
  }}
  .price-details {{
    font-size: 14px;
    opacity: 0.75;
    margin-top: 12px;
    line-height: 1.7;
  }}

  .stats-grid {{
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-bottom: 10px;
  }}
  .stat-box {{
    flex: 1 1 45%;
    background: rgba(255,255,255,0.12);
    border-radius: 12px;
    padding: 22px 14px;
    text-align: center;
  }}
  .stat-num {{
    font-size: 34px;
    font-weight: 800;
  }}
  .stat-label {{
    font-size: 12px;
    opacity: 0.7;
    margin-top: 6px;
  }}

  .white-section {{
    background: #fff;
    color: #222;
    padding: 38px 42px 32px;
  }}
  .white-section h3 {{
    color: #1159A2;
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 24px;
  }}

  .bullet {{
    display: flex;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 20px;
  }}
  .bullet-check {{
    width: 28px;
    height: 28px;
    min-width: 28px;
    background: #1159A2;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 16px;
    font-weight: 700;
    margin-top: 2px;
  }}
  .bullet-text b {{
    font-size: 16px;
    display: block;
    margin-bottom: 3px;
  }}
  .bullet-text span {{
    font-size: 13px;
    color: #666;
    line-height: 1.5;
  }}

  .footer-blue {{
    background: #1159A2;
    padding: 30px 42px 24px;
    text-align: center;
  }}
  .tagline {{
    font-size: 18px;
    font-style: italic;
    color: rgba(255,255,255,0.9);
    margin-bottom: 20px;
  }}
  .footer-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .footer-url {{
    font-size: 12px;
    color: rgba(255,255,255,0.7);
  }}
  .footer-row img {{ height: 48px; }}
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
    SMART Navigation Voice guides patients through structured, clinician-designed
    triage pathways over the phone.
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
      <div class="stat-label">Patients triaged (2024–25)</div>
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
  <h3>Stage 2: Automated Voice Triage</h3>
  <div class="bullet">
    <div class="bullet-check">✓</div>
    <div class="bullet-text">
      <b>AI-led patient triage</b>
      <span>Patients speak directly to the system which guides them through safe navigation questions.</span>
    </div>
  </div>
  <div class="bullet">
    <div class="bullet-check">✓</div>
    <div class="bullet-text">
      <b>Reduce reception pressure</b>
      <span>Free staff from lengthy triage calls.</span>
    </div>
  </div>
  <div class="bullet">
    <div class="bullet-check">✓</div>
    <div class="bullet-text">
      <b>Consistent, structured outcomes</b>
      <span>Every patient assessed using the same safe pathways.</span>
    </div>
  </div>
  <div class="bullet">
    <div class="bullet-check">✓</div>
    <div class="bullet-text">
      <b>Built for NHS primary care</b>
    </div>
  </div>
</div>

<div class="footer-blue">
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
  @page {{ size: 210mm 495mm; margin: 0; }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: Helvetica, Arial, sans-serif; width: 210mm; height: 495mm; }}

  .top-bar {{
    background: #fff;
    padding: 40px 0 30px;
    text-align: center;
  }}
  .top-bar img {{ height: 80px; }}

  .blue-section {{
    background: #1159A2;
    color: #fff;
    padding: 40px 42px 45px;
  }}

  .emis-badge {{
    background: rgba(255,255,255,0.15);
    border-radius: 10px;
    padding: 16px 24px;
    text-align: center;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 28px;
  }}

  .case-label {{
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 1.5px;
    opacity: 0.7;
    margin-bottom: 12px;
  }}
  .case-sub {{
    font-size: 16px;
    opacity: 0.8;
    text-align: center;
    margin-bottom: 24px;
  }}

  .big-stat {{
    text-align: center;
    margin-bottom: 14px;
  }}
  .big-stat-num {{
    font-size: 110px;
    font-weight: 800;
    line-height: 1;
  }}
  .big-stat-text {{
    font-size: 20px;
    font-weight: 700;
    margin-top: 10px;
  }}
  .big-stat-sub {{
    font-size: 13px;
    opacity: 0.7;
    margin-top: 8px;
  }}

  .stats-row {{
    display: flex;
    gap: 12px;
    margin-top: 28px;
  }}
  .stat-box {{
    flex: 1;
    background: rgba(255,255,255,0.12);
    border-radius: 12px;
    padding: 20px 10px;
    text-align: center;
  }}
  .stat-num {{
    font-size: 28px;
    font-weight: 800;
  }}
  .stat-label {{
    font-size: 11px;
    opacity: 0.7;
    margin-top: 6px;
    line-height: 1.3;
  }}

  .white-section {{
    background: #fff;
    color: #222;
    padding: 38px 42px 32px;
  }}
  .white-section h3 {{
    color: #1159A2;
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 24px;
  }}

  .bullet {{
    display: flex;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 18px;
  }}
  .bullet-check {{
    width: 28px;
    height: 28px;
    min-width: 28px;
    background: #1159A2;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 16px;
    font-weight: 700;
    margin-top: 2px;
  }}
  .bullet-text b {{
    font-size: 15px;
    display: block;
    margin-bottom: 3px;
  }}
  .bullet-text span {{
    font-size: 12px;
    color: #666;
    line-height: 1.5;
  }}

  .footer-blue {{
    background: #1159A2;
    padding: 30px 42px 24px;
    text-align: center;
  }}
  .tagline {{
    font-size: 18px;
    font-style: italic;
    color: rgba(255,255,255,0.9);
    margin-bottom: 20px;
  }}
  .footer-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .footer-url {{
    font-size: 12px;
    color: rgba(255,255,255,0.7);
  }}
  .footer-row img {{ height: 48px; }}
</style>
</head>
<body>

<div class="top-bar">
  <img src="{SN_LOGO}" alt="SMART navigation">
</div>

<div class="blue-section">
  <div class="emis-badge">EMIS Partner API — Fully Integrated</div>

  <div class="case-label">CASE STUDY</div>
  <div class="case-sub">Real-world impact across 40+ practices nationally</div>

  <div class="big-stat">
    <div class="big-stat-num">43%</div>
    <div class="big-stat-text">reduction in receptionist<br>call handling time</div>
    <div class="big-stat-sub">Barnstaple to Newcastle — from Leeds practices to 40+ nationally</div>
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
    <div class="bullet-check">✓</div>
    <div class="bullet-text">
      <b>AI-led patient triage</b>
      <span>Patients speak directly to the system which guides them through safe navigation questions.</span>
    </div>
  </div>
  <div class="bullet">
    <div class="bullet-check">✓</div>
    <div class="bullet-text">
      <b>Reduce reception pressure</b>
      <span>Free staff from lengthy triage calls. 71 hours of GP time saved every week.</span>
    </div>
  </div>
  <div class="bullet">
    <div class="bullet-check">✓</div>
    <div class="bullet-text">
      <b>Consistent, structured outcomes</b>
      <span>Every patient assessed using the same safe pathways, aligned with NICE guidance.</span>
    </div>
  </div>
  <div class="bullet">
    <div class="bullet-check">✓</div>
    <div class="bullet-text">
      <b>Built for NHS primary care</b>
      <span>Designed around real GP workflows. Pathways reviewed by GP clinical leads.</span>
    </div>
  </div>
  <div class="bullet">
    <div class="bullet-check">✓</div>
    <div class="bullet-text">
      <b>EMIS Partner API integration</b>
      <span>Seamless integration with clinical systems. Triage data uploaded into patient records.</span>
    </div>
  </div>
</div>

<div class="footer-blue">
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
