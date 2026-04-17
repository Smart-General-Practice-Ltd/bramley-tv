#!/usr/bin/env python3
"""Generate SMART Navigation conference flyer as HTML -> PDF.
Size: A5 portrait (148mm x 210mm).

Cleaner, less busy version: cut "What is it?", cut the top tagline,
cut 2 features. Leaves more air, bigger logos, cleaner hierarchy.

Height budget (mm):
  top       16
  contract  30
  pricing   14
  what      30
  proof     42
  features  42
  cta       14
  footer    22
  ----------
  total    210
"""
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
SGP_LOGO = img_to_data_uri(os.path.join(LOGO_DIR, "smart-general-practice-logo.png"))
QR_WHITE = make_qr('https://smartnavigation.co.uk', fill='white', back='#1159A2')

FLYER_HTML = f"""<!DOCTYPE html>
<html>
<head>
<style>
  @page {{ size: 148mm 210mm; margin: 0; }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: 148mm; height: 210mm; }}
  body {{
    font-family: Helvetica, Arial, sans-serif;
    color: #111;
    overflow: hidden;
    font-size: 8pt;
    line-height: 1.4;
    font-weight: 400;
  }}

  /* Typography scale */
  .overline {{
    font-size: 7pt;
    font-weight: 800;
    letter-spacing: 2.4px;
    text-transform: uppercase;
  }}

  .band {{ overflow: hidden; }}

  /* ── Band 1: Top (white, 16mm) ───────────────────────────────────── */
  .top {{
    height: 16mm;
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 8mm;
  }}
  .top img {{ height: 12mm; }}

  /* ── Band 2: Contract hero (blue, 30mm) ──────────────────────────── */
  .contract {{
    height: 30mm;
    background: #1159A2;
    color: #fff;
    padding: 3.5mm 10mm;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 2mm;
  }}
  .contract-label {{
    font-size: 7pt;
    font-weight: 800;
    letter-spacing: 2.4px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.7);
  }}
  .contract-quote {{
    font-size: 13pt;
    font-weight: 800;
    line-height: 1.2;
  }}
  .contract-payoff {{
    font-size: 10pt;
    font-weight: 700;
    line-height: 1.3;
  }}

  /* ── Band 3: Pricing (white, 14mm) ───────────────────────────────── */
  .pricing {{
    height: 14mm;
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 7mm;
  }}
  .pricing-price {{
    font-size: 24pt;
    font-weight: 500;
    color: #111;
    line-height: 1;
    letter-spacing: -0.5px;
  }}
  .pricing-price .year {{ font-size: 10pt; margin-left: 0.5mm; font-weight: 400; }}
  .pricing-divider {{
    width: 0.6mm;
    height: 10mm;
    background: #111;
    opacity: 0.3;
  }}
  .pricing-offer {{
    font-size: 11pt;
    font-weight: 700;
    color: #111;
    line-height: 1.3;
  }}
  .pricing-offer em {{ font-style: italic; font-weight: 800; }}

  /* ── Band 4: What is it (white, 30mm) ────────────────────────────── */
  .what {{
    height: 30mm;
    background: #fff;
    padding: 2mm 10mm;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    border-top: 0.3mm solid #e5e5e5;
    border-bottom: 0.3mm solid #e5e5e5;
  }}
  .what h2 {{
    font-size: 11pt;
    font-weight: 800;
    color: #111;
    margin-bottom: 1.5mm;
    line-height: 1.2;
  }}
  .what p {{
    font-size: 6.8pt;
    line-height: 1.35;
    color: #333;
    max-width: 128mm;
    margin: 0 auto;
  }}
  .what p + p {{ margin-top: 1.3mm; }}

  /* ── Band 5: Case study (blue, 42mm) ─────────────────────────────── */
  .proof {{
    height: 42mm;
    background: #1159A2;
    color: #fff;
    padding: 5mm 7mm 5mm;
    text-align: center;
    display: flex;
    flex-direction: column;
  }}
  .proof-label {{
    font-size: 7pt;
    font-weight: 800;
    letter-spacing: 2.4px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.7);
    margin-bottom: 1mm;
  }}
  .proof-sub {{
    font-size: 7pt;
    line-height: 1.3;
    color: rgba(255,255,255,0.85);
    margin-bottom: 2mm;
  }}
  .proof-hero {{
    font-size: 24pt;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 0.5mm;
  }}
  .proof-hero-text {{
    font-size: 9pt;
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 2mm;
  }}
  .proof-pills {{
    display: flex;
    gap: 1.8mm;
    margin-top: auto;
  }}
  .pill {{
    flex: 1;
    background: rgba(255,255,255,0.16);
    border-radius: 2.5mm;
    padding: 1.8mm 1.3mm 2mm;
    text-align: center;
  }}
  .pill-num {{ font-size: 12pt; font-weight: 800; line-height: 1; }}
  .pill-lbl {{
    font-size: 5.8pt;
    color: rgba(255,255,255,0.9);
    margin-top: 0.7mm;
    line-height: 1.2;
  }}

  /* ── Band 6: Features (white, 42mm) — 2x2 grid ───────────────────── */
  .features {{
    height: 42mm;
    background: #fff;
    padding: 3mm 7mm 3mm;
    display: flex;
    flex-direction: column;
  }}
  .features h2 {{
    font-size: 11pt;
    font-weight: 800;
    color: #111;
    text-align: center;
    margin-bottom: 2.5mm;
    line-height: 1.2;
    flex: 0 0 auto;
  }}
  .feat-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 1.8mm 2.5mm;
    flex: 1;
    min-height: 0;
  }}
  .feat {{
    background: #f4f7fb;
    border-left: 0.8mm solid #1159A2;
    border-radius: 1.5mm;
    padding: 2mm 2.5mm;
    display: flex;
    gap: 2mm;
    align-items: center;
    overflow: hidden;
  }}
  .feat-icon {{
    width: 8mm;
    height: 8mm;
    flex-shrink: 0;
  }}
  .feat-icon svg {{ width: 8mm; height: 8mm; }}
  .feat-body {{ flex: 1; min-width: 0; }}
  .feat h4 {{
    font-size: 8.5pt;
    font-weight: 800;
    color: #111;
    margin-bottom: 0.6mm;
    line-height: 1.15;
  }}
  .feat p {{
    font-size: 6.8pt;
    line-height: 1.3;
    color: #333;
  }}

  /* ── Band 7: CTA (blue, 14mm) ────────────────────────────────────── */
  .cta {{
    height: 14mm;
    background: #1159A2;
    color: #fff;
    padding: 2mm 7mm;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 5mm;
  }}
  .cta-text {{ flex: 1; }}
  .cta-text .url {{ font-size: 12pt; font-weight: 800; line-height: 1.2; }}
  .cta-text .email {{
    font-size: 9pt;
    color: rgba(255,255,255,0.9);
    margin-top: 0.6mm;
    line-height: 1.2;
  }}
  .cta-qr {{
    flex: 0 0 auto;
    display: flex;
    align-items: center;
    gap: 2.5mm;
  }}
  .cta-qr-label {{
    font-size: 8pt;
    font-weight: 700;
    color: #fff;
    text-align: right;
    line-height: 1.25;
    max-width: 22mm;
  }}
  .cta-qr img {{
    width: 10mm;
    height: 10mm;
    background: #fff;
    padding: 0.4mm;
    border-radius: 0.8mm;
    display: block;
    flex-shrink: 0;
  }}

  /* ── Band 8: Footer (white, 22mm) — bigger F&F ──────────────────── */
  .footer {{
    height: 22mm;
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 8mm;
  }}
  .footer .ff {{ max-height: 18mm; }}
  .footer .sgp {{ max-height: 14mm; }}
</style>
</head>
<body>

<!-- Band 1: Top -->
<div class="band top">
  <img src="{SN_LOGO}" alt="SMART navigation">
</div>

<!-- Band 2: Contract hero -->
<div class="band contract">
  <div class="contract-label">Built around the 2026/27 GP Contract</div>
  <div class="contract-quote">&ldquo;Clinically urgent requests must be dealt with on the same day.&rdquo;</div>
  <div class="contract-payoff">SMARTnavigation is how EMIS practices deliver it.</div>
</div>

<!-- Band 3: Pricing -->
<div class="band pricing">
  <div class="pricing-price">&pound;1,000<span class="year">/year</span></div>
  <div class="pricing-divider"></div>
  <div class="pricing-offer">3 months <em>free</em> &ndash; Conference Offer</div>
</div>

<!-- Band 4: What is it -->
<div class="band what">
  <h2>What is it?</h2>
  <p>For years, practices have relied on a duty doctor to handle same day demand &mdash; a model that&rsquo;s no longer sustainable. Receptionists are the first point of contact but are left making clinical decisions without enough support. SMARTnavigation fixes this.</p>
  <p>SMARTnavigation guides patients through GP-designed, condition-specific pathways and supports automatic write-back into the clinical record. This reduces admin, improves triage accuracy, and helps practices manage demand more safely and efficiently.</p>
</div>

<!-- Band 5: Case study proof -->
<div class="band proof">
  <div class="proof-label">12-Month Case Study</div>
  <div class="proof-sub">April 2024 &ndash; March 2025 &bull; 17 practices &bull; 152,508 patients triaged</div>
  <div class="proof-hero">47%</div>
  <div class="proof-hero-text">of patients safely redirected away from the GP</div>
  <div class="proof-pills">
    <div class="pill"><div class="pill-num">15%</div><div class="pill-lbl">eConsultations</div></div>
    <div class="pill"><div class="pill-num">12%</div><div class="pill-lbl">Community<br>Pharmacy</div></div>
    <div class="pill"><div class="pill-num">11%</div><div class="pill-lbl">Other clinicians<br>(Nurse, HCA)</div></div>
    <div class="pill"><div class="pill-num">9%</div><div class="pill-lbl">A&amp;E / WIC</div></div>
  </div>
</div>

<!-- Band 5: Features (2x2) -->
<div class="band features">
  <h2>How it works</h2>
  <div class="feat-grid">
    <div class="feat">
      <div class="feat-icon">
        <svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
          <circle cx="19" cy="22" r="13" fill="none" stroke="#1159A2" stroke-width="2.4"/>
          <text x="19" y="26" text-anchor="middle" font-family="Helvetica" font-weight="700" font-size="9" fill="#1159A2">AGE</text>
          <circle cx="32" cy="10" r="5.5" fill="#1159A2"/>
          <path d="M32 7.2v5.6 M29.2 10h5.6" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/>
        </svg>
      </div>
      <div class="feat-body">
        <h4>Age Triage</h4>
        <p>Scripts adapt questions to the patient&rsquo;s age.</p>
      </div>
    </div>

    <div class="feat">
      <div class="feat-icon">
        <svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
          <path d="M20 5 L36 33 L4 33 Z" fill="none" stroke="#1159A2" stroke-width="2.4" stroke-linejoin="round"/>
          <rect x="18.5" y="15" width="3" height="9" fill="#1159A2" rx="1"/>
          <rect x="18.5" y="26" width="3" height="3" fill="#1159A2" rx="0.7"/>
        </svg>
      </div>
      <div class="feat-body">
        <h4>Red Flag Screening</h4>
        <p>Condition-specific red flags guide patients away from Primary Care.</p>
      </div>
    </div>

    <div class="feat">
      <div class="feat-icon">
        <svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
          <circle cx="23" cy="23" r="11" fill="none" stroke="#1159A2" stroke-width="2.4"/>
          <path d="M23 23 L23 16 M23 23 L28.5 23" stroke="#1159A2" stroke-width="2.4" stroke-linecap="round"/>
          <rect x="20" y="8" width="6" height="2" rx="0.6" fill="#1159A2"/>
          <rect x="22" y="6" width="2" height="3" rx="0.4" fill="#1159A2"/>
          <path d="M4 22 L10 21 M3 27 L11 26 M4 31 L9 30" stroke="#1159A2" stroke-width="1.8" stroke-linecap="round"/>
        </svg>
      </div>
      <div class="feat-body">
        <h4>Same Day Triage</h4>
        <p>Books patients into same-day slots using condition-specific questions.</p>
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
        <p>Filters patients into bookable pharmacist slots to prevent looping.</p>
      </div>
    </div>
  </div>
</div>

<!-- Band 7: CTA -->
<div class="band cta">
  <div class="cta-text">
    <div class="url">smartnavigation.co.uk</div>
    <div class="email">enquiries@smartgeneralpractice.com</div>
  </div>
  <div class="cta-qr">
    <div class="cta-qr-label">Scan to<br>book a demo</div>
    <img src="{QR_WHITE}" alt="Scan to book a demo">
  </div>
</div>

<!-- Band 7: Footer -->
<div class="band footer">
  <img class="ff" src="{FF_LOGO}" alt="Fuller and Forbes Healthcare Group">
  <img class="sgp" src="{SGP_LOGO}" alt="SMART general practice">
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
