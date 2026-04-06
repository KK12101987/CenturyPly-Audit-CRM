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

    def draw_header_and_watermark(canvas_obj, page_num):
        # Optional: Logo
        logo = BASE / "static" / "logo.png"
        if logo.exists():
            try:
                img = ImageReader(str(logo))
                canvas_obj.saveState()
                canvas_obj.drawImage(img, 40, h-160, width=180, height=70, mask='auto')
                canvas_obj.restoreState()
            except Exception:
                pass

        # Watermark Background (Fixed)
        canvas_obj.saveState()
        canvas_obj.translate(300, 400)
        canvas_obj.rotate(45)
        canvas_obj.setFillAlpha(0.15)
        canvas_obj.setFillColorRGB(0.5, 0.5, 0.5)
        canvas_obj.setFont("Helvetica-Bold", 60)
        canvas_obj.drawCentredString(0, 0, "CENTURYPLY QA 2025")
        canvas_obj.restoreState()

        # Header
        canvas_obj.setFillColorRGB(0.69, 0.07, 0.09)
        canvas_obj.setFont("Helvetica-Bold", 18)
        canvas_obj.drawString(40, h-80, "CENTURYPLY QA AUDIT REPORT")

        canvas_obj.setFont("Helvetica", 11)
        canvas_obj.drawString(40, h-100, "Version: v4.2 Ultimate Build — 2025")
        canvas_obj.drawString(40, h-115, f"Auditor: {auditor_name}")
        canvas_obj.drawString(40, h-130, f"Generated On: {datetime.date.today().isoformat()}")
        
        # Footer for current page
        canvas_obj.setFont("Helvetica", 9)
        canvas_obj.drawString(40, 30, "© 2025 CenturyPly Corporate QA")
        canvas_obj.drawRightString(w-40, 30, f"Page {page_num}")

    # Draw first page header
    page_number = 1
    draw_header_and_watermark(c, page_number)
    
    # Content Start Y-coordinate
    y = h - 170
    c.setFont("Helvetica", 10)

    if df.empty:
        c.drawString(40, y, "No data available in database.")
    else:
        # Removed the .head(12) limit to process all rows dynamically
        for _, row in df.iterrows():
            text = (
                f"RM: {row.get('name','')} | %: {row.get('percent',0)} | "
                f"Obs: {str(row.get('audit_observation',''))[:40]}"
            )
            c.drawString(40, y, text)
            y -= 14
            
            # Pagination logic: Create new page when reaching the bottom margin
            if y < 60:
                c.showPage()
                page_number += 1
                draw_header_and_watermark(c, page_number)
                y = h - 170
                c.setFont("Helvetica", 10)

    c.save()
