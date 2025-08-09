# EduGenAI  
**A Dual-Agent AI Platform for Teachers and Students**  

EduGenAI is a conversational AI-powered educational platform that replaces multiple complex education portals with a **single agentic interface**.  
It leverages **LangChain**, **FastAPI**, **MongoDB**, **Google Cloud Storage**, and modern **LLMs** to automate content creation, grading, and academic communication.  

---

## 🚀 Features  

### Teacher Agent  
- Generate MCQs, summaries, and notes directly from uploaded PDFs.  
- Create assignments and share unique test links.  
- Evaluate tests via rubric-aware grading in conversation.  
- Upload course materials to the cloud through chat.  
- Create and post course announcements instantly.  

### Student Agent  
- Access course materials and assignments.  
- Take and submit MCQ tests through the chatbot or dashboard.  
- Get instant grades and detailed feedback.  
- Retrieve performance reports and academic details.  

---

## 🏗 System Architecture  

![System Architecture Diagram](docs/system-architecture.png)  

**Components**:  
- **Frontend (React.js)**: Teacher and student dashboards with embedded conversational agent.  
- **Backend (FastAPI)**: Endpoints for file upload, conversation handling, MCQ management, grading, and content management.  
- **LangChain Agents**:  
  - Teacher Agent Tools: PDF → Images → OCR → MCQ generation → Save to DB, plus announcements & uploads.  
  - Student Agent Tools: Get MCQs, Evaluate Tests, Get Grades, Get Student Details.  
- **External Services**:  
  - Google Cloud Storage for file hosting.  
  - MongoDB for persistence.  
  - OCR (Tesseract/PaddleOCR) for text extraction.  
  - LLMs (Groq API, DeepSeek R1, Meta-LLaMA) for content generation.  

---

