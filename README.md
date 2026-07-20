# 🤖 AI Resume Screening & Recruitment Assistant

An AI-powered Resume Screening System that helps recruiters automatically analyze resumes, calculate ATS scores, generate interview questions, evaluate candidates using LLMs, and send interview invitations.

---

# 🚀 Features

- 📄 Resume Parsing (PDF)
- 🎯 ATS Score Calculation
- 🧠 AI Candidate Evaluation
- 🎤 AI Interview Question Generation
- 📊 Skill Matching
- 📑 PDF Report Generation
- 📧 Email Interview Invitation
- 🔍 Resume Search & Filtering
- 🤖 Google Gemini Integration
- ⚡ FAISS Vector Search
- 🌐 Streamlit Web Application

---

## 📸 Screenshots

### Home Page

![Dark themed admin login screen for Resume Screening RAG Chatbot showing login form with username password fields and a login button on a dark background](assets/home.png)

## 📄 Job Description Upload

![Job description upload interface with an upload panel and instructions for adding job details in a recruitment assistant layout](assets/job_description.png)

## 👤 Candidate Dashboard

![Candidate dashboard displaying evaluation metrics panels and filtered applicant data cards in a recruitment system interface](assets/candidate_dashboard.png)

## 📑 Candidate Resume

![Parsed candidate resume view showing highlighted extracted skills and experience fields in the application interface](assets/candidate_resume.png)


## 📊 ATS Score Visualization

![Dashboard visualization showing ATS score distribution and candidate ranking charts with performance metrics in the application interface](assets/ats_score_visualization.png)

## 📈 ATS Score Comparison

![Comparison chart showing ATS score differences across candidate resumes with bars comparing percentages](assets/ats_score_comparison.png)

---

### Candidate Analysis

![Analytics section of recruitment dashboard with title analytics and a resume ranking list showing Resume3.pdf 57.05% Match Resume2.pdf 38.72% Match Resume1.pdf 36.67% Match Resume4.pdf 34.69% Match plus a download ATS report prompt on a dark background](assets/analytics.png)

---

### AI Tools

![AI tools panel showing options for interview question generation and candidate evaluation features in a sidebar layout](assets/ai_tools.png)

---

### Reports

![Reports section showing PDF report generation options and summary output with document icon and report controls](assets/reports.png)

## 🏆 Top Candidate

![Top candidate profile highlighted in the recruitment dashboard as best match for the role with candidate match score emphasis](assets/top_candidate.png)

## 💬 User Queries

![User query interface showing chat-style questions and responses about candidate information](assets/user_queries.png)

# 🛠️ Tech Stack

Frontend
- Streamlit

Backend
- Python

AI
- Google Gemini
- LangChain

Vector Database
- FAISS

Embeddings
- HuggingFace Sentence Transformers

Libraries
- PyMuPDF
- Pandas
- ReportLab
- dotenv

---

# 📂 Project Structure

```
AI-Resume-Screening-System
│
├── app.py
├── src/
├── pages/
├── utils/
├── reports/
├── assets/
├── data/
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/roniarosariosamk/AI-Resume-Screening-System.git
```

Go into the project

```bash
cd AI-Resume-Screening-System
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

# 🔑 Environment Variables

Create a `.env` file:

```
GOOGLE_API_KEY=your_api_key
EMAIL=your_email@gmail.com
APP_PASSWORD=your_app_password
```

---

# ✨ Future Enhancements

- AI Resume Chat
- Candidate Ranking
- Recruiter Dashboard
- Database Integration
- Multi-user Authentication
- Docker Deployment

---

# 👨‍💻 Author

**Ronia Rosario Sam K**

B.Tech – Artificial Intelligence & Data Science

GitHub:
https://github.com/roniarosariosamk

---

# ⭐ If you found this project useful, consider giving it a star!

[def]: E:\ragbot\RAGBOT\ragbot\src\assets\home.png