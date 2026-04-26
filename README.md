# AI-Skill-Assessment-Agent
# 🧠 SkillLens – AI Skill Assessment & Learning Agent

An AI-powered application that evaluates a candidate’s resume against a job description, assesses real skill proficiency, identifies gaps, and generates a **personalized learning roadmap with curated resources**.

---

## 🚀 Live Demo

(https://ai-skill-assessment-agent-nrswznarccupq57fchtefd.streamlit.app/)

---

## 📌 Problem Statement

Resumes only reflect what candidates *claim* to know—not how well they actually know it.
Recruiters lack tools to assess real proficiency, and candidates don’t get actionable feedback.

---

## 💡 Solution

SkillLens uses an AI agent to:

* Analyze resumes vs job descriptions
* Evaluate **actual skill proficiency**
* Identify **strengths, weak areas, and missing skills**
* Generate a **personalized learning plan**
* Provide **curated, real learning resources**
* Enable **interactive AI mentorship via chat**

---

## ✨ Features

* 📊 **Job Fit Score** – Quantifies how well a candidate matches a role
* 🧩 **Skill Breakdown** – Strengths, weak skills, and missing skills
* 📚 **Personalized Learning Plan** – Step-by-step roadmap
* 🔗 **Curated Resources** – No fake links, only verified learning sources
* 🤖 **AI Chat Assistant** – Ask questions and get career guidance
* 🎨 **Premium UI** – Glassmorphism-based modern interface

---

## 🧠 How It Works

1. Upload resume (PDF)
2. Paste job description
3. AI analyzes both using a structured prompt
4. Generates:

   * Skill evaluation
   * Match score
   * Learning roadmap
5. System enhances output with **verified resource mapping**
6. User can interact via chat for deeper guidance

---

## ⚙️ Tech Stack

* **Frontend**: Streamlit
* **AI Model**: OpenRouter (LLM API)
* **Backend Logic**: Python
* **PDF Parsing**: PyPDF2
* **Prompt Engineering**: Custom structured prompts

---

## 🏗️ Project Structure

```
AI-Skill-Assessment-Agent/
│
├── app.py
├── prompts/
│   └── analysis_prompt.txt
├── requirements.txt
└── README.md
```

---

## 🔑 Setup Instructions (Local)

```bash
git clone https://github.com/your-username/AI-Skill-Assessment-Agent.git
cd AI-Skill-Assessment-Agent

pip install -r requirements.txt
```

Create `.env` file:

```
OPENROUTER_API_KEY=your_api_key_here
```

Run the app:

```bash
streamlit run app.py
```

---

## ☁️ Deployment

Deployed using **Streamlit Community Cloud**

* Add API key in **Secrets**
* Set app path: `app.py`

---

## 🎯 Key Highlights

* ✅ Single-call AI agent for evaluation + planning
* ✅ Structured JSON → clean UI transformation
* ✅ Fixed hallucination issue using curated resource mapping
* ✅ Designed for **both recruiters and candidates**

---

## 🚀 Future Improvements

* Resume improvement suggestions
* Interview simulation module
* Skill graph / analytics visualization
* Multi-role comparison

---

## 👨‍💻 Author

**Harsh Barnwal**
📧 [harshbarnwal7216@gmail.com](mailto:harshbarnwal7216@gmail.com)


---

## ⭐ If you like this project

Give it a ⭐ on GitHub and support the work!
