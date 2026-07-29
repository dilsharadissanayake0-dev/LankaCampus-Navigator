import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.3,
    groq_api_key=groq_api_key
)

# Absolute path resolution to project root's chroma_db
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
CHROMA_DIR = os.path.join(PROJECT_ROOT, "chroma_db")


def eligibility_agent(student_profile: str) -> str:
    """
    Searches the RAG Vector Store and determines the list of eligible degree programs.
    """
    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )

    docs = vectorstore.similarity_search(student_profile, k=6)
    retrieved_context = "\n\n".join([f"Document Content:\n{doc.page_content}" for doc in docs])
    
    prompt = f"""
    You are the official 'Eligibility & Cut-Off Agent' for Sri Lankan State Universities.
    
    CRITICAL INSTRUCTION:
    Use the following retrieved UGC Handbook Context to analyze and state the eligible degree programs.
    Do NOT state that data is missing.

    ===================================================
    RETRIEVED UGC HANDBOOK CONTEXT DATA:
    {retrieved_context}
    ===================================================

    Student Profile:
    {student_profile}

    Based on the context above, provide a clear, structured Markdown output:
    1. List the Eligible Degree Programs with Exact University Names and minimum Z-scores.
    2. Explicitly specify the University Name for each course (e.g., University of Colombo, University of Moratuwa).
    """
    
    response = llm.invoke(prompt)
    return response.content


def career_advisor_agent(eligible_courses_info: str) -> str:
    """
    Provides strategic career advice based STRICTLY on the output of Agent 1.
    """
    prompt = f"""
    You are the 'Course & Career Advisor Agent' for Sri Lankan students.
    
    CRITICAL INSTRUCTION:
    - Base your response ONLY on the eligible courses and university names provided by Agent 1 below.
    - NEVER say 'data is not available' or 'general outline'.
    - Mention the specific University Names and Degree Courses provided by Agent 1.

    ===================================================
    ELIGIBLE COURSES FROM AGENT 1:
    {eligible_courses_info}
    ===================================================

    Based on Agent 1's list above, provide:
    1. 🎯 **Career Opportunities**: Specific pathways for each degree/university mentioned.
    2. 📝 **Mandatory Aptitude Tests**: Highlight if any specific degree requires an aptitude test.
    3. 💡 **UGC Application Strategy**: How to prioritize these specific university options in the application form.
    """
    
    response = llm.invoke(prompt)
    return response.content


def run_lankacampus_navigator(z_score: str, stream: str, district: str) -> dict:
    student_profile = f"Stream: {stream}, District: {district}, Z-Score: {z_score}"
    
    eligible_courses = eligibility_agent(student_profile)
    career_guidance = career_advisor_agent(eligible_courses)
    
    return {
        "eligible_courses": eligible_courses,
        "career_guidance": career_guidance
    }