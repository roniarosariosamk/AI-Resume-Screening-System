from src.skill_matcher import extract_skills

sample = """
Python Developer

Skills Required

Python
SQL
Machine Learning
Docker
Git
AWS
"""

skills = extract_skills(sample)

print("=" * 50)
print("Extracted Skills")
print("=" * 50)

for skill in skills:
    print(skill)