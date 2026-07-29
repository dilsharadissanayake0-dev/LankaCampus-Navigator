# 🎓 LankaCampus Navigator

An AI-Powered Multi-Agent System designed to guide Sri Lankan A/L students in finding eligible state university degree programs and providing strategic career guidance based on UGC guidelines.

---

## 📌 Section 1: Overview & Problem Statement
Every year, thousands of Sri Lankan G.C.E. Advanced Level students struggle to navigate the complex University Grants Commission (UGC) handbook to identify degree programs matching their Z-scores and streams. **LankaCampus Navigator** addresses this challenge by providing an automated, dual-agent AI assistant that accurately evaluates university cut-off marks and offers tailored career advice.

---

## 🏛️ Section 2: System Architecture

```mermaid
graph TD
    User([🎓 A/L Student]) -->|Inputs Z-Score, Stream, District| UI[💻 Streamlit Web Application]
    UI -->|Triggers Pipeline| AgentPipe[⚙️ Multi-Agent Orchestrator]
    
    subgraph Multi-Agent RAG System
        Agent1[🤖 Agent 1: Eligibility & Cut-Off Agent]
        Agent2[🤖 Agent 2: Course & Career Advisor Agent]
        VS[(🗄️ ChromaDB Vector Store)]
        LLM[🧠 Groq Llama-3.3 LLM]
        
        AgentPipe --> Agent1
        Agent1 -->|Similarity Search| VS
        VS -->|Contextual UGC Data| Agent1
        Agent1 -->|Passes Eligible Courses| Agent2
        Agent1 <--> LLM
        Agent2 <--> LLM
    end
    
    Agent2 -->|Returns Final Guidance & Strategy| UI
🔄 Section 3: Agentic Workflows & Communication
The application implements two distinct AI agents that interact sequentially to deliver results:

Eligibility & Cut-Off Agent (Tool-Use / ReAct Pattern):

Performs semantic similarity searches over the ChromaDB vector database using the student's profile (Z-Score, Stream, District).

Filters out non-eligible courses and outputs a structured list of state university options with exact cut-off comparisons.

Course & Career Advisor Agent (Synthesis Pattern):

Receives the output stream directly from the Eligibility Agent.

Synthesizes career pathways, highlights key subject modules, and alerts students about mandatory university Aptitude Tests (e.g., Architecture, Translation Studies).

🛠️ Section 4: Tech Stack & Tools Used
AI & Agentic Framework: LangChain, Multi-Agent Communication Architecture

Large Language Model (LLM): Groq API (llama-3.3-70b-versatile)

Vector Database & Embeddings: ChromaDB & FastEmbed (BAAI/bge-small-en-v1.5)

Frontend Web Framework: Streamlit

Version Control: Git & GitHub (Branching & PR Workflow)

🚀 Section 5: Installation & Setup Guide
1. Prerequisites
Python 3.10+ installed

Active Groq API Key

2. Repository Cloning & Environment Setup
Bash
# Clone the repository
git clone [https://github.com/dilsharadissanayake0-dev/LankaCampus-Navigator.git](https://github.com/dilsharadissanayake0-dev/LankaCampus-Navigator.git)
cd LankaCampus-Navigator

# Install dependencies
pip install -r requirements.txt
3. Environment Variables Configuration
Create a .env file in the root directory:

Code snippet
GROQ_API_KEY=your_actual_groq_api_key_here
🏃 Section 6: Usage & Execution Instructions
Follow these commands in order to execute the RAG pipeline and launch the application:

Generate UGC Knowledge Corpus:

Bash
python src/generate_docs.py
Build Knowledge Base (ChromaDB Ingestion):

Bash
python src/rag_pipeline.py
Launch Streamlit Web UI:

Bash
python -m streamlit run app.py
🧪 Section 7: Sample Test Case & Output Verification
Input Profile: Z-Score: 1.75 | Stream: Physical Science | District: Colombo

Expected Output:

Agent 1: Identifies eligibility for degrees such as BSc in Software Engineering (Kelaniya) and Applied Sciences (Jayewardenepura).

Agent 2: Provides career advice for Software Engineering (DevOps, Full Stack Roles) and highlights application preference ordering strategies.