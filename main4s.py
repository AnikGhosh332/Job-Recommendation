import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from sentence_transformers import SentenceTransformer

from util.handle_resume import (
    load_resume_text,
    extract_experience_section,
    extract_structured_experience_entries,
    extract_projects_section,
    extract_structured_projects,
    extract_education_section,
    extract_structured_education,
)
from util.joblist import jobs
from Data.skills import domains
from util.recommend import recommend_jobs, find_skills_and_distribution


# ---------------------------
# Streamlit Page Config
# ---------------------------
st.set_page_config(page_title="AI Job Recommender", layout="wide")

st.title("🤖 AI Job Recommender")
st.markdown("Upload your resume to get **job recommendations, skills, domain matches, and project insights**.")


# ---------------------------
# File Uploader
# ---------------------------
uploaded_file = st.file_uploader("📂 Upload your resume (.pdf or .docx)", type=["pdf", "docx"])

if uploaded_file:
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # ---------------------------
    # Extract Resume Content
    # ---------------------------
    resume_text = load_resume_text(uploaded_file)

    experience_text = extract_experience_section(resume_text)
    structured_experience = extract_structured_experience_entries(experience_text)
    
    education_text = extract_education_section(resume_text)
    structured_education = extract_structured_education(education_text)

    project_text_raw = extract_projects_section(resume_text)
    structured_projects = extract_structured_projects(project_text_raw)

    # ---------------------------
    # Prepare Summaries
    # ---------------------------
    summary_texts = [exp["summary"] for exp in structured_experience if exp.get("summary")]
    project_texts = [proj["description"] for proj in structured_projects if proj.get("description")]

    summary_text = " ".join(summary_texts)
    project_text_combined = " ".join(project_texts)
    full_summary = summary_text + " " + project_text_combined
    
    
    # --- Show Education ---
    st.subheader("🎓 Education")
    if structured_education:
        for edu in structured_education:
            degree = edu.get("degree_level") or "N/A"
            course = edu.get("degree_subject") or "N/A"
            st.markdown(f"**{degree}** – {course}")
    else:
        st.info("No clear education details detected.")


    # ---------------------------
    # Display Extracted Experience
    # ---------------------------
    st.subheader("💼 Extracted Work Experience")
    if structured_experience:
        for exp in structured_experience:
            company = exp.get("company_name", "Unknown Company")
            position = exp.get("position", "Unknown Role")
            period = f"{exp.get('from','?')} - {exp.get('to','?')}"
            with st.expander(f"{position} @ {company} ({period})"):
                st.write(exp.get("summary", ""))
    else:
        st.info("No work experience extracted.")


    # ---------------------------
    # Display Extracted Projects
    # ---------------------------
    st.subheader("📂 Extracted Projects")
    if structured_projects:
        for proj in structured_projects:
            with st.expander(proj.get("project_name", "Project")):
                st.write(proj.get("description", ""))
    else:
        st.info("No projects extracted.")


    # ---------------------------
    # Job Recommendations
    # ---------------------------
    st.subheader("🎯 Top Job Matches")
    top_matches = recommend_jobs(model, summary_text, jobs)

    if top_matches:
        for job in top_matches:
            with st.container():
                st.markdown(f"### 🏢 {job['company']} (Score: {job['similarity']:.2f})")
                st.write(f"**📌 Role:** {job['job_description']}")
                st.write(f"**🛠 Skills Needed:** {', '.join(job['skills_needed'])}")
                st.markdown("---")
    else:
        st.warning("No job matches found.")


    # ---------------------------
    # Skills & Domain Analysis
    # ---------------------------
    st.subheader("🧠 Skills & Domain Analysis")

    def plot_skill_distribution(distribution, title):
        """Create a thick stacked horizontal bar with value annotations."""
        if not distribution:
            st.info("No domain matches found.")
            return

        # Sort domains by percentage descending
        sorted_dist = dict(sorted(distribution.items(), key=lambda x: x[1], reverse=True))
        colors = px.colors.qualitative.Vivid
        if len(sorted_dist) > len(colors):
            colors *= (len(sorted_dist) // len(colors)) + 1  # repeat if needed

        # Create stacked horizontal bar
        fig = go.Figure()
        for i, (label, val) in enumerate(sorted_dist.items()):
            fig.add_trace(go.Bar(
                x=[val],
                y=["Experience"],
                orientation="h",
                name=f"{label}",
                marker=dict(color=colors[i]),
                hovertemplate=f"<b>{label}</b><br>Percentage: {val:.1f}%<extra></extra>",
                text=f"{val:.1f}%",
                textposition="inside",
                insidetextanchor="middle"
            ))

        fig.update_layout(
            barmode="stack",
            title=dict(text=title, x=0.5),
            xaxis=dict(title="Percentage", range=[0, 100], showgrid=False, zeroline=False),
            yaxis=dict(showticklabels=False),
            height=220,  # thicker bar
            bargap=0.05,
            legend=dict(orientation="h", y=-0.3, x=0),
            margin=dict(l=20, r=20, t=40, b=80),
        )
        st.plotly_chart(fig, use_container_width=True)


    def show_matched_skills(matches):
        """Show matched sub-skills for each domain in a clean UI list."""
        if not matches:
            return
        for domain, subs in sorted(matches.items(), key=lambda x: x[0]):
            skills_list = ", ".join([f"{s} ({score:.2f})" for s, score in subs])
            st.markdown(f"**{domain}:** {skills_list}")


    # 🔹 Experience + Projects Distribution
    matches_exp, dist_exp = find_skills_and_distribution(model, full_summary, domains, "Experience + Projects")
    plot_skill_distribution(dist_exp, "Domain Distribution (Experience + Projects)")
    show_matched_skills(matches_exp)  # ➡️ NEW: show matched sub-skills

    # 🔹 Projects Only Distribution
    matches_proj, dist_proj = find_skills_and_distribution(model, project_text_combined, domains, "Projects")
    plot_skill_distribution(dist_proj, "Domain Distribution (Projects Only)")
    show_matched_skills(matches_proj)  # ➡️ NEW: show matched sub-skills

else:
    st.info("👆 Upload a resume to start the AI analysis.")
