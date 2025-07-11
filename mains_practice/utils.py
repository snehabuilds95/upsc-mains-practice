import re
from PyPDF2 import PdfReader

def remove_hindi(text):
    return ''.join(char for char in text if not '\u0900' <= char <= '\u097F')

def extract_questions_from_file(file):
    reader = PdfReader(file)
    full_text = " ".join([page.extract_text() or '' for page in reader.pages])

    lines = full_text.split('\n')
    english_lines = [line.strip() for line in lines if not any('\u0900' <= ch <= '\u097F' for ch in line)]
    text = " ".join(english_lines)

    question_blocks = re.findall(r'\d+\.\s.*?(?=\d+\.\s|$)', text, re.DOTALL)

    extracted = []
    for i, block in enumerate(question_blocks, start=1):
        marks = 0
        marks_match = re.search(r'(\d{1,2})\s*(½|\.5)?\s*$', block)
        if marks_match:
            whole = int(marks_match.group(1))
            frac = marks_match.group(2)
            marks = whole + 0.5 if frac in ['½', '.5'] else whole

        block_without_marks = re.sub(r'(\d{1,2})\s*(½|\.5)?\s*$', '', block).strip()
        cleaned_text = remove_hindi(block_without_marks)
        cleaned_text = re.sub(r'^\d+\.\s*', '', cleaned_text).strip()

        if cleaned_text:
            extracted.append({
                'number': i,
                'text': cleaned_text,
                'marks': marks
            })

    print(f"\n✅ Extracted {len(extracted)} questions:")
    for q in extracted:
        print(f"Q{q['number']} → {q['marks']} marks\n{q['text']}\n")

    return extracted
