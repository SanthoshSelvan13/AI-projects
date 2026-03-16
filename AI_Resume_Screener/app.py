import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pdfplumber
import google.generativeai as genai

genai.configure(api_key="AIzaSyDg9LhZbzmjgFnYxd9G-1cMp_e-MuiKTwY")
model = genai.GenerativeModel("models/gemini-1.5-flash")

st.title("AI Resume Screener")
job_description = st.text_area("Enter Job Description")
uploaded_files = st.file_uploader(
    "Upload Resumes",
    accept_multiple_files=True,
    type=["pdf"]
)

def extract_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text


def analyze_resume(resume_text, job_description):
    prompt = f"""
    Job Description:
    {job_description}
    Resume:
    {resume_text}
    Give ONLY a number between 0 and 100 for match score.
    """
    response = model.generate_content(prompt)
    score_text = response.text.strip()
    try:
        score = int(score_text)
    except:
        score = 0
    return score


if uploaded_files and job_description:
    results = []
    for file in uploaded_files:
        resume_text = extract_text(file)
        score = analyze_resume(resume_text, job_description)
        results.append({
            "Candidate": file.name,
            "Score": score
        })

    df = pd.DataFrame(results)
    df = df.sort_values(by="Score", ascending=False)
    
    st.subheader("Top Candidates")
    st.dataframe(df)

    fig, ax = plt.subplots()
    ax.bar(df["Candidate"], df["Score"])
    ax.set_xlabel("Candidate")
    ax.set_ylabel("Score")
    ax.set_title("Resume Match Scores")
    st.pyplot(fig)