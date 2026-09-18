from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def create_professional_cv(filename, name, contact, summary, skills, experience, education, projects):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    styles = getSampleStyleSheet()
    story = []

    # Header Styles
    name_style = ParagraphStyle('CVName', fontName='Helvetica-Bold', fontSize=20, leading=22, textColor=colors.HexColor('#1A252C'))
    contact_style = ParagraphStyle('CVContact', fontName='Helvetica', fontSize=9, leading=12, textColor=colors.HexColor('#555555'))
    section_heading = ParagraphStyle('CVSection', fontName='Helvetica-Bold', fontSize=12, leading=14, textColor=colors.HexColor('#2C3E50'), spaceAfter=4)
    body_style = ParagraphStyle('CVBody', fontName='Helvetica', fontSize=9.5, leading=13, textColor=colors.HexColor('#333333'))
    title_style = ParagraphStyle('CVTitle', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=colors.HexColor('#2C3E50'))

    # Name & Contact Header
    story.append(Paragraph(name, name_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(contact, contact_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#3498DB'), spaceAfter=12))

    # Professional Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_heading))
    story.append(Paragraph(summary, body_style))
    story.append(Spacer(1, 10))

    # Technical Skills
    story.append(Paragraph("TECHNICAL SKILLS", section_heading))
    story.append(Paragraph(skills, body_style))
    story.append(Spacer(1, 10))

    # Work Experience
    story.append(Paragraph("WORK EXPERIENCE", section_heading))
    for exp in experience:
        story.append(Paragraph(f"<b>{exp['role']}</b> | <i>{exp['company']}</i> <font color='#777'>({exp['dates']})</font>", title_style))
        for bullet in exp['bullets']:
            story.append(Paragraph(f"• {bullet}", body_style))
        story.append(Spacer(1, 6))
    story.append(Spacer(1, 4))

    # Key Projects
    if projects:
        story.append(Paragraph("PROJECTS", section_heading))
        for proj in projects:
            story.append(Paragraph(f"<b>{proj['name']}</b>", title_style))
            story.append(Paragraph(f"• {proj['desc']}", body_style))
            story.append(Spacer(1, 4))
        story.append(Spacer(1, 6))

    # Education
    story.append(Paragraph("EDUCATION", section_heading))
    story.append(Paragraph(education, body_style))

    doc.build(story)

# 1. Real AI / ML Developer Resume
create_professional_cv(
    filename="resume_ai.pdf",
    name="Alex Mercer",
    contact="San Francisco, CA | alex.mercer@email.com | github.com/alexmercer-ai | linkedin.com/in/alexmercer",
    summary="Results-driven Machine Learning Engineer with 3+ years of experience designing, training, and deploying end-to-end Deep Learning and LLM systems. Proficient in PyTorch, FastAPI, and cloud AI infrastructure.",
    skills="<b>Languages & Frameworks:</b> Python, C++, PyTorch, TensorFlow, FastAPI, LangChain, Hugging Face.<br/><b>Tools & Infrastructure:</b> Docker, Git, AWS S3/EC2, PostgreSQL, WSL Ubuntu, REST APIs.",
    experience=[
        {
            "role": "Machine Learning Engineer",
            "company": "Apex AI Innovations",
            "dates": "2024 - Present",
            "bullets": [
                "Fine-tuned Llama-3 70B models using QLoRA for domain-specific NLP tasks, improving generation accuracy by 24%.",
                "Built asynchronous FastAPI microservices serving model inference to 50k daily active users."
            ]
        },
        {
            "role": "AI Research Intern",
            "company": "DataVision Labs",
            "dates": "2023 - 2024",
            "bullets": [
                "Implemented computer vision classification pipelines using PyTorch and OpenCV.",
                "Optimized PyPDF text extraction workflows for resume-driven evaluation benchmarks."
            ]
        }
    ],
    projects=[
        {
            "name": "Automated PDF Assessment Generator",
            "desc": "Built a full-stack platform using FastAPI, Groq LLM API, and Netlify to extract PDF text and dynamically generate timed 20-question quizzes."
        }
    ],
    education="<b>Bachelor of Technology in Computer Science & AI</b> — Geeta University (2022 - 2026)"
)

# 2. Real Science / Biotechnology Resume
create_professional_cv(
    filename="resume_science.pdf",
    name="Dr. Elena Rostova",
    contact="Boston, MA | e.rostova@biotechlab.org | linkedin.com/in/elenarostova",
    summary="Detail-oriented Molecular Biologist with extensive experience in cellular bioenergetics, genetics research, and protocol validation for clinical diagnostics.",
    skills="<b>Laboratory Skills:</b> PCR, DNA/RNA Extraction, Next-Gen Sequencing, Cell Culture, Protein Electrophoresis.<br/><b>Software:</b> Rosalind BioInformatics tools, R, Python, PyMOL.",
    experience=[
        {
            "role": "Senior Research Specialist",
            "company": "BioGen Technologies",
            "dates": "2024 - Present",
            "bullets": [
                "Analyzed ATP synthesis and eukaryotic mitochondrial respiration across plant cell variants.",
                "Engineered scalable sequencing workflows reducing cellular assay runtime by 18%."
            ]
        }
    ],
    projects=[],
    education="<b>Master of Science in Biological Sciences</b> — Stanford University"
)

# 3. Real History / Humanities Resume
create_professional_cv(
    filename="resume_history.pdf",
    name="Marcus Vance",
    contact="Chicago, IL | m.vance@archival.org | linkedin.com/in/marcusvance",
    summary="Archival Specialist and Historian specializing in 19th-century Industrialization economic shifts and modern geopolitical treaty analysis.",
    skills="<b>Research Methodologies:</b> Archival Digitization, Primary Document Analysis, Historical Pedagogy.",
    experience=[
        {
            "role": "Lead Archival Researcher",
            "company": "National Historical Foundation",
            "dates": "2023 - Present",
            "bullets": [
                "Curated 500+ primary source records from the British Industrial Revolution.",
                "Published comparative historical analyses on World War I European alliance structures."
            ]
        }
    ],
    projects=[],
    education="<b>Bachelor of Arts in World History</b> — University of Oxford"
)

print("Realistic professional PDF resumes generated!")
