# backend/utils/files.py
import os
from PyPDF2 import PdfReader
from docx import Document

KNOWLEDGE_FILE = "knowledge_base.txt"

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    return "\n".join([p.extract_text() or "" for p in reader.pages])

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def append_to_knowledge_base(filename: str, content: str):
    with open(KNOWLEDGE_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n--- DOCUMENT : {filename} ---\n")
        f.write(content.strip())
        f.write("\n\n")
