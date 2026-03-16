import streamlit as st
import pandas as pd
import pdfplumber
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.title("AI Resume Screener")
job_description = st.text_area("Enter Job Description")
uploaded_files = st.file_uploader(
    "Upload Resumes",
    type=["pdf"],
    accept_multiple_files=True
)


def extract_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text


def calculate_score(resume_text, job_description):
    documents = [job_description, resume_text]
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(documents)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    score = similarity[0][0] * 100
    return round(score, 2)


if uploaded_files and job_description:
    results = []
    for file in uploaded_files:
        resume_text = extract_text(file)
        score = calculate_score(resume_text, job_description)
        results.append({
            "Candidate": file.name,
            "Score": score
        })

    df = pd.DataFrame(results)
    df = df.sort_values(by="Score", ascending=False)
    st.subheader("Candidate Ranking")
    st.dataframe(df)

    st.subheader("Top Candidates")
    st.dataframe(df.head())

    fig, ax = plt.subplots()
    ax.bar(df["Candidate"], df["Score"])
    ax.set_xlabel("Candidate")
    ax.set_ylabel("Match Score")
    ax.set_title("Resume Matching Score")
    st.pyplot(fig)