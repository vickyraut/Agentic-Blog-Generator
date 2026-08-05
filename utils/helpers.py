import re
import math
from io import BytesIO
from fpdf import FPDF

def calculate_blog_stats(text: str, generation_time_sec: float = 0.0, language: str = "English"):
    """
    Calculate word count, character count, estimated reading time, and metadata.
    """
    if not text:
        return {
            "word_count": 0,
            "char_count": 0,
            "reading_time": "0 min",
            "generation_time": f"{generation_time_sec:.2f}s",
            "language": language
        }
    
    # Strip markdown syntax for accurate word count
    clean_text = re.sub(r'[#*`_\[\]()>-]', ' ', text)
    words = clean_text.split()
    word_count = len(words)
    char_count = len(text)
    
    # Average reading speed: 200 words per minute
    reading_time_minutes = max(1, math.ceil(word_count / 200)) if word_count > 0 else 0
    reading_time_str = f"{reading_time_minutes} min read" if reading_time_minutes > 0 else "< 1 min read"

    return {
        "word_count": f"{word_count:,}",
        "char_count": f"{char_count:,}",
        "reading_time": reading_time_str,
        "generation_time": f"{generation_time_sec:.2f}s",
        "language": language
    }


def encode_latin1_safe(text: str) -> str:
    """
    Sanitize text for standard FPDF Helvetica font encoding by replacing
    unsupported Unicode characters with ASCII equivalents.
    """
    substitutions = {
        '•': '-',
        '–': '-',
        '—': '-',
        '“': '"',
        '”': '"',
        '‘': "'",
        '’': "'",
        '…': '...',
    }
    for char, replacement in substitutions.items():
        text = text.replace(char, replacement)
    return text.encode('latin-1', 'replace').decode('latin-1')


def generate_pdf_bytes(title: str, content: str) -> bytes:
    """
    Generate a clean, styled PDF document from Markdown content using FPDF2.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    epw = pdf.epw  # Effective page width

    # Title
    pdf.set_font("Helvetica", style="B", size=18)
    safe_title = encode_latin1_safe(title)
    pdf.multi_cell(epw, 10, safe_title, align="L")
    pdf.ln(5)

    # Line Separator
    pdf.set_draw_color(200, 200, 200)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(8)

    # Content Body
    lines = content.split("\n")
    for line in lines:
        line_clean = encode_latin1_safe(line)
        if line_clean.startswith("# "):
            pdf.set_font("Helvetica", style="B", size=16)
            pdf.multi_cell(epw, 8, line_clean[2:].strip())
            pdf.ln(2)
        elif line_clean.startswith("## "):
            pdf.set_font("Helvetica", style="B", size=14)
            pdf.multi_cell(epw, 7, line_clean[3:].strip())
            pdf.ln(2)
        elif line_clean.startswith("### "):
            pdf.set_font("Helvetica", style="B", size=12)
            pdf.multi_cell(epw, 6, line_clean[4:].strip())
            pdf.ln(1)
        elif line_clean.startswith("- ") or line_clean.startswith("* "):
            pdf.set_font("Helvetica", size=11)
            pdf.multi_cell(epw, 6, f"  - {line_clean[2:].strip()}")
        else:
            pdf.set_font("Helvetica", size=11)
            if line_clean.strip():
                pdf.multi_cell(epw, 6, line_clean)
            else:
                pdf.ln(3)

    return bytes(pdf.output())


