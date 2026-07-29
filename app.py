import streamlit as st
import sys
import os

# Append src directory to system path for modular imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import multi-agent pipeline orchestrator function
from src.agents import run_lankacampus_navigator

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
    
    # Sidebar Developer Information
    st.markdown("---")
    st.markdown("""
    ### 👨‍💻 Developed By
    **Dilshara Dissanayake** ITBIN-2313-0030  
    Intake 13
    """)

# 4. Main Processing & Sequential Agent Execution
if submit_btn:
    with st.spinner("🤖 Multi-Agent RAG Pipeline is analyzing UGC handbook data..."):
        try:
            # Execute sequential agent flow
            results = run_lankacampus_navigator(z_score=str(z_score), stream=stream, district=district)
            
            # Store responses in session state to persist across rerenders
            st.session_state['agent1_res'] = results["eligible_courses"]
            st.session_state['agent2_res'] = results["career_guidance"]
            st.success("Analysis Complete!")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# 5. Output Display Section using Streamlit Tabs
if 'agent1_res' in st.session_state and 'agent2_res' in st.session_state:
    
    # Create distinct view options using Tabs
    tab1, tab2 = st.tabs([
        "📌 Step 1: Eligible Degrees & Cut-Offs (Agent 1)", 
        "💡 Step 2: Strategic Career & Module Guidance (Agent 2)"
    ])
    
    # Tab 1: Agent 1 (Eligibility & Cut-Offs Output)
    with tab1:
        st.markdown("### 🤖 Agent 1: University Eligibility & Cut-Off Analysis")
        st.info("Searches UGC Database via ChromaDB RAG Vector Store based on Z-Score, Stream, and District.")
        st.markdown(st.session_state['agent1_res'])
        
    # Tab 2: Agent 2 (Career Advisor Output)
    with tab2:
        st.markdown("### 🤖 Agent 2: Course & Career Guidance Advisor")
        st.success("Synthesizes career pathways, subject modules, and mandatory aptitude test information.")
        st.markdown(st.session_state['agent2_res'])

else:
    # Initial Landing State Information
    st.info("👈 Fill in your A/L Stream, District, and Z-Score in the sidebar and click 'Find Eligible Degrees' to start.")