import streamlit as st
import sys
import os

# Append src directory to system path for modular imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# --- EMBED API KEY FOR DEPLOYMENT ---
os.environ["GROQ_API_KEY"] = "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"
# ------------------------------------
# 1. Page Configuration Setup
st.set_page_config(
    page_title="LankaCampus Navigator",
    page_icon="🎓",
    layout="wide"
)

# 2. Application Header
st.title("🎓 LankaCampus Navigator")
st.caption("🚀 AI-Powered Dual-Agent University Admission & Career Guidance System")
st.markdown("---")

# 3. Sidebar - Student Inputs & Profile
with st.sidebar:
    st.header("📋 Student Profile")
    
    stream = st.selectbox(
        "Select A/L Stream:",
        ["Physical Science", "Biological Science", "Commerce", "Arts", "Technology"]
    )
    
    district = st.selectbox(
        "Select District:",
        ["Colombo", "Gampaha", "Kalutara", "Kandy", "Galle", "Matara", "Jaffna", "Kurunegala", "Other"]
    )
    
    z_score = st.number_input(
        "Enter Z-Score:",
        min_value=0.0,
        max_value=4.0,
        value=1.50,
        step=0.01
    )
    
    st.markdown("---")
    submit_btn = st.button("🔍 Find Eligible Degrees & Career Advice", use_container_width=True)
    


# 4. Main Processing & Sequential Agent Execution
if submit_btn:
    with st.spinner("🤖 Multi-Agent RAG Pipeline is analyzing UGC handbook data..."):
        try:
            from agents import run_lankacampus_navigator
            
            results = run_lankacampus_navigator(z_score=str(z_score), stream=stream, district=district)
            
            st.session_state['agent1_res'] = results["eligible_courses"]
            st.session_state['agent2_res'] = results["career_guidance"]
            st.success("Analysis Complete!")
        except Exception as e:
            st.error(f"An error occurred while connecting to database: {str(e)}")

# 5. Output Display Section using Streamlit Tabs
if 'agent1_res' in st.session_state and 'agent2_res' in st.session_state:
    
    tab1, tab2 = st.tabs([
        "📌 Step 1: Eligible Degrees & Cut-Offs (Agent 1)", 
        "💡 Step 2: Strategic Career & Module Guidance (Agent 2)"
    ])
    
    with tab1:
        st.markdown("### 🤖 Agent 1: University Eligibility & Cut-Off Analysis")
        st.info("Searches UGC Database via ChromaDB RAG Vector Store based on Z-Score, Stream, and District.")
        st.markdown(st.session_state['agent1_res'])
        
    with tab2:
        st.markdown("### 🤖 Agent 2: Course & Career Guidance Advisor")
        st.success("Synthesizes career pathways, subject modules, and mandatory aptitude test information.")
        st.markdown(st.session_state['agent2_res'])

else:
    st.info("👈 Fill in your A/L Stream, District, and Z-Score in the sidebar and click 'Find Eligible Degrees' to start.")