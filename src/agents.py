import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings

# Environment variables load කිරීම (.env file එකෙන් API Key එක ගනී)
load_dotenv()

# 1. Groq LLM එක initialize කිරීම (ලොකු වේගයක් සහිත නොමිලේ ලබාදෙන Llama-3 Model එක)
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.3
)

# 2. Vector Store එක load කිරීම
embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

# -------------------------------------------------------------
# AGENT 1: Eligibility & Cut-Off Agent (Tool-Use / ReAct)
# -------------------------------------------------------------
def eligibility_agent(student_profile: str) -> str:
    """
    RAG Vector Store එක සෝදිසි කර ශිෂ්‍යයාට සුදුසු උපාධි පාඨමාලා ලැයිස්තුව සොයා දෙයි.
    """
    # Student Profile එකට අනුව Vector store එකෙන් ලඟම තොරතුරු 4ක් search කරයි
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
    Eligibility Agent ගෙන් ලැබෙන පාඨමාලා සඳහා Career Guidance, Modules, සහ Aptitude test උපදෙස් සකසයි.
    """
    prompt = f"""
    You are the 'Course & Career Advisor Agent' for Sri Lankan students.
    Take the following eligible course list provided by the Eligibility Agent and enhance it with practical guidance.
    
    Eligible Courses Info:
    {eligible_courses_info}
    
    Please provide:
    1. A summary of Career Opportunities for each degree course.
    2. Any special notes regarding mandatory Aptitude Tests if mentioned in the course info.
    3. Practical advice on how the student should order these in their UGC handbook application form.
    
    Keep the advice encouraging, structured, and easy to understand.
    """
    
    response = llm.invoke(prompt)
    return response.content

# -------------------------------------------------------------
# AGENT-TO-AGENT PIPELINE (Communication Flow)
# -------------------------------------------------------------
def run_lankacampus_navigator(z_score: str, stream: str, district: str) -> dict:
    student_profile = f"Z-Score: {z_score}, Stream: {stream}, District: {district}"
    
    print("🤖 Agent 1 (Eligibility Agent) is searching UGC database...")
    eligible_courses = eligibility_agent(student_profile)
    
    print("🤖 Agent 2 (Career Advisor Agent) is generating career advice...")
    career_guidance = career_advisor_agent(eligible_courses)
    
    return {
        "eligible_courses": eligible_courses,
        "career_guidance": career_guidance
    }

if __name__ == "__main__":
    # Local Testing
    result = run_lankacampus_navigator(z_score="1.75", stream="Physical Science", district="Colombo")
    print("\n--- ELIGIBILITY AGENT OUTPUT ---")
    print(result["eligible_courses"])
    print("\n--- CAREER ADVISOR AGENT OUTPUT ---")
    print(result["career_guidance"])