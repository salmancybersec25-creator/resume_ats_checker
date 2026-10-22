import streamlit as st
import pypdf
import io
import os
from google import genai
from google.genai import types

# --- Page Configuration ---
st.set_page_config(page_title="AI ATS Resume Checker", page_icon="📄", layout="wide")

# --- Load Custom CSS ---
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("app.css")

# --- Helper Functions ---
def extract_text_from_pdf(uploaded_file):
    """Extracts text from an uploaded PDF file."""
    try:
        pdf_reader = pypdf.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        st.error(f"⚠️ Error reading PDF: {e}")
        return ""

def get_gemini_response(resume_text, job_description, api_key):
    """Sends the resume and JD to Gemini for analysis."""
    try:
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are an expert ATS (Applicant Tracking System) and senior recruiter. 
        Evaluate the following resume against the provided job description.

        **Job Description:**
        {job_description}

        **Resume:**
        {resume_text}

        **Instructions:**
        1. Provide an **ATS Score** out of 100.
        2. Identify **Missing Keywords** (skills, tools, or qualifications present in the JD but missing from the resume).
        3. List **Formatting Issues** (e.g., missing sections, poor structure, contact info).
        4. Provide **Actionable Improvements** (how to rewrite or add content to increase the score).
        5. Give a brief **Profile Summary** of the candidate based on the resume.

        Format the output clearly with headings and bullet points.
        """
        
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                top_p=0.95,
                max_output_tokens=2048,
            )
        )
        return response.text
    except Exception as e:
        st.error(f"⚠️ API Error: {e}")
        return None

# --- Main App UI ---
st.title("📄 AI ATS Resume Checker")
st.markdown('<p class="sub-header">Upload your resume and paste the job description to get an instant ATS score and improvement tips powered by Gemini.</p>', unsafe_allow_html=True)

# --- Permanent API Key Handling ---
api_key = None
try:
    # Tries to load from Streamlit secrets (for deployed app)
    api_key = st.secrets["GEMINI_API_KEY"]
    st.sidebar.success("✅ API Key loaded securely.")
except (FileNotFoundError, KeyError):
    # Fallback to manual input (for local testing)
    with st.sidebar:
        st.header("⚙️ Configuration")
        api_key = st.text_input(
            "Enter your Google Gemini API Key", 
            type="password",
            help="Get your key from https://aistudio.google.com/app/apikey"
        )
        st.markdown("[Get a free API Key](https://aistudio.google.com/app/apikey)")

# Input section
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Resume")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

with col2:
    st.subheader("2. Job Description")
    job_description = st.text_area("Paste the job description here", height=250)

# Analyze Button
if st.button("🚀 Analyze Resume", type="primary", use_container_width=True):
    if not api_key:
        st.warning("Please enter your Gemini API Key in the sidebar.")
    elif not uploaded_file:
        st.warning("Please upload a PDF resume.")
    elif not job_description:
        st.warning("Please paste the job description.")
    else:
        with st.spinner("Analyzing your resume... This may take a moment."):
            resume_text = extract_text_from_pdf(uploaded_file)
            
            if resume_text:
                result = get_gemini_response(resume_text, job_description, api_key)
                if result:
                    st.success("Analysis Complete!")
                    st.markdown("---")
                    # Wrap the result in a nice container
                    with st.container(border=True):
                        st.markdown(result)
            else:
                st.error("Could not extract text from the PDF. Please ensure it is a valid, text-based PDF.")

# Footer
st.markdown("---")
st.caption("Built with Streamlit and Google Gemini. Note: AI analysis should be used as a guide, not a definitive metric.")