import streamlit as st
from src.agents import run_lankacampus_navigator

# Streamlit Page Configuration
st.set_page_config(
    page_title="LankaCampus Navigator",
    page_icon="🎓",
    layout="wide"
)

# App Title & Header
st.title("🎓 LankaCampus Navigator")
st.subheader("AI-Powered University Admission & Career Guidance System")
st.markdown("---")

# Sidebar - User Inputs
st.sidebar.header("📋 Student Profile Input")

stream = st.sidebar.selectbox(
    "Select your A/L Stream:",
    ["Physical Science", "Biological Science", "Commerce", "Arts", "Technology"]
)

district = st.sidebar.selectbox(
    "Select your District:",
    ["Colombo", "Gampaha", "Kalutara", "Kandy", "Matale", "Nuwara Eliya", 
     "Galle", "Matara", "Hambantota", "Jaffna", "Kurunegala", "Badulla", "Anuradhapura"]
)

z_score = st.sidebar.text_input("Enter your Z-Score:", value="1.75")

# Run Pipeline Button
if st.sidebar.button("🔍 Find Eligible Courses & Career Advice"):
    if not z_score:
        st.error("Please enter a valid Z-Score!")
    else:
        with st.spinner("🤖 Multi-Agent System is processing your request..."):
            try:
                # Call Agent Communication Pipeline
                results = run_lankacampus_navigator(
                    z_score=z_score,
                    stream=stream,
                    district=district
                )
                
                st.success("Analysis Complete!")
                
                # Layout Columns for Two Agents
                col1, col2 = st.columns(2)
                
                with col1:
                    st.header("📌 Agent 1: Eligibility & Cut-Offs")
                    st.info("Searches UGC Database via RAG Vector Store")
                    st.markdown(results["eligible_courses"])
                    
                with col2:
                    st.header("💡 Agent 2: Career & Course Advisor")
                    st.success("Synthesizes Guidance, Modules & Aptitude Info")
                    st.markdown(results["career_guidance"])
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.caption("Powered by LangChain, Groq LLM, ChromaDB & Streamlit | LankaCampus Navigator")