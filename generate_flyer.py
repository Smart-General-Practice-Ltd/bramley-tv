#!/usr/bin/env python3
"""Generate SMART Navigation conference flyer as HTML -> PDF.
Size: A5 portrait (148mm x 210mm). Strict height budget per band
so the whole flyer lands on exactly one page.

Format mirrors generate_posters.py: full-width horizontal bands,
alternating white and #1159A2 backgrounds, rounded semi-transparent
pills for stats, no column splits, no gradients.

Height budget (mm):
  top       20
  contract  30
  pricing   14
  what      18
  proof     46
  features  52
  cta       18
  footer    12
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
    font-size: 8pt;           /* body default */
    line-height: 1.4;
    font-weight: 400;
  }}

  /* Typography scale — use these classes/rules everywhere */
  .overline {{
    font-size: 7pt;
    font-weight: 800;
    letter-spacing: 2.4px;
    text-transform: uppercase;
  }}
  .body-sm {{ font-size: 7pt; line-height: 1.35; }}
  .body    {{ font-size: 8pt; line-height: 1.4; }}
  .subtitle {{ font-size: 10pt; font-weight: 700; line-height: 1.3; }}
  .heading {{ font-size: 12pt; font-weight: 800; line-height: 1.2; }}

  .band {{ overflow: hidden; }}

  /* ── Band 1: Top (white, 20mm) ───────────────────────────────────── */
  .top {{
    height: 20mm;
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6mm;
    padding: 0 8mm;
  }}
  .top img {{ height: 13mm; }}
  .top-tagline {{
    font-size: 12pt;
    font-weight: 800;
    color: #111;
    line-height: 1.2;
    border-left: 0.8mm solid #1159A2;
    padding-left: 5mm;
  }}

  /* ── Band 2: Contract hero (blue, 30mm) ──────────────────────────── */
  .contract {{
    height: 30mm;
    background: #1159A2;
    color: #fff;
    padding: 4mm 10mm;
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
    font-size: 14pt;
    font-weight: 800;
    line-height: 1.2;
  }}
  .contract-payoff {{
    font-size: 10pt;
    font-weight: 700;
    line-height: 1.3;
    margin-top: 1.5mm;
  }}

  /* ── Band 3: Pricing strip (white, 14mm) ─────────────────────────── */
  .pricing {{
    height: 14mm;
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6mm;
  }}
  .pricing-price {{
    font-size: 22pt;
    font-weight: 500;
    color: #111;
    line-height: 1;
    letter-spacing: -0.5px;
  }}
  .pricing-price .year {{ font-size: 10pt; margin-left: 0.5mm; font-weight: 400; }}
  .pricing-divider {{
    width: 0.6mm;
    height: 9mm;
    background: #111;
    opacity: 0.3;
  }}
  .pricing-offer {{
    font-size: 10pt;
    font-weight: 700;
    color: #111;
    line-height: 1.3;
  }}
  .pricing-offer em {{ font-style: italic; font-weight: 800; }}

  /* ── Band 4: What is it (white, 18mm) ────────────────────────────── */
  .what {{
    height: 18mm;
    background: #fff;
    padding: 3mm 10mm;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    border-top: 0.3mm solid #e5e5e5;
    border-bottom: 0.3mm solid #e5e5e5;
  }}
  .what h2 {{
    font-size: 12pt;
    font-weight: 800;
    color: #111;
    margin-bottom: 1.5mm;
    line-height: 1.2;
  }}
  .what p {{
    font-size: 8pt;
    line-height: 1.4;
    color: #333;
    max-width: 125mm;
    margin: 0 auto;
  }}

  /* ── Band 5: Case study (blue, 46mm) ─────────────────────────────── */
  .proof {{
    height: 46mm;
    background: #1159A2;
    color: #fff;
    padding: 4mm 6mm 4mm;
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
    line-height: 1.35;
    color: rgba(255,255,255,0.85);
    margin-bottom: 2.5mm;
  }}
  .proof-hero {{
    font-size: 28pt;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 0.8mm;
  }}
  .proof-hero-text {{
    font-size: 10pt;
    font-weight: 700;
    line-height: 1.3;
    margin-bottom: 3mm;
  }}
  .proof-pills {{
    display: flex;
    gap: 1.8mm;
    margin-top: auto;
  }}
  .pill {{
    flex: 1;
    background: rgba(255,255,255,0.16);
    border-radius: 3mm;
    padding: 2mm 1.5mm 2.2mm;
    text-align: center;
  }}
  .pill-num {{ font-size: 13pt; font-weight: 800; line-height: 1; }}
  .pill-lbl {{
    font-size: 6pt;
    color: rgba(255,255,255,0.9);
    margin-top: 0.8mm;
    line-height: 1.25;
  }}

  /* ── Band 6: Features (white, 52mm) ──────────────────────────────── */
  .features {{
    height: 52mm;
    background: #fff;
    padding: 3mm 6mm 3mm;
    display: flex;
    flex-direction: column;
  }}
  .features h2 {{
    font-size: 12pt;
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
    grid-template-rows: repeat(3, 1fr);
    gap: 1.8mm 2.2mm;
    flex: 1;
    min-height: 0;
  }}
  .feat {{
    background: #f4f7fb;
    border-left: 0.8mm solid #1159A2;
    border-radius: 1.5mm;
    padding: 1.8mm 2.4mm;
    display: flex;
    gap: 2mm;
    align-items: center;
    overflow: hidden;
  }}
  .feat-icon {{
    width: 6.5mm;
    height: 6.5mm;
    flex-shrink: 0;
  }}
  .feat-icon svg {{ width: 6.5mm; height: 6.5mm; }}
  .feat-body {{ flex: 1; min-width: 0; }}
  .feat h4 {{
    font-size: 8pt;
    font-weight: 800;
    color: #111;
    margin-bottom: 0.6mm;
    line-height: 1.15;
  }}
  .feat p {{
    font-size: 7pt;
    line-height: 1.35;
    color: #333;
  }}

  /* ── Band 7: CTA (blue, 18mm) ────────────────────────────────────── */
  .cta {{
    height: 18mm;
    background: #1159A2;
    color: #fff;
    padding: 2.5mm 6mm;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 5mm;
  }}
  .cta-text {{ flex: 1; }}
  .cta-text h3 {{
    font-size: 12pt;
    font-weight: 800;
    margin-bottom: 1mm;
    line-height: 1.2;
  }}
  .cta-text .url {{ font-size: 10pt; font-weight: 700; line-height: 1.3; }}
  .cta-text .email {{
    font-size: 8pt;
    color: rgba(255,255,255,0.9);
    margin-top: 0.8mm;
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
    width: 13mm;
    height: 13mm;
    background: #fff;
    padding: 0.5mm;
    border-radius: 0.8mm;
    display: block;
    flex-shrink: 0;
  }}

  /* ── Band 8: Footer (white, 12mm) ────────────────────────────────── */
  .footer {{
    height: 12mm;
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 6mm;
  }}
  .footer .ff {{ max-height: 9.5mm; }}
  .footer .sgp {{ max-height: 8mm; }}
</style>
</head>
<body>

<!-- Band 1: Top -->
<div class="band top">
  <img src="{SN_LOGO}" alt="SMART navigation">
  <div class="top-tagline">Contract-ready.<br>Already proven.</div>
</div>

<!-- Band 2: Contract hero -->
<div class="band contract">
  <div class="contract-label">BUILT AROUND THE 2026/27 GP CONTRACT</div>
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
  <p>GP-designed, condition-specific triage for your reception team. Replaces duty-doctor pressure with a safe, auditable same-day pathway &mdash; reducing admin and directing every patient to the right care first time.</p>
</div>

<!-- Band 5: Case study proof -->
<div class="band proof">
  <div class="proof-label">12-MONTH CASE STUDY</div>
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

<!-- Band 6: Features -->
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
        <p>Same-day condition-specific questions book patients into same-day slots.</p>
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

    <div class="feat">
      <div class="feat-icon">
        <svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
          <path d="M8 16 A13 13 0 0 1 31 11" fill="none" stroke="#1159A2" stroke-width="2.4" stroke-linecap="round"/>
          <polygon points="33,13 29,5 24,11" fill="#1159A2"/>
          <path d="M32 24 A13 13 0 0 1 9 29" fill="none" stroke="#1159A2" stroke-width="2.4" stroke-linecap="round"/>
          <polygon points="7,27 11,35 16,29" fill="#1159A2"/>
          <circle cx="20" cy="20" r="6" fill="#1159A2"/>
          <polygon points="18,16.7 24,20 18,23.3" fill="#fff"/>
        </svg>
      </div>
      <div class="feat-body">
        <h4>EMIS Write-Back</h4>
        <p>Automatic write-back &mdash; no PDFs, no manual steps.</p>
      </div>
    </div>

    <div class="feat">
      <div class="feat-icon">
        <svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
          <rect x="17" y="5" width="6" height="16" rx="3" fill="#1159A2"/>
          <path d="M11 19 a9 9 0 0 0 18 0" fill="none" stroke="#1159A2" stroke-width="2.4" stroke-linecap="round"/>
          <line x1="20" y1="28" x2="20" y2="33" stroke="#1159A2" stroke-width="2.4" stroke-linecap="round"/>
          <line x1="14" y1="35" x2="26" y2="35" stroke="#1159A2" stroke-width="2.4" stroke-linecap="round"/>
        </svg>
      </div>
      <div class="feat-body">
        <h4>Ambient Voice Technology</h4>
        <p>Trialling in a Leeds practice: ambient voice answering calls on SMARTnav scripts.</p>
      </div>
    </div>
  </div>
</div>

<!-- Band 7: CTA -->
<div class="band cta">
  <div class="cta-text">
    <h3>Book a demo today</h3>
    <div class="url">smartnavigation.co.uk</div>
    <div class="email">enquiries@smartgeneralpractice.com</div>
  </div>
  <div class="cta-qr">
    <div class="cta-qr-label">Scan to<br>book a demo</div>
    <img src="{QR_WHITE}" alt="Scan to book a demo">
  </div>
</div>

<!-- Band 8: Footer -->
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
