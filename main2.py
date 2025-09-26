import numpy as np
import dateparser

from collections import Counter
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from itertools import islice

from sklearn.feature_extraction.text import TfidfVectorizer

import pdfplumber
import docx
# import spacy
import os
import re

import spacy
 
from util.handle_resume import load_resume_text,extract_experience_section,extract_structured_experience_entries,extract_projects_section,extract_structured_projects, extract_education_section, extract_structured_education 
from util.joblist import jobs,job_requirements_list
from Data.skills import domains
from util.recommend import recommend_jobs, find_skills_and_distribution

from sentence_transformers import SentenceTransformer, util
from transformers import pipeline




model = SentenceTransformer("all-MiniLM-L6-v2")
    
file_path = "Data/Resume Full Time ML V220 Doc.docx" # or .docx
# file_path = "Data/Resume Part Time.docx"

resume_text = load_resume_text(file_path)


experience_text = extract_experience_section(resume_text)
project_text = extract_projects_section(resume_text)
education_text = extract_education_section(resume_text)



structured_projects = extract_structured_projects(project_text)

structured_education = extract_structured_education(education_text)

# print(f'\n Education section : \n {structured_education}')

for education in structured_education:
    print(f"degree : {education['degree_level']}")
    print(f"course : {education['degree_subject']}")



print("\nExtracted Experience Section:\n")
structured_experience = extract_structured_experience_entries(experience_text)

for experience in structured_experience:
    print(experience,'\n')
    
project_text = []
summary_text = []
    
for experience in structured_experience:
    summary = experience['summary']
    summary_text.append(summary)

for project in structured_projects:
    project_desc = project['description']
    project_text.append(project_desc)    

summary_text = ' '.join(summary_text)
project_text = ' '.join(project_text)

summary = summary_text + project_text

# print(project_text)
        
recommend_jobs(model,summary_text,jobs)  

# print(f'Summary \n {summary}')     


            
            
find_skills_and_distribution(model,summary,domains,'Work Experience and Projects')   
find_skills_and_distribution(model,project_text,domains,'Projects')         