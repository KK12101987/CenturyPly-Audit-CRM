from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from pathlib import Path
import datetime

def generate_full_pdf(df, out_path, auditor_name="Unknown Auditor"):
    out_path = Path(out_path)
    c = canvas.Canvas(str(out_path), pagesize=A4)
    w, h = A4

    BASE = Path(__file__).parent

    # Optional: Logo
    logo = BASE / "static" / "logo.png"
    if logo.exists():
        try:
            img = ImageReader(str(logo))
            c.saveState()
            c.drawImage(img, 40, h-160, width=180, height=70, mask='auto')
            c.restoreState()
        except Exception:
            pass

    # Watermark Background
    c.saveState()
    c.setFont("Helvetica-Bold", 60)
    c.setFillGray(0.9)
    c.translate(300, 400)
    c.rotate(45)
    try:
        c.setFillAlpha(0.09)
    except:
        pass
    c.drawCentredString(0, 0, "CENTURYPLY QA 2025")
    c.restoreState()

    # Header
    c.setFillColorRGB(0.69, 0.07, 0.09)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40, h-80, "CENTURYPLY QA AUDIT REPORT")

    c.setFont("Helvetica", 11)
    c.drawString(40, h-100, "Version: v4.2 Ultimate Build — 2025")
    c.drawString(40, h-115, f"Auditor: {auditor_name}")
    c.drawString(40, h-130,
                 f"Generated On: {datetime.date.today().isoformat()}")

    # Content
    y = h - 170
    c.setFont("Helvetica", 10)

    if df.empty:
        c.drawString(40, y, "No data available in database.")
    else:
        for _, row in df.head(12).iterrows():
            text = (
                f"RM: {row.get('name','')} | %: {row.get('percent',0)} | "
                f"Obs: {str(row.get('audit_observation',''))[:40]}"
            )
            c.drawString(40, y, text)
            y -= 14
            if y < 60:
                c.showPage()
                y = h - 100

    # Footer
    c.showPage()
    c.setFont("Helvetica", 9)
    c.drawString(40, 30, "© 2025 CenturyPly Corporate QA")
    c.drawRightString(w-40, 30, "Page 1")
    c.save()
