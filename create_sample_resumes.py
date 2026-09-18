from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_resume_pdf(filename, name, title, skills, experience, education):
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    story = []

    # Title & Header
    story.append(Paragraph(f"<b><font size=16 color='#2c3e50'>{name}</font></b>", styles['Title']))
    story.append(Paragraph(f"<b><font size=11 color='#7f8c8d'>{title}</font></b>", styles['Normal']))
    story.append(Spacer(1, 10))

    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, leading=14)

    # Technical Skills Section
    story.append(Paragraph("<b>TECHNICAL SKILLS</b>", styles['Heading2']))
    story.append(Paragraph(skills, body_style))
    story.append(Spacer(1, 10))

    # Experience Section
    story.append(Paragraph("<b>PROFESSIONAL EXPERIENCE</b>", styles['Heading2']))
    for exp in experience:
        story.append(Paragraph(f"• {exp}", body_style))
        story.append(Spacer(1, 4))
    story.append(Spacer(1, 10))

    # Education Section
    story.append(Paragraph("<b>EDUCATION</b>", styles['Heading2']))
    story.append(Paragraph(education, body_style))

    doc.build(story)

# 1. AI & Machine Learning Sample Resume
create_resume_pdf(
    filename="resume_ai.pdf",
    name="Alex Mercer",
    title="AI & Machine Learning Engineer",
    skills="<b>Core Competencies:</b> Python, PyTorch, TensorFlow, FastAPI, Natural Language Processing, Large Language Models (LLMs), Computer Vision, Git, Docker.",
    experience=[
        "<b>ML Engineer @ TechCorp:</b> Developed and deployed Transformer-based NLP pipelines using FastAPI and Groq API.",
        "<b>AI Research Intern:</b> Trained convolutional neural networks (CNNs) and benchmarked supervised learning classification models.",
        "<b>Projects:</b> Built a PDF Quiz Generator utilizing PyPDF, LangChain, and RESTful API endpoints."
    ],
    education="B.S. in Computer Science & Artificial Intelligence, Geeta University (2026)"
)

# 2. Science & Biology Sample Resume
create_resume_pdf(
    filename="resume_science.pdf",
    name="Dr. Elena Rostova",
    title="Biotechnology & Molecular Biology Researcher",
    skills="<b>Core Competencies:</b> Cellular Biology, Genetics, DNA Sequencing, Biochemistry, Photosynthesis Analysis, Laboratory Protocol Design.",
    experience=[
        "<b>Research Associate @ BioGen Labs:</b> Conducted DNA extraction and RNA sequencing for cell culture growth analysis.",
        "<b>Lab Technician:</b> Evaluated cellular bioenergetics and ATP synthesis pathways in eukaryotic cell structures.",
        "<b>Publications:</b> Co-authored papers on photosynthetic electron transport and enzymatic catalysis."
    ],
    education="M.S. in Biological Sciences, Stanford University"
)

# 3. World History & Humanities Sample Resume
create_resume_pdf(
    filename="resume_history.pdf",
    name="Marcus Vance",
    title="Historian & Archival Researcher",
    skills="<b>Core Competencies:</b> World History Analysis, Archival Documentation, Industrialization Economics, Modern Geopolitics, Historiography.",
    experience=[
        "<b>Archival Assistant @ National History Museum:</b> Cataloged primary historical source documents from the Industrial Revolution.",
        "<b>Historical Researcher:</b> Conducted qualitative studies on World War I military alliances and 20th-century diplomatic history.",
        "<b>Lecturer Assistant:</b> Led university seminars on post-WWII geopolitical structures and international relations."
    ],
    education="B.A. in History & Political Science, University of Oxford"
)

print("Sample resumes created: resume_ai.pdf, resume_science.pdf, resume_history.pdf")
