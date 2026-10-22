# AI ATS Resume Checker 📄

An intelligent web application that evaluates a resume against a job description using Google's Gemini 2.0 Flash model. It provides an ATS score, missing keywords, formatting issues, and actionable improvement tips.

## Features ✨
*   **ATS Score:** Get a match percentage out of 100.
*   **Keyword Analysis:** Identifies missing skills and keywords.
*   **Actionable Feedback:** Suggests improvements to your resume.
*   **Easy to Use:** Simple UI with file upload and text area.

## Tech Stack 🛠️
*   **Frontend:** Streamlit
*   **AI Model:** Google Gemini 3.8 Flash (`gemini-3.8-flash`)
*   **PDF Parsing:** PyPDF2

## Getting Started 🚀
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`
4. Enter your Google Gemini API key in the sidebar.
5. Upload your resume and paste the job description.

## Deployment ☁️
This app can be easily deployed on Streamlit Community Cloud. Follow the steps in the deployment guide below.
