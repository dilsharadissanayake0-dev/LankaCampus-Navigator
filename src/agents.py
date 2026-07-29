import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings

# 1. Load environment variables from .env file
load_dotenv()

# Retrieve Groq API Key securely
groq_api_key = os.getenv("GROQ_API_KEY")

# 2. Initialize Groq LLM
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.3,
    groq_api_key=groq_api_key
)

# 3. Load Persistent Vector Store (ChromaDB)
embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

# -------------------------------------------------------------
# AGENT 1: Eligibility & Cut-Off Agent (Tool-Use / ReAct Pattern)
# -------------------------------------------------------------
def eligibility_agent(student_profile: str) -> str:
    """
    Searches the RAG Vector Store and determines the list of eligible degree programs.
    """
    # Retrieve top 4 relevant context documents from Vector Store
    docs = vectorstore.similarity_search(student_profile, k=4)
    retrieved_info = "\n\n".join([doc.page_content for doc in docs])
    
    prompt = f"""
    You are the 'Eligibility & Cut-Off Agent' for Sri Lankan State Universities.
    Based ONLY on the retrieved UGC handbook data below, identify and list the eligible degree programs for the student.
    
    Student Profile: {student_profile}
    
    Retrieved UGC Data:
    {retrieved_info}
    
    Provide a clear list of eligible courses with University Name, Course Name, and Minimum Z-Score required.
    """
    
    response = llm.invoke(prompt)
    return response.content

# -------------------------------------------------------------
# AGENT 2: Course & Career Advisor Agent (Synthesis Pattern)
# -------------------------------------------------------------
def career_advisor_agent(eligible_courses_info: str) -> str:
    """
    Provides strategic career advice based STRICTLY on the output of Agent 1.
    """
    prompt = f"""
    You are the 'Course & Career Advisor Agent' for Sri Lankan students.
    
    CRITICAL INSTRUCTIONS:
    - Strictly base your response ONLY on the eligible courses listed below provided by Agent 1.
    - NEVER invent, assume, or add hypothetical courses or Z-Scores.
    - NEVER mention 'UGC handbook data is not provided'. Treat the input as authentic and complete.

    --- ELIGIBLE COURSES FROM AGENT 1 ---
    {eligible_courses_info}
    -------------------------------------
    
    Based ONLY on the list above, provide:
    1. 🎯 **Career Opportunities**: A short summary for each eligible degree course mentioned above.
    2. 📝 **Aptitude Tests**: Highlight if any of the above courses require mandatory Aptitude Tests.
    3. 💡 **Application Guidance**: Practical advice on how the student should order these specific eligible courses in their UGC handbook application form.
    
    Keep the advice encouraging, structured, and easy to understand.
    """
    
    response = llm.invoke(prompt)
    return response.content

# -------------------------------------------------------------
# AGENT-TO-AGENT PIPELINE (Sequential Communication Flow)
# -------------------------------------------------------------
def run_lankacampus_navigator(z_score: str, stream: str, district: str) -> dict:
    """
    Orchestrates the sequential execution of Agent 1 and Agent 2.
    """
    student_profile = f"Z-Score: {z_score}, Stream: {stream}, District: {district}"
    
    # Step 1: Execute Eligibility Agent
    eligible_courses = eligibility_agent(student_profile)
    
    # Step 2: Pass Agent 1 output directly to Career Advisor Agent
    career_guidance = career_advisor_agent(eligible_courses)
    
    return {
        "eligible_courses": eligible_courses,
        "career_guidance": career_guidance
    }

if __name__ == "__main__":
    # Local Testing Execution
    result = run_lankacampus_navigator(z_score="1.75", stream="Physical Science", district="Colombo")
    print("\n--- ELIGIBILITY AGENT OUTPUT ---")
    print(result["eligible_courses"])
    print("\n--- CAREER ADVISOR AGENT OUTPUT ---")
    print(result["career_guidance"])