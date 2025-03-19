import os
from io import BytesIO

import docx
import PyPDF2
import spacy

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# File path to store potential hires for the employer
POTENTIAL_HIRES_PATH = "potential_hires.txt"

#  extract skills from the text
def extract_skills(text):
    skills = ["python", "java", "sql", "communication", "teamwork", "leadership", "html", "css", "project management", "ai", "machine learning"]
    text = text.lower()
    found_skills = [skill for skill in skills if skill in text]
    return found_skills

#  extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text

# extract text from file type
def extract_text(file):
    file.seek(0)
    if file.name.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif file.name.endswith(".docx"):
        return extract_text_from_docx(file)
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        raise ValueError("Unsupported file format")

#  analyse job listing and resume
def analyze_job_and_resume(job_file, resume_file):
    try:
        job_listing_text = extract_text(job_file) if job_file else ""
        resume_text = extract_text(resume_file)
        
        job_skills = extract_skills(job_listing_text)
        resume_skills = extract_skills(resume_text)
        
        missing_skills = [skill for skill in job_skills if skill not in resume_skills]
        extra_skills = [skill for skill in resume_skills if skill not in job_skills]
        
        # Calculate the percentage of skills matched
        match_percentage = (len(job_skills) - len(missing_skills)) / len(job_skills) * 100 if job_skills else 0

        # Checks if potential hire - change percantage based on requiremnts
        is_potential_hire = match_percentage >= 80

        # If the employer is using the system store the applicant file if it's a potential hire
        if is_potential_hire and job_file:
            save_to_potential_hires(resume_file.name)

        return missing_skills, extra_skills, match_percentage, is_potential_hire
    except Exception as e:
        raise Exception(f"Error analyzing files: {e}")

# save the potential hire file
def save_to_potential_hires(resume_file_name):
    with open(POTENTIAL_HIRES_PATH, "a") as f:
        f.write(f"{resume_file_name}\n")
