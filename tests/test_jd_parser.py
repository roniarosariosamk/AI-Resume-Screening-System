from src.jd_parser import extract_job_description

pdf_path = "data/job_description/job_description.pdf"

text = extract_job_description(pdf_path)

print("=" * 60)
print("JOB DESCRIPTION")
print("=" * 60)
print(text)