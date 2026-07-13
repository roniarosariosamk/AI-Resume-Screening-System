# 📄 AI Resume Screening System

An AI-powered Resume Screening and Applicant Tracking System (ATS) built using **Python**, **Streamlit**, **LangChain**, **FAISS**, and **Hugging Face Embeddings**.

The system automates resume screening by comparing resumes with a Job Description, calculating ATS scores, ranking candidates, generating interview questions using AI, evaluating candidates, sending interview invitations via email, and enabling recruiters to search resumes using a Retrieval-Augmented Generation (RAG) chatbot.

## 📌 Project Overview

Recruiters often spend significant time manually reviewing resumes. This project simplifies the hiring process by leveraging Artificial Intelligence to automate resume screening and candidate evaluation.

The system allows recruiters to:

- Upload multiple resumes
- Upload a Job Description
- Automatically calculate ATS scores
- Rank candidates based on similarity
- Generate AI-powered interview questions
- Evaluate candidates using AI
- Send interview invitations
- Download ATS reports
- Ask questions about uploaded resumes using a RAG chatbot

## ✨ Features

- 🔐 Admin Login Authentication
- 📄 Multiple Resume Upload
- 📋 Job Description Upload
- 🧠 Resume Parsing
- 🎯 ATS Score Calculation
- 🏆 Resume Ranking
- 👤 Candidate Dashboard
- 📊 Analytics Dashboard
- 📈 ATS Reports
- 🤖 AI Candidate Evaluation
- 🎤 AI Interview Question Generator
- 📧 Email Interview Invitation
- 📄 PDF ATS Report Generation
- 💬 RAG-based Resume Chatbot
- 📂 Modular Project Structure

## 🛠️ Technology Stack

| Category | Technologies |
|----------|--------------|
| Programming Language | Python |
| Frontend | Streamlit |
| AI Framework | LangChain |
| Embedding Model | Hugging Face Sentence Transformers |
| Vector Database | FAISS |
| LLM | Ollama (Llama 3) |
| Resume Parsing | PyMuPDF |
| Data Visualization | Plotly |
| Data Processing | Pandas |
| PDF Report | ReportLab |
| Version Control | Git & GitHub |

## 📂 Project Structure

```text
AI-Resume-Screening-System/
│
├── app.py
├── requirements.txt
│
├── components/
│   ├── sidebar.py
│   ├── metrics.py
│   └── candidate_card.py
│
├── pages/
│   ├── upload.py
│   ├── dashboard.py
│   ├── analytics.py
│   ├── reports.py
│   ├── ai_tools.py
│   └── chatbot.py
│
├── src/
│   ├── parser.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── chatbot.py
│   ├── jd_parser.py
│   ├── resume_ranker.py
│   ├── skill_matcher.py
│   ├── interview_generator.py
│   ├── candidate_evaluator.py
│   ├── email_sender.py
│   ├── pdf_report.py
│   └── auth.py
│
├── utils/
│   ├── jd_processor.py
│   ├── resume_processor.py
│   └── constants.py
│
├── data/
│   ├── resumes/
│   └── job_description/
│
└── tests/
```

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/roniarosariosamk/AI-Resume-Screening-System.git
```

### 2. Navigate to the Project Folder

```bash
cd AI-Resume-Screening-System
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt

## 🚀 Running the Application

### Start Ollama

Make sure Ollama is installed and the required model is available.

```bash
ollama serve
```

If required, pull the model:

```bash
ollama pull llama3
```

### Run the Streamlit App

```bash
streamlit run app.py
```

The application will open automatically in your default browser.

```
http://localhost:8501
```

## 🔑 Default Admin Login

| Username | Password |
|----------|----------|
| admin | admin123 |

## 📌 Configuration

Create a `.streamlit/secrets.toml` file and configure:

```toml
EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_gmail_app_password"
```

These credentials are used to send interview invitation emails.

## 📸 Application Screenshots

> Replace the placeholders below with screenshots after deployment.

### 🔐 Admin Login

![Login](screenshots/login.png)

---

### 📄 Resume Upload

![Upload](screenshots/upload.png)

---

### 👤 Candidate Dashboard

![Dashboard](screenshots/dashboard.png)

---

### 📊 Analytics Dashboard

![Analytics](screenshots/analytics.png)

---

### 📈 ATS Reports

![Reports](screenshots/reports.png)

---

### 🤖 AI Tools

![AI Tools](screenshots/ai_tools.png)

---

### 💬 Resume Chatbot

![Chatbot](screenshots/chatbot.png)

## 🔮 Future Enhancements

- 🌐 Multi-user authentication and role-based access
- 📧 Automated interview scheduling with calendar integration
- ☁️ Cloud database integration
- 📊 Advanced recruiter analytics dashboard
- 📄 OCR support for scanned resumes
- 🎙️ AI-powered mock interview assistant
- 🌍 Multi-language resume parsing
- 📱 Responsive mobile interface

## 👨‍💻 Author

**Ronia Rosario Sam K**

B.Tech – Artificial Intelligence & Data Science

GitHub: https://github.com/roniarosariosamk

LinkedIn: linkedin.com/in/ronia-rosario-sam-k-13493a290

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

Contributions, suggestions, and feedback are always welcome.