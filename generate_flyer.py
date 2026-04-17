#!/usr/bin/env python3
"""Generate SMART Navigation conference flyer as HTML -> PDF.
Size: A5 portrait (148mm x 210mm). Strict height budget per band
so the whole flyer lands on exactly one page.

Format mirrors generate_posters.py: full-width horizontal bands,
alternating white and #1159A2 backgrounds, rounded semi-transparent
pills for stats, no column splits, no gradients.

Height budget (mm):
  top       18
  contract  36
  pricing   14
  what      22
  proof     40
  features  50
  cta       22
  footer     8
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
QR_WHITE = make_qr('https://smartnavigation.co.uk', fill='white', back='#1159A2')

FLYER_HTML = f"""<!DOCTYPE html>
<html>
<head>
<style>
  @page {{ size: 148mm 210mm; margin: 0; }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: 148mm; height: 210mm; }}
  body {{ font-family: Helvetica, Arial, sans-serif; color: #222; overflow: hidden; }}

  .band {{ overflow: hidden; }}

  /* ── Band 1: Top (white, 18mm) ───────────────────────────────────── */
  .top {{
    height: 18mm;
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5mm;
    padding: 0 8mm;
  }}
  .top img {{ height: 11mm; }}
  .top-tagline {{
    font-size: 10pt;
    font-weight: 800;
    color: #1159A2;
    line-height: 1.1;
    border-left: 0.4mm solid #1159A2;
    padding-left: 4mm;
  }}

  /* ── Band 2: Contract hero (blue, 36mm) ──────────────────────────── */
  .contract {{
    height: 36mm;
    background: #1159A2;
    color: #fff;
    padding: 4mm 8mm;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  .contract-label {{
    font-size: 6.8pt;
    font-weight: 800;
    letter-spacing: 2.6px;
    color: rgba(255,255,255,0.65);
    margin-bottom: 2.5mm;
  }}
  .contract-quote {{
    font-size: 12.5pt;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 2mm;
  }}
  .contract-attrib {{
    font-size: 6.8pt;
    font-style: italic;
    color: rgba(255,255,255,0.7);
    margin-bottom: 3mm;
  }}
  .contract-payoff {{
    font-size: 9.5pt;
    font-weight: 700;
    line-height: 1.2;
  }}

  /* ── Band 3: Pricing strip (white, 14mm) ─────────────────────────── */
  .pricing {{
    height: 14mm;
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5mm;
    border-bottom: 0.3mm solid #e5e5e5;
  }}
  .pricing-price {{
    font-size: 22pt;
    font-weight: 300;
    color: #1159A2;
    line-height: 1;
    letter-spacing: -0.5px;
  }}
  .pricing-price .year {{ font-size: 9pt; margin-left: 0.5mm; }}
  .pricing-divider {{
    width: 0.3mm;
    height: 8mm;
    background: #1159A2;
    opacity: 0.3;
  }}
  .pricing-offer {{
    font-size: 9pt;
    font-weight: 700;
    color: #1159A2;
    line-height: 1.2;
  }}
  .pricing-offer em {{ font-style: italic; font-weight: 800; }}

  /* ── Band 4: What is it (white, 22mm) ────────────────────────────── */
  .what {{
    height: 22mm;
    background: #fff;
    padding: 3mm 10mm 3mm;
    text-align: center;
  }}
  .what h2 {{
    font-size: 11pt;
    font-weight: 800;
    color: #1159A2;
    margin-bottom: 1.5mm;
  }}
  .what p {{
    font-size: 7.2pt;
    line-height: 1.35;
    color: #333;
    max-width: 125mm;
    margin: 0 auto;
  }}

  /* ── Band 5: Case study (blue, 40mm) ─────────────────────────────── */
  .proof {{
    height: 40mm;
    background: #1159A2;
    color: #fff;
    padding: 3.5mm 6mm 4mm;
    text-align: center;
    display: flex;
    flex-direction: column;
  }}
  .proof-label {{
    font-size: 6.5pt;
    font-weight: 800;
    letter-spacing: 2.4px;
    color: rgba(255,255,255,0.65);
    margin-bottom: 1mm;
  }}
  .proof-sub {{
    font-size: 7pt;
    color: rgba(255,255,255,0.8);
    margin-bottom: 2mm;
  }}
  .proof-hero {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 3mm;
    margin-bottom: 2.5mm;
  }}
  .proof-hero-num {{
    font-size: 30pt;
    font-weight: 800;
    line-height: 0.9;
  }}
  .proof-hero-text {{
    font-size: 8.5pt;
    font-weight: 700;
    text-align: left;
    line-height: 1.2;
    max-width: 52mm;
  }}
  .proof-pills {{
    display: flex;
    gap: 1.5mm;
    margin-top: auto;
  }}
  .pill {{
    flex: 1;
    background: rgba(255,255,255,0.14);
    border-radius: 2mm;
    padding: 2mm 1mm;
    text-align: center;
  }}
  .pill-num {{ font-size: 11pt; font-weight: 800; line-height: 1; }}
  .pill-lbl {{
    font-size: 5.6pt;
    color: rgba(255,255,255,0.85);
    margin-top: 0.8mm;
    line-height: 1.15;
  }}

  /* ── Band 6: Features (white, 50mm) ──────────────────────────────── */
  .features {{
    height: 50mm;
    background: #fff;
    padding: 3mm 6mm 3mm;
  }}
  .features h2 {{
    font-size: 10pt;
    font-weight: 800;
    color: #1159A2;
    text-align: center;
    margin-bottom: 2.5mm;
  }}
  .feat-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr 1fr;
    gap: 1.8mm 2mm;
  }}
  .feat {{
    background: #f4f7fb;
    border-left: 0.7mm solid #1159A2;
    border-radius: 1.2mm;
    padding: 1.8mm 2.2mm;
    display: flex;
    gap: 2mm;
    align-items: flex-start;
  }}
  .feat-icon {{
    width: 6mm;
    height: 6mm;
    flex-shrink: 0;
    margin-top: 0.2mm;
  }}
  .feat-icon svg {{ width: 6mm; height: 6mm; }}
  .feat h4 {{
    font-size: 7.2pt;
    font-weight: 800;
    color: #1159A2;
    margin-bottom: 0.4mm;
    line-height: 1.1;
  }}
  .feat p {{
    font-size: 5.8pt;
    line-height: 1.25;
    color: #333;
  }}

  /* ── Band 7: CTA (blue, 22mm) ────────────────────────────────────── */
  .cta {{
    height: 22mm;
    background: #1159A2;
    color: #fff;
    padding: 3mm 6mm;
    display: flex;
    align-items: center;
    gap: 5mm;
  }}
  .cta-qr {{ flex: 0 0 auto; text-align: center; }}
  .cta-qr img {{
    width: 15mm;
    height: 15mm;
    background: #fff;
    padding: 0.5mm;
    border-radius: 0.8mm;
    display: block;
  }}
  .cta-qr-label {{
    font-size: 5.4pt;
    color: rgba(255,255,255,0.8);
    margin-top: 0.6mm;
  }}
  .cta-text {{ flex: 1; }}
  .cta-text h3 {{
    font-size: 11pt;
    font-weight: 800;
    margin-bottom: 1mm;
    line-height: 1.1;
  }}
  .cta-text .url {{ font-size: 9pt; font-weight: 700; line-height: 1.2; }}
  .cta-text .email {{
    font-size: 7.4pt;
    color: rgba(255,255,255,0.85);
    margin-top: 0.8mm;
  }}

  /* ── Band 8: Footer (white, 8mm) ─────────────────────────────────── */
  .footer {{
    height: 8mm;
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 6mm;
  }}
  .footer .ff {{ max-height: 5.5mm; }}
  .sgp-logo {{ display: flex; align-items: center; gap: 1.3mm; }}
  .sgp-circle {{
    width: 5mm;
    height: 5mm;
    border-radius: 50%;
    background: #1159A2;
    color: #fff;
    font-size: 4pt;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .sgp-text {{ font-size: 8pt; color: #1159A2; line-height: 1; }}
  .sgp-tm {{
    font-size: 3.5pt;
    vertical-align: super;
    margin-left: 0.3mm;
    font-weight: 600;
  }}
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
  <div class="contract-attrib">NHS England, GP Contract 2026/27</div>
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
  <div class="proof-hero">
    <div class="proof-hero-num">47%</div>
    <div class="proof-hero-text">of patients safely redirected away from the GP</div>
  </div>
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
      <div>
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
      <div>
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
      <div>
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
      <div>
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
      <div>
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
      <div>
        <h4>Ambient Voice Technology</h4>
        <p>Trialling in a Leeds practice: ambient voice answering calls on SMARTnav scripts.</p>
      </div>
    </div>
  </div>
</div>

<!-- Band 7: CTA -->
<div class="band cta">
  <div class="cta-qr">
    <img src="{QR_WHITE}" alt="Scan to book a demo">
    <div class="cta-qr-label">Scan to book a demo</div>
  </div>
  <div class="cta-text">
    <h3>Book a demo today</h3>
    <div class="url">smartnavigation.co.uk</div>
    <div class="email">enquiries@smartgeneralpractice.com</div>
  </div>
</div>

<!-- Band 8: Footer -->
<div class="band footer">
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
