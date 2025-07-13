import re
from pdf2image import convert_from_path
import pytesseract

def extract_text_from_pdf(file_path):
    """
    Converts scanned PDF to text using OCR (Tesseract).
    """
    pages = convert_from_path(file_path, dpi=300)
    text = ""
    for page in pages:
        text += pytesseract.image_to_string(page, lang='eng+hin') + "\n"
    return text

def extract_questions_from_text(text):
    text = text.replace('\n', ' ')
    blocks = re.findall(r'(\d+)\.\s+(.*?)(?=(\d+\.\s)|$)', text, re.DOTALL)

    extracted = []

    for number, block, _ in blocks:
        # Skip junk before danda
        if '।' in block:
            block = block.split('।', 1)[-1]

        # Remove Hindi and junk
        block = ''.join(c for c in block if not '\u0900' <= c <= '\u097F')
        block = re.sub(r'[^\w\s.,;:\-\'\"()/?]', '', block)
        block = re.sub(r'\s+', ' ', block).strip()

        # Extract marks
        marks = 0
        marks_match = re.search(r'(\d{1,2})(½|\.5|/2|‘/2|’/2)?\s*$', block)
        if marks_match:
            whole = int(marks_match.group(1))
            frac = marks_match.group(2)
            marks = whole + 0.5 if frac else whole
            block = re.sub(r'(\d{1,2})(½|\.5|/2|‘/2|’/2)?\s*$', '', block).strip()

        # Filter valid questions
        if len(block.split()) >= 8:
            extracted.append({
                'number': int(number),
                'text': block,
                'marks': marks
            })

    # Optional debug
    print(f"\n✅ Extracted {len(extracted)} questions:")
    for q in extracted:
        print(f"Q{q['number']} → {q['marks']} marks\n{q['text']}\n")

    return extracted
