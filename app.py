import streamlit as st
import json
from jd_pdf_parser import parse_job_description_pdf

# ---------------------------------------------------------
# Streamlit Page Setup
# ---------------------------------------------------------
st.set_page_config(
    page_title="JD Analyzer",
    layout="wide",
    page_icon="🧠",
)

st.title("🧠 Intelligent Job Description Analyzer")
st.markdown("Upload any **PDF or DOCX** job description to extract skills, responsibilities, domain, and more.")

# ---------------------------------------------------------
# File Upload
# ---------------------------------------------------------
uploaded = st.file_uploader(
    "📄 Upload Job Description (PDF or DOCX)",
    type=["pdf", "docx"]
)

if uploaded:
    file_ext = uploaded.name.split(".")[-1].lower()
    temp_path = f"uploaded_jd.{file_ext}"

    # Save file temporarily
    with open(temp_path, "wb") as f:
        f.write(uploaded.getbuffer())

    st.info("⏳ Processing job description... Please wait.")

    try:
        result = parse_job_description_pdf(temp_path)
        st.success("✅ Job Description processed successfully!")
    except Exception as e:
        st.error(f"❌ Error while processing: {e}")
        st.stop()

    # ---------------------------------------------------------
    # Display Extracted Skills
    # ---------------------------------------------------------
    st.markdown("## 📌 Extracted Skills")
    if result["skills"]:
        st.write(", ".join(result["skills"]))
    else:
        st.warning("No skills detected.")

    # ---------------------------------------------------------
    # Responsibilities Section
    # ---------------------------------------------------------
    st.markdown("## 📌 Responsibilities Identified")
    if result["responsibilities"]:
        for r in result["responsibilities"]:
            st.markdown(f"- {r}")
    else:
        st.info("No responsibilities detected for this JD.")

    # ---------------------------------------------------------
    # Metadata Columns
    # ---------------------------------------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📌 Seniority Level")
        st.write(result["seniority_level"])

    with col2:
        st.subheader("📌 Tech Stack Identified")
        st.write(", ".join(result["tech_stack"]) if result["tech_stack"] else "Not found")

    with col3:
        st.subheader("📌 Domain Classification")
        st.write(result["domain"])

    # ---------------------------------------------------------
    # Keywords
    # ---------------------------------------------------------
    st.markdown("## 📌 Keywords")
    if result["keywords"]:
        st.write(", ".join(result["keywords"]))
    else:
        st.write("No keywords extracted.")

    # ---------------------------------------------------------
    # Cleaned Job Description Text
    # ---------------------------------------------------------
    with st.expander("📄 View Cleaned JD Text"):
        st.write(result["cleaned_text"])

    # ---------------------------------------------------------
    # Embedding Vector (Hidden behind expander)
    # ---------------------------------------------------------
    with st.expander("🧠 View JD Embedding Vector"):
        st.write(result["embedding"])

    # ---------------------------------------------------------
    # Download JSON Button
    # ---------------------------------------------------------
    st.download_button(
        label="⬇️ Download Extracted JD Data (JSON)",
        data=json.dumps(result, indent=2),
        file_name="parsed_job_description.json",
        mime="application/json"
    )

else:
    st.info("Upload a PDF or DOCX file to begin.")
