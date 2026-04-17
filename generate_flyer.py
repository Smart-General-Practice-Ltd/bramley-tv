#!/usr/bin/env python3
"""Generate SMART Navigation conference flyer as HTML -> PDF.
Size: A5 portrait (148mm x 210mm).
Magpies colour palette, typography, QR/logo footer, stat boxes from
generate_posters.py but reflows to A5."""
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

# SMART general practice mark (reuses the SMARTnavigation blue circle feel)
SGP_LOGO = SN_LOGO  # fallback - swap in bespoke asset when available

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
    height: 52mm;
  }}
  .top-left {{
    flex: 1;
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 6mm;
  }}
  .top-left img {{
    max-width: 100%;
    max-height: 22mm;
  }}
  .top-right {{
    flex: 1;
    background: #1159A2;
    color: #fff;
    padding: 7mm 7mm 6mm;
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
  .price {{
    font-size: 38pt;
    font-weight: 400;
    line-height: 1;
    letter-spacing: -1px;
  }}
  .price-year {{
    font-size: 14pt;
    font-weight: 400;
    margin-left: 2mm;
    opacity: 0.95;
  }}
  .offer {{
    margin-top: 8mm;
    font-size: 13pt;
    font-style: italic;
    line-height: 1.25;
  }}
  .offer b {{ font-weight: 700; font-style: italic; }}

  /* ── Info band (What is it? / Use Case) ──────────────────────────── */
  .info {{
    display: flex;
    height: 73mm;
  }}
  .info-left {{
    flex: 1;
    background: #1159A2;
    color: #fff;
    padding: 6mm 6mm 5mm;
  }}
  .info-right {{
    flex: 1;
    background: #fff;
    color: #1a1a1a;
    padding: 6mm 6mm 5mm;
  }}
  .section-title {{
    font-size: 15pt;
    font-weight: 800;
    margin-bottom: 2mm;
  }}
  .title-rule {{
    display: flex;
    gap: 4px;
    margin-bottom: 4mm;
  }}
  .title-rule span {{
    height: 1.6px;
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
    font-size: 7.8pt;
    line-height: 1.35;
    margin-bottom: 2.5mm;
    text-align: justify;
  }}
  .info-right p {{
    color: #1a1a1a;
  }}
  .tick-list {{
    list-style: none;
    margin-top: 3mm;
  }}
  .tick-list li {{
    display: flex;
    align-items: center;
    gap: 3mm;
    margin-bottom: 2.5mm;
    font-size: 8.5pt;
    font-weight: 700;
  }}
  .tick {{
    width: 4.5mm;
    height: 4.5mm;
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
    width: 2.2mm;
    height: 1.1mm;
    border-left: 1.1px solid #fff;
    border-bottom: 1.1px solid #fff;
    transform: rotate(-45deg) translate(0.1mm, -0.3mm);
  }}

  /* ── Features band (3+3 grid) ───────────────────────────────────── */
  .features {{
    display: flex;
    height: 60mm;
  }}
  .features-col {{
    flex: 1;
    padding: 5mm 5mm 4mm;
    display: flex;
    flex-direction: column;
    gap: 3mm;
  }}
  .features-left {{ background: #fff; }}
  .features-right {{ background: #eef3fa; }}
  .feat {{
    display: flex;
    gap: 3mm;
    align-items: flex-start;
  }}
  .feat-icon {{
    width: 11mm;
    height: 11mm;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .feat-icon svg {{
    width: 11mm;
    height: 11mm;
  }}
  .feat-body h4 {{
    font-size: 9pt;
    font-weight: 800;
    margin-bottom: 1mm;
    color: #1a1a1a;
  }}
  .feat-body p {{
    font-size: 7pt;
    line-height: 1.3;
    color: #333;
    text-align: justify;
  }}

  /* ── Contact strip ──────────────────────────────────────────────── */
  .contact {{
    display: flex;
    height: 17mm;
    background: linear-gradient(90deg, #7aa9dc 0%, #2d6bb3 50%, #7aa9dc 100%);
    color: #fff;
    align-items: center;
    padding: 0 6mm;
    gap: 4mm;
  }}
  .scan {{
    display: flex;
    align-items: center;
    gap: 2mm;
    flex: 0 0 auto;
  }}
  .scan-text {{
    font-size: 11pt;
    font-weight: 700;
  }}
  .scan-arrow {{
    width: 8mm;
    height: 6mm;
  }}
  .scan img.qr {{
    height: 13mm;
    width: 13mm;
    background: #fff;
    padding: 0.6mm;
    border-radius: 1mm;
  }}
  .contact-details {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 1.5mm;
    padding-left: 4mm;
  }}
  .contact-row {{
    display: flex;
    align-items: center;
    gap: 3mm;
    font-size: 8.5pt;
  }}
  .contact-icon {{
    width: 4.5mm;
    height: 4.5mm;
    background: #fff;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: #1159A2;
    flex-shrink: 0;
  }}
  .contact-icon svg {{
    width: 2.8mm;
    height: 2.8mm;
  }}

  /* ── Footer ─────────────────────────────────────────────────────── */
  .footer {{
    display: flex;
    height: 8mm;
    background: #fff;
    align-items: center;
    justify-content: space-between;
    padding: 0 6mm;
  }}
  .footer img {{
    max-height: 6mm;
  }}
  .footer .ff {{ max-height: 7mm; }}
</style>
</head>
<body>

<!-- Top band -->
<div class="top">
  <div class="top-left">
    <img src="{SN_LOGO}" alt="SMART navigation">
  </div>
  <div class="top-right">
    <div class="price">&pound;1,000<span class="price-year">/year</span></div>
    <div class="offer">3 months <b>free</b> &ndash;<br>Conference Offer</div>
  </div>
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
          <circle cx="20" cy="20" r="14" fill="none" stroke="#1a1a1a" stroke-width="1.8"/>
          <text x="20" y="24" text-anchor="middle" font-family="Helvetica" font-weight="700" font-size="9" fill="#1a1a1a">AGE</text>
          <circle cx="32" cy="10" r="5" fill="#1159A2"/>
          <path d="M32 7.5v5 M29.5 10h5" stroke="#fff" stroke-width="1.2" stroke-linecap="round"/>
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
          <path d="M20 5 L36 33 L4 33 Z" fill="none" stroke="#1a1a1a" stroke-width="1.8" stroke-linejoin="round"/>
          <path d="M20 5 L36 33 L20 33 Z" fill="#1159A2"/>
          <rect x="18.8" y="14" width="2.4" height="10" fill="#fff"/>
          <rect x="18.8" y="26" width="2.4" height="2.4" fill="#fff"/>
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
          <circle cx="22" cy="22" r="11" fill="none" stroke="#1a1a1a" stroke-width="1.8"/>
          <path d="M22 22 L22 15 M22 22 L28 22" stroke="#1159A2" stroke-width="2" stroke-linecap="round"/>
          <path d="M18 9 h8" stroke="#1a1a1a" stroke-width="1.8" stroke-linecap="round"/>
          <path d="M30 14 l3 -3" stroke="#1a1a1a" stroke-width="1.8" stroke-linecap="round"/>
          <path d="M4 28 L10 26 M4 32 L12 30 M4 36 L8 35" stroke="#1159A2" stroke-width="1.6" stroke-linecap="round"/>
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
          <path d="M20 5 L36 33 L4 33 Z" fill="none" stroke="#1a1a1a" stroke-width="1.8" stroke-linejoin="round"/>
          <path d="M20 5 L36 33 L20 33 Z" fill="#1159A2"/>
          <rect x="18.8" y="14" width="2.4" height="10" fill="#fff"/>
          <rect x="18.8" y="26" width="2.4" height="2.4" fill="#fff"/>
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
          <circle cx="20" cy="20" r="7" fill="#1159A2"/>
          <polygon points="18,17 25,20 18,23" fill="#fff"/>
          <path d="M20 5 a15 15 0 0 1 13 7" fill="none" stroke="#1a1a1a" stroke-width="1.6" stroke-linecap="round"/>
          <path d="M33 12 l1 -4 l-4 1" fill="#1a1a1a"/>
          <path d="M33 28 a15 15 0 0 1 -13 7" fill="none" stroke="#1a1a1a" stroke-width="1.6" stroke-linecap="round"/>
          <path d="M20 35 l4 1 l-1 -4" fill="#1a1a1a"/>
          <path d="M7 28 a15 15 0 0 1 -2 -8" fill="none" stroke="#1a1a1a" stroke-width="1.6" stroke-linecap="round"/>
          <path d="M5 20 l-3 2 l2 2" fill="none" stroke="#1a1a1a" stroke-width="1.6" stroke-linecap="round"/>
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
      <svg class="scan-arrow" viewBox="0 0 40 30" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round">
        <path d="M4 6 Q 20 28 34 18"/>
        <path d="M34 18 l-5 -2 M34 18 l-2 5"/>
      </svg>
    </div>
    <img class="qr" src="{QR_BLUE}" alt="Scan for SMARTnavigation">
  </div>
  <div class="contact-details">
    <div class="contact-row">
      <span class="contact-icon">
        <svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg" fill="currentColor">
          <path d="M2 5 l8 6 l8 -6 v10 h-16 z"/>
          <path d="M2 4 h16 l-8 6 z"/>
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
  <img src="{SGP_LOGO}" alt="SMART general practice">
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
