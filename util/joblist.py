import json

with open("Data/jobs.json", "r") as f:
    data = json.load(f)


jobs = data["jobs"]  

job_requirements = [job["skills_needed"] for job in jobs]

job_requirements_list = []

for job in job_requirements:
    job = ' '.join(job)
    job_requirements_list.append(job)
    
print(jobs) 
    