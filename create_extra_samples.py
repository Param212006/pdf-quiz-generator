from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def make_pdf(filename, title, content_paragraphs):
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    story = [Paragraph(f"<b>{title}</b>", styles['Title']), Spacer(1, 12)]
    
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, leading=14)
    for p in content_paragraphs:
        story.append(Paragraph(p, body_style))
        story.append(Spacer(1, 10))
        
    doc.build(story)

science_p = [
    "1. Cellular Biology and Bioenergetics: The cell is the fundamental unit of structure and function in living organisms. Prokaryotes lack membrane-bound nuclei, whereas eukaryotes contain distinct organelles such as mitochondria, which synthesize adenosine triphosphate (ATP) through cellular respiration. Ribosomes translate genetic code into proteins.",
    "2. Photosynthesis & Molecular Genetics: Photosynthesis occurs inside plant chloroplasts where light energy converts water and carbon dioxide into glucose and oxygen gas. DNA (deoxyribonucleic acid) utilizes adenine, thymine, cytosine, and guanine nitrogenous base pairs to store genetic data in a double helix structure.",
    "3. Ecosystem Ecology & Human Systems: Trophic structures direct energy flow from primary autotrophic producers to secondary consumers. Decomposers recycle essential organic nitrogen and carbon. In humans, deoxygenated blood returns to the right heart atrium before entering lungs via pulmonary arteries."
]

ai_p = [
    "1. Machine Learning & Paradigms: Artificial Intelligence simulates human cognitive tasks using computational algorithms. Machine learning algorithms train models on empirical data without manual rule encoding. Supervised learning pairs inputs with explicit targets for classification and regression tasks.",
    "2. Neural Networks & Deep Learning: Deep artificial neural networks feature input, hidden, and output node layers connected by tunable numeric weights. Training utilizes backpropagation and gradient descent optimization to decrease error loss functions.",
    "3. Large Language Models: Transformer architectures process long sequence contexts using multi-head self-attention mechanisms. Auto-regressive generation predicts subsequent tokens probabilistically to complete natural language queries."
]

history_p = [
    "1. The Industrial Revolution: Transitioning European economies from manual artisan labor to factory production systems between 1760 and 1840, industrialization relied on British coal deposits, steam engines, mechanized textile looms, and widespread urbanization.",
    "2. World War I & Global Alliances: Systemic factors including militarism, imperialism, and European alliance chains escalated into continental conflict following the June 1914 assassination of Archduke Franz Ferdinand. trench warfare dominated the Western Front until the 1918 Armistice.",
    "3. World War II & Modern Diplomacy: Sparked by the 1939 German invasion of Poland, WWII allied forces defeated Axis coalitions in 1945. The subsequent international order established the United Nations to prevent future geopolitical aggression."
]

make_pdf("sample.pdf", "Science & Biology Sample Document", science_p)
make_pdf("sample_ai.pdf", "AI & Machine Learning Sample Document", ai_p)
make_pdf("sample_history.pdf", "World History Sample Document", history_p)
print("Native text PDF files generated successfully!")
