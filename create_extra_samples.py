from pypdf import PdfWriter
from pypdf.annotations import FreeText

def create_pdf(filename, text):
    writer = PdfWriter()
    page = writer.add_blank_page(width=612, height=792)
    annotation = FreeText(
        text=text,
        rect=(50, 50, 562, 742),
        font="Helvetica",
        font_size="12pt",
    )
    writer.add_annotation(page_number=0, annotation=annotation)
    with open(filename, "wb") as f:
        writer.write(f)

ai_text = """Artificial Intelligence and Machine Learning Overview
Artificial Intelligence (AI) is the simulation of human intelligence by computer systems.
Key subfields include Machine Learning (ML), Deep Learning, and Natural Language Processing (NLP).
Machine Learning relies on algorithms trained on data to make predictions or decisions.
Supervised learning uses labeled datasets, whereas unsupervised learning finds hidden patterns in unlabeled data.
Reinforcement learning trains models through rewards and penalties.
Large Language Models (LLMs) utilize transformer architectures to process and generate human-like text."""

history_text = """World History Overview: The Industrial Revolution and Modern Era
The Industrial Revolution began in Great Britain in the late 18th century, transitioning economies from agrarian to industrial manufacturing.
Key inventions included the steam engine by James Watt and mechanized textile production.
The 20th century was marked by World War I (1914–1918) and World War II (1939–1945), leading to major political realignments.
The United Nations was established in 1945 to promote international cooperation and prevent future global conflicts.
The Cold War dominated global politics in the second half of the 20th century until the dissolution of the Soviet Union in 1991."""

create_pdf("sample_ai.pdf", ai_text)
create_pdf("sample_history.pdf", history_text)
print("Sample PDFs generated successfully.")
