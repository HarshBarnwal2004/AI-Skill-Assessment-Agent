import streamlit as st
import PyPDF2
import io
import json
import os
from openai import OpenAI
import urllib.parse
from dotenv import load_dotenv


RESOURCE_MAP = {
    "python": [
        "https://youtu.be/_uQrJ0TkZlc",
        "https://realpython.com/"
    ],
    "sql": [
        "https://www.w3schools.com/sql/",
        "https://mode.com/sql-tutorial/"
    ],
    "docker": [
        "https://youtu.be/fqMOX6JJhGo",
        "https://docs.docker.com/get-started/"
    ],
    "aws": [
        "https://youtu.be/ulprqHHWlng",
        "https://aws.amazon.com/getting-started/"
    ],
    "machine learning": [
        "https://www.coursera.org/learn/machine-learning",
        "https://scikit-learn.org/"
    ]
}

# ---------------- CONFIG ----------------
load_dotenv()

try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except:
    api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    st.error("API key not found. Add it in .env or Streamlit secrets.")
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

st.set_page_config(page_title="SkillLens", layout="wide")

# ---------------- STYLING ----------------
st.markdown("""
<style>

/* Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

/* Glass Card */
.glass {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(14px);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 0 20px rgba(0,0,0,0.3);
}

/* Glow */
.glow {
    box-shadow: 0 0 15px rgba(34,197,94,0.3);
}

/* Button */
.stButton>button {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    border: none;
}

/* Chat */
.chat-user {
    text-align:right;
    background:#2563eb;
    padding:10px;
    border-radius:12px;
    margin:5px;
    color:white;
}

.chat-ai {
    text-align:left;
    background:rgba(255,255,255,0.05);
    padding:10px;
    border-radius:12px;
    margin:5px;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------

def load_prompt():
    base_dir = os.path.dirname(__file__)
    path = os.path.join(base_dir, "prompts", "analysis_prompt.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_text(file):
    pdf = PyPDF2.PdfReader(io.BytesIO(file))
    text = ""
    for page in pdf.pages:
        if page.extract_text():
            text += page.extract_text()
    return text


def safe_json(text):
    try:
        return json.loads(text)
    except:
        try:
            cleaned = text.split("```")[-1]
            return json.loads(cleaned)
        except:
            return None


def analyze(resume_text, jd_text):
    base_prompt = load_prompt()

    prompt = f"""
{base_prompt}

Resume:
{resume_text[:1500]}

Job Description:
{jd_text}
"""

    res = client.chat.completions.create(
        model="openai/gpt-oss-120b:free",
        messages=[
            {"role": "system", "content": "Return only JSON"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return safe_json(res.choices[0].message.content)


def chat_with_ai(context, question):
    res = client.chat.completions.create(
        model="openai/gpt-oss-120b:free",
        messages=[
            {"role": "system", "content": "You are an AI career coach."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
        ],
        temperature=0.4
    )
    return res.choices[0].message.content


# ---------------- SESSION ----------------
if "result" not in st.session_state:
    st.session_state.result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>🧠 SkillLens</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>AI-powered skill assessment & learning roadmap</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- INPUT ----------------
st.markdown("<div class='glass'>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    uploaded_file = st.file_uploader("📄 Upload Resume", type="pdf")

with col2:
    jd = st.text_area("📝 Paste Job Description", height=150)

analyze_btn = st.button("🚀 Analyze Profile")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- ANALYSIS ----------------
if analyze_btn:
    if not uploaded_file or not jd:
        st.warning("Please upload resume and enter JD")
    else:
        with st.spinner("Analyzing..."):
            resume_text = extract_text(uploaded_file.read())
            result = analyze(resume_text, jd)

    # -------- FIX RESOURCE LINKS --------
    for item in result.get("learning_plan", []):
        skill = item["skill"].lower()

        if skill in RESOURCE_MAP:
            item["resources"] = RESOURCE_MAP[skill]
        else:
            encoded_skill = urllib.parse.quote(skill)

            item["resources"] = [
                f"https://www.youtube.com/results?search_query=learn+{encoded_skill}",
                f"https://www.google.com/search?q={encoded_skill}+tutorial"
            ]

    st.session_state.result = result

    

# ---------------- RESULTS ----------------
if st.session_state.result:
    result = st.session_state.result

    tab1, tab2, tab3 = st.tabs(["📊 Overview", "📚 Learning Plan", "🤖 Chat"])

    # ---------- OVERVIEW ----------
    with tab1:
        st.markdown("<div class='glass glow'>", unsafe_allow_html=True)
        st.markdown(f"<h2>🎯 Match Score: {result['job_fit_percentage']}%</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"<div class='glass'><b>Strengths</b><br>{', '.join(result['strengths'])}</div>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"<div class='glass'><b>Weak</b><br>{', '.join(result['weak_skills'])}</div>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"<div class='glass'><b>Missing</b><br>{', '.join(result['missing_skills'])}</div>", unsafe_allow_html=True)

        for s in result["skill_analysis"]:
            st.markdown(
                f"<div class='glass'><b>{s['skill']}</b> — {s['score']}/10 ({s['level']})<br>{s['reason']}</div>",
                unsafe_allow_html=True
            )

    # ---------- LEARNING ----------
    with tab2:
        for p in result["learning_plan"]:
            with st.expander(f"📌 {p['skill']}"):
                st.markdown("<div class='glass'>", unsafe_allow_html=True)
                st.write(p["why_needed"])

                for step in p["roadmap"]:
                    st.write(f"- {step}")

                for r in p["resources"]:
                    st.markdown(f"[Open Resource]({r})")

                st.markdown("</div>", unsafe_allow_html=True)

    # ---------- CHAT ----------
    with tab3:
        st.markdown("### 🤖 AI Assistant")

        col1, col2 = st.columns([4, 1])

        with col1:
            user_input = st.text_input("Ask anything...", key="chat_input")

        with col2:
            send = st.button("Send")

        if send and user_input:
            response = chat_with_ai(result, user_input)

            st.session_state.chat_history.append(("user", user_input))
            st.session_state.chat_history.append(("ai", response))

        for role, msg in st.session_state.chat_history:
            if role == "user":
                st.markdown(f"<div class='chat-user'>{msg}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-ai'>{msg}</div>", unsafe_allow_html=True)
