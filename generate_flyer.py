#!/usr/bin/env python3
"""Generate SMART Navigation conference flyer as HTML -> PDF.
Size: A5 portrait (148mm x 210mm).
Magpies colour palette, typography, QR/logo footer, stat boxes from
generate_posters.py. Colour scheme: #1159A2 and white only."""
import os
from base64 import b64encode
from io import BytesIO
import qrcode

LOGO_DIR = os.path.dirname(os.path.abspath(__file__))


def img_to_data_uri(path):
    with open(path, "rb") as f:
        data = b64encode(f.read()).decode()
    return f"data:image/png;base64,{data}"


def make_qr(url, fill='#1159A2', back='white'):
    qr = qrcode.QRCode(version=1, box_size=20, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill, back_color=back)
    buf = BytesIO()
    img.save(buf, format='PNG')
    data = b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{data}"


SN_LOGO = img_to_data_uri(os.path.join(LOGO_DIR, "smartnavigation.logo.png"))
FF_LOGO = img_to_data_uri(os.path.join(LOGO_DIR, "Forbes and Fuller Transparent 3.png"))
QR_BLUE = make_qr('https://smartnavigation.co.uk', fill='#1159A2', back='white')

FLYER_HTML = f"""<!DOCTYPE html>
<html>
<head>
<style>
  @page {{ size: 148mm 210mm; margin: 0; }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: Helvetica, Arial, sans-serif; width: 148mm; height: 210mm; color: #1a1a1a; }}

  /* ── Top band (logo + price/offer) ───────────────────────────────── */
  .top {{
    display: flex;
    height: 48mm;
  }}
  .top-left {{
    flex: 1;
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 5mm;
  }}
  .top-left img {{
    max-width: 100%;
    max-height: 20mm;
  }}
  .top-right {{
    flex: 1;
    background: #1159A2;
    color: #fff;
    padding: 6mm 6mm 5mm;
    position: relative;
    overflow: hidden;
  }}
  .top-right::after {{
    content: '';
    position: absolute;
    top: 0; right: 0; bottom: 0; width: 55%;
    background: repeating-linear-gradient(
      -60deg,
      transparent 0, transparent 1.5mm,
      rgba(255,255,255,0.06) 1.5mm, rgba(255,255,255,0.06) 1.6mm
    );
    pointer-events: none;
  }}
  .price-block {{
    position: relative;
    z-index: 1;
  }}
  .price {{
    font-size: 34pt;
    font-weight: 400;
    line-height: 0.95;
    letter-spacing: -1px;
    display: inline-block;
  }}
  .price-year {{
    display: block;
    font-size: 11pt;
    font-weight: 400;
    text-align: right;
    margin-top: -1mm;
    padding-right: 2mm;
    opacity: 0.95;
  }}
  .offer {{
    position: relative;
    z-index: 1;
    margin-top: 6mm;
    font-size: 12pt;
    font-style: italic;
    line-height: 1.25;
  }}
  .offer b {{ font-weight: 800; font-style: italic; }}

  /* ── Contract banner ────────────────────────────────────────────── */
  .contract {{
    height: 19mm;
    background: #fff;
    color: #1159A2;
    padding: 3.5mm 6mm 3mm;
    text-align: center;
    border-top: 0.6mm solid #1159A2;
    border-bottom: 0.6mm solid #1159A2;
  }}
  .contract-tag {{
    font-size: 7.5pt;
    font-weight: 800;
    letter-spacing: 2.4px;
    color: #1159A2;
    margin-bottom: 1.2mm;
  }}
  .contract-quote {{
    font-size: 10.5pt;
    font-weight: 700;
    line-height: 1.25;
    color: #1a1a1a;
    margin-bottom: 1.4mm;
  }}
  .contract-quote em {{
    font-style: normal;
    color: #1159A2;
  }}
  .contract-payoff {{
    font-size: 8pt;
    font-weight: 600;
    color: #1159A2;
    font-style: italic;
  }}

  /* ── Info band (What is it? / Use Case) ──────────────────────────── */
  .info {{
    display: flex;
    height: 65mm;
  }}
  .info-left {{
    flex: 1;
    background: #1159A2;
    color: #fff;
    padding: 5mm 5.5mm 4mm;
  }}
  .info-right {{
    flex: 1;
    background: #fff;
    color: #1a1a1a;
    padding: 5mm 5.5mm 4mm;
  }}
  .section-title {{
    font-size: 14pt;
    font-weight: 800;
    margin-bottom: 1.5mm;
  }}
  .title-rule {{
    display: flex;
    gap: 4px;
    margin-bottom: 3mm;
  }}
  .title-rule span {{
    height: 1.4px;
    flex: 1;
    background: currentColor;
  }}
  .title-rule span:first-child {{
    flex: 1.4;
  }}
  .title-rule span:last-child {{
    opacity: 0.5;
  }}
  .info p {{
    font-size: 7pt;
    line-height: 1.35;
    margin-bottom: 2mm;
    text-align: justify;
  }}
  .tick-list {{
    list-style: none;
    margin-top: 2mm;
  }}
  .tick-list li {{
    display: flex;
    align-items: center;
    gap: 2.5mm;
    margin-bottom: 1.8mm;
    font-size: 8pt;
    font-weight: 700;
  }}
  .tick {{
    width: 4mm;
    height: 4mm;
    background: #1159A2;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    position: relative;
  }}
  .tick::after {{
    content: '';
    width: 2mm;
    height: 1mm;
    border-left: 1px solid #fff;
    border-bottom: 1px solid #fff;
    transform: rotate(-45deg) translate(0.1mm, -0.2mm);
  }}

  /* ── Features band (3+3 grid) ───────────────────────────────────── */
  .features {{
    display: flex;
    height: 54mm;
  }}
  .features-col {{
    flex: 1;
    padding: 4mm 4.5mm 3mm;
    display: flex;
    flex-direction: column;
    gap: 2.5mm;
  }}
  .features-left {{ background: #fff; }}
  .features-right {{ background: #eef3fa; }}
  .feat {{
    display: flex;
    gap: 2.5mm;
    align-items: flex-start;
  }}
  .feat-icon {{
    width: 10mm;
    height: 10mm;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .feat-icon svg {{
    width: 10mm;
    height: 10mm;
  }}
  .feat-body h4 {{
    font-size: 8.5pt;
    font-weight: 800;
    margin-bottom: 0.8mm;
    color: #1a1a1a;
    line-height: 1.15;
  }}
  .feat-body p {{
    font-size: 6.6pt;
    line-height: 1.3;
    color: #333;
    text-align: justify;
  }}

  /* ── Contact strip ──────────────────────────────────────────────── */
  .contact {{
    display: flex;
    height: 16mm;
    background: linear-gradient(90deg, #7aa9dc 0%, #2d6bb3 50%, #7aa9dc 100%);
    color: #fff;
    align-items: center;
    padding: 0 5mm;
    gap: 3mm;
  }}
  .scan {{
    display: flex;
    align-items: center;
    gap: 1.5mm;
    flex: 0 0 auto;
  }}
  .scan-text {{
    font-size: 10pt;
    font-weight: 700;
    line-height: 1;
  }}
  .scan-arrow {{
    width: 7mm;
    height: 5mm;
    margin-top: 0.5mm;
  }}
  .scan img.qr {{
    height: 12mm;
    width: 12mm;
    background: #fff;
    padding: 0.5mm;
    border-radius: 1mm;
  }}
  .contact-details {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 1.3mm;
    padding-left: 3mm;
  }}
  .contact-row {{
    display: flex;
    align-items: center;
    gap: 2.5mm;
    font-size: 8pt;
  }}
  .contact-icon {{
    width: 4mm;
    height: 4mm;
    background: #fff;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: #1159A2;
    flex-shrink: 0;
  }}
  .contact-icon svg {{
    width: 2.4mm;
    height: 2.4mm;
  }}

  /* ── Footer ─────────────────────────────────────────────────────── */
  .footer {{
    display: flex;
    height: 8mm;
    background: #fff;
    align-items: center;
    justify-content: space-between;
    padding: 0 5mm;
  }}
  .footer img {{
    max-height: 6mm;
  }}
  .footer .ff {{ max-height: 7mm; }}

  /* SMART general practice logo built in HTML/CSS */
  .sgp-logo {{
    display: flex;
    align-items: center;
    gap: 1.5mm;
    height: 6mm;
  }}
  .sgp-circle {{
    width: 6mm;
    height: 6mm;
    border-radius: 50%;
    background: #1159A2;
    color: #fff;
    font-size: 4.8pt;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    letter-spacing: 0.2px;
  }}
  .sgp-text {{
    font-size: 9pt;
    font-weight: 400;
    color: #1159A2;
    line-height: 1;
    position: relative;
  }}
  .sgp-tm {{
    font-size: 4pt;
    vertical-align: super;
    margin-left: 0.3mm;
    font-weight: 600;
  }}
</style>
</head>
<body>

<!-- Top band -->
<div class="top">
  <div class="top-left">
    <img src="{SN_LOGO}" alt="SMART navigation">
  </div>
  <div class="top-right">
    <div class="price-block">
      <span class="price">&pound;1,000</span>
      <span class="price-year">/year</span>
    </div>
    <div class="offer">3 months <b>free</b> &ndash;<br>Conference Offer</div>
  </div>
</div>

<!-- Contract banner -->
<div class="contract">
  <div class="contract-tag">BUILT AROUND THE 2026/27 GP CONTRACT</div>
  <div class="contract-quote">&ldquo;Clinically urgent requests must be dealt with on the same day.&rdquo;</div>
  <div class="contract-payoff">SMARTnavigation is how you deliver it.</div>
</div>

<!-- Info band -->
<div class="info">
  <div class="info-left">
    <div class="section-title">What is it?</div>
    <div class="title-rule"><span></span><span></span></div>
    <p>For years, practices have relied on a duty doctor to handle same day demand &mdash; a model that&rsquo;s no longer sustainable. Receptionists are the first point of contact but are left making clinical decisions without enough support. SMARTnavigation fixes this.</p>
    <p>SMARTnavigation guides patients through GP-designed, condition-specific pathways and supports automatic write-back into the clinical record. This reduces admin, improves triage accuracy, and helps practices manage demand more safely and efficiently.</p>
  </div>
  <div class="info-right">
    <div class="section-title">Use Case</div>
    <div class="title-rule" style="color:#1159A2;"><span></span><span></span></div>
    <p>(April 2024&ndash;March 2025) from 17 practices, 152,508 patients triaged.</p>
    <p>47% of patients were redirected away from the GP.</p>
    <ul class="tick-list">
      <li><span class="tick"></span>15% to econsultations</li>
      <li><span class="tick"></span>12% to community pharmacy</li>
      <li><span class="tick"></span>11% to other clinicians (Nurse, HCA)</li>
      <li><span class="tick"></span>9% to A&amp;E/WIC</li>
    </ul>
  </div>
</div>

<!-- Features band -->
<div class="features">
  <div class="features-col features-left">
    <div class="feat">
      <div class="feat-icon">
        <svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
          <circle cx="19" cy="22" r="13" fill="none" stroke="#1a1a1a" stroke-width="1.8"/>
          <text x="19" y="26" text-anchor="middle" font-family="Helvetica" font-weight="700" font-size="9" fill="#1a1a1a">AGE</text>
          <circle cx="32" cy="10" r="5" fill="#1159A2"/>
          <path d="M32 7.6v4.8 M29.6 10h4.8" stroke="#fff" stroke-width="1.3" stroke-linecap="round"/>
        </svg>
      </div>
      <div class="feat-body">
        <h4>Age Triage</h4>
        <p>Each script begins with age related triage adapting the questions to the patients age.</p>
      </div>
    </div>
    <div class="feat">
      <div class="feat-icon">
        <svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
          <path d="M20 5 L36 33 L4 33 Z" fill="none" stroke="#1a1a1a" stroke-width="2" stroke-linejoin="round"/>
          <path d="M20 5 L36 33 L20 33 Z" fill="#1159A2"/>
          <rect x="18.7" y="15" width="2.6" height="9" fill="#fff" rx="1"/>
          <rect x="18.7" y="26" width="2.6" height="2.6" fill="#fff" rx="0.6"/>
        </svg>
      </div>
      <div class="feat-body">
        <h4>Red Flag Screening</h4>
        <p>Condition specific red flag patients guide patients away from Primary Care.</p>
      </div>
    </div>
    <div class="feat">
      <div class="feat-icon">
        <svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
          <circle cx="23" cy="23" r="11" fill="none" stroke="#1a1a1a" stroke-width="1.8"/>
          <path d="M23 23 L23 16 M23 23 L28.5 23" stroke="#1159A2" stroke-width="2" stroke-linecap="round"/>
          <rect x="20" y="8" width="6" height="2" rx="0.6" fill="#1a1a1a"/>
          <rect x="22" y="6" width="2" height="3" rx="0.4" fill="#1a1a1a"/>
          <path d="M32 14 l3 -3" stroke="#1a1a1a" stroke-width="1.6" stroke-linecap="round"/>
          <path d="M4 22 L10 21 M3 27 L11 26 M4 31 L9 30" stroke="#1159A2" stroke-width="1.4" stroke-linecap="round"/>
        </svg>
      </div>
      <div class="feat-body">
        <h4>Same Day Triage</h4>
        <p>Same day condition specific questions book patients into same day appointments making the best use of available clinical capacity.</p>
      </div>
    </div>
  </div>

  <div class="features-col features-right">
    <div class="feat">
      <div class="feat-icon">
        <svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
          <path d="M20 5 L36 33 L4 33 Z" fill="none" stroke="#1a1a1a" stroke-width="2" stroke-linejoin="round"/>
          <path d="M20 5 L36 33 L20 33 Z" fill="#1159A2"/>
          <rect x="18.7" y="15" width="2.6" height="9" fill="#fff" rx="1"/>
          <rect x="18.7" y="26" width="2.6" height="2.6" fill="#fff" rx="0.6"/>
        </svg>
      </div>
      <div class="feat-body">
        <h4>Ambient Voice Technology</h4>
        <p>In a Leeds practice, we are currently trialling an ambient voice that answers calls, triages patients and books appointments on SMARTnavigation scripts &mdash; a digital front door, not a chatbot.</p>
      </div>
    </div>
    <div class="feat">
      <div class="feat-icon">
        <svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
          <path d="M14 6 h12 v8 h8 v12 h-8 v8 h-12 v-8 h-8 v-12 h8 z" fill="#1159A2"/>
        </svg>
      </div>
      <div class="feat-body">
        <h4>Pharmacy First</h4>
        <p>Filters patients into bookable appointment slots with a Pharmacist to prevent patient looping.</p>
      </div>
    </div>
    <div class="feat">
      <div class="feat-icon">
        <svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
          <path d="M8 16 A13 13 0 0 1 31 11" fill="none" stroke="#1a1a1a" stroke-width="1.8" stroke-linecap="round"/>
          <polygon points="33,13 29,5 24,11" fill="#1a1a1a"/>
          <path d="M32 24 A13 13 0 0 1 9 29" fill="none" stroke="#1a1a1a" stroke-width="1.8" stroke-linecap="round"/>
          <polygon points="7,27 11,35 16,29" fill="#1a1a1a"/>
          <circle cx="20" cy="20" r="6.5" fill="#1159A2"/>
          <polygon points="18,16.5 24.5,20 18,23.5" fill="#fff"/>
        </svg>
      </div>
      <div class="feat-body">
        <h4>EMIS Write-Back</h4>
        <p>Automatic write-back into EMIS &mdash; no PDFs, no manual steps. Live rollout.</p>
      </div>
    </div>
  </div>
</div>

<!-- Contact strip -->
<div class="contact">
  <div class="scan">
    <div>
      <div class="scan-text">Scan here</div>
      <svg class="scan-arrow" viewBox="0 0 40 30" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M4 4 Q 8 26 32 22"/>
        <path d="M32 22 l-6 -3 M32 22 l-3 6"/>
      </svg>
    </div>
    <img class="qr" src="{QR_BLUE}" alt="Scan for SMARTnavigation">
  </div>
  <div class="contact-details">
    <div class="contact-row">
      <span class="contact-icon">
        <svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round">
          <rect x="2.5" y="5" width="15" height="10" rx="0.8"/>
          <path d="M2.5 5 L10 11 L17.5 5"/>
        </svg>
      </span>
      enquiries@smartgeneralpractice.com
    </div>
    <div class="contact-row">
      <span class="contact-icon">
        <svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="10" cy="10" r="7.5"/>
          <ellipse cx="10" cy="10" rx="3.5" ry="7.5"/>
          <path d="M2.5 10 h15"/>
        </svg>
      </span>
      www.smartnavigation.co.uk
    </div>
  </div>
</div>

<!-- Footer logos -->
<div class="footer">
  <img class="ff" src="{FF_LOGO}" alt="Fuller and Forbes Healthcare Group">
  <div class="sgp-logo">
    <span class="sgp-circle">SMART</span>
    <span class="sgp-text">general practice<span class="sgp-tm">TM</span></span>
  </div>
</div>

</body>
</html>"""

if __name__ == "__main__":
    html_out = os.path.join(LOGO_DIR, "smartnav-flyer-conference.html")
    with open(html_out, "w", encoding="utf-8") as f:
        f.write(FLYER_HTML)
    print(f"Created: {html_out}")

    from weasyprint import HTML
    out = os.path.join(LOGO_DIR, "smartnav-flyer-conference.pdf")
    HTML(string=FLYER_HTML).write_pdf(out)
    print(f"Created: {out}")
    print("Done!")
