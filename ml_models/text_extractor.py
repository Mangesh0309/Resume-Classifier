import os
from typing import Optional
from docx import Document
from pdfminer.high_level import extract_text as extract_text_pdf

def extract_text_from_file(file_path: str) -> str:
    """
    Extract text from various file formats (PDF, DOCX, TXT)
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == '.docx':
        return extract_text_from_docx(file_path)
    elif file_extension == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from PDF file
    """
    return extract_text_pdf(file_path)

def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from DOCX file
    """
    doc = Document(file_path)
    return ' '.join([paragraph.text for paragraph in doc.paragraphs])
