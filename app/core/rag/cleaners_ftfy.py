import re
import ftfy


def clean_text(text: str, preserve_structure: bool = True) -> str:
    if not text:
        return ""
    
    text = ftfy.fix_text(text)
    text = ftfy.fix_text(text, normalization='NFC')
    
    if preserve_structure:
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]', '', text)
        text = re.sub(r'\n\n\n+', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
    else:
        text = re.sub(r'[\x00-\x1F\x7F-\x9F]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
    
    return text.strip()
