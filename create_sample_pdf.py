from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def make_pdf():
    pdf_path = "sample.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=16, leading=20, textColor="#003366")
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=12, leading=16, textColor="#005580", spaceBefore=10)
    body_style = ParagraphStyle('Body', parent=styles['BodyText'], fontSize=10, leading=14, spaceAfter=8)

    story = [
        Paragraph("MoSPI Training Module: Fundamentals of Statistical Data Collection", title_style),
        Spacer(1, 10),
        Paragraph("1. Sampling Techniques and Frameworks", heading_style),
        Paragraph("In large-scale national surveys managed by MoSPI, Simple Random Sampling (SRS) ensures every unit in the population has an equal non-zero probability of selection. Stratified Random Sampling is preferred when target populations exhibit heterogeneous sub-groups (e.g., rural vs. urban) to improve national estimation precision.", body_style),
        Paragraph("2. Primary Data Validation & Range Checks", heading_style),
        Paragraph("Primary data collected by field officers must undergo double-entry verification and automated range checks to prevent outliers caused by typographical mistakes. Missing value imputations follow international statistical protocols like hot-deck imputation.", body_style),
        Paragraph("3. Consumer Price Index (CPI) Benchmark", heading_style),
        Paragraph("The Consumer Price Index (CPI) measures temporal changes in the general price level of goods and services consumed by households. The base year serves as a benchmark (standardized at an index value of 100).", body_style)
    ]

    doc.build(story)
    print(f"Success! '{pdf_path}' has been created.")

if __name__ == "__main__":
    make_pdf()
