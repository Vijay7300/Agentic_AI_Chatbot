# Agentic_AI_Chatbot
Here is a **350-character GitHub description**:  > Agentic AI Chatbot built with LangGraph and Groq GPT-OSS-120B, featuring intelligent tool calling, web search, calculator, stock lookup, RAG with FAISS and BGE embeddings, PDF/DOCX processing, PostgreSQL memory, LangSmith tracing, and a modern Streamlit UI.

## 📌 Overview

This project is an Agentic AI chatbot designed to intelligently handle different types of user queries by selecting and using appropriate tools. Instead of relying only on the LLM, the chatbot can perform calculations, search the web, retrieve stock prices, and answer questions from uploaded documents using RAG.

The system also maintains persistent conversation state using PostgreSQL and provides LangSmith tracing for monitoring and debugging agent workflows.

---

## 🛠️ Tools & Capabilities

### 🤖 AI & Agent

- LangGraph Agentic Workflow
- Groq GPT-OSS-120B
- Intelligent Tool Calling
- LangSmith Tracing

### 🔧 Available Tools

- 🧮 Calculator
- 🌐 Web Search using DDGS
- 📈 Stock Price Lookup
- 📚 Document RAG

### 📄 Document Intelligence

- PDF / DOCX Upload
- Document Processing
- Text Chunking
- BGE-base-en-v1.5 Embeddings
- FAISS Vector Search
- Context-Aware Question Answering

### 🗄️ Memory & Storage

- PostgreSQL
- LangGraph PostgreSQL Checkpointer
- Persistent Conversation Threads

### 🖥️ Frontend

- Streamlit
- Interactive Chat Interface
- Tool Execution Status
- Conversation History
- Document Upload Interface

---

## 🔄 Workflow

```text
                    User Query
                        │
                        ▼
                 ┌─────────────┐
                 │  LangGraph  │
                 │    Agent    │
                 └──────┬──────┘
                        │
              ┌─────────┼─────────┐
              │         │         │
              ▼         ▼         ▼
          Calculator  Web Search  Stock
              │         │         │
              └─────────┼─────────┘
                        │
                        ▼
                    RAG Tool
                        │
                  FAISS Retriever
                        │
                 BGE Embeddings
                        │
                        ▼
                  Document Context
                        │
                        ▼
                 Groq GPT-OSS-120B
                        │
                        ▼
                   Final Answer
                        │
                        ▼
                   PostgreSQL
````

---

## 📊 Results / Demo

The chatbot successfully demonstrates:

* ✅ Multi-tool agentic conversations
* ✅ Automatic tool selection
* ✅ Mathematical calculations
* ✅ Web-based information retrieval
* ✅ Stock price retrieval
* ✅ PDF/DOCX-based question answering
* ✅ FAISS semantic search
* ✅ Persistent conversation history
* ✅ Streaming responses
* ✅ LangSmith workflow tracing
* ✅ Interactive Streamlit interface

### 🎥 Project Demo

<!-- Add your video link below -->

[![Agentic AI Chatbot Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

> Replace `YOUR_VIDEO_ID` with your YouTube video's ID.

---

## 💻 Technology Stack

| Category            | Technology            |
| ------------------- | --------------------- |
| LLM                 | Groq GPT-OSS-120B     |
| Agent Framework     | LangGraph             |
| LLM Framework       | LangChain             |
| Embeddings          | BAAI/bge-base-en-v1.5 |
| Vector Database     | FAISS                 |
| Database            | PostgreSQL            |
| Web Search          | DDGS                  |
| Frontend            | Streamlit             |
| Document Processing | PyPDF, Docx2txt       |
| Monitoring          | LangSmith             |
| Language            | Python                |

---

## 📂 Project Structure

```text
Agentic_AI_Chatbot/
│
├── langgraph_tool_backend.py
├── rag.py
├── streamlit_frontend_tool.py
├── requirements.txt
├── README.md
├── LICENSE
├── .env
└── venv/
```

> `.env` and `venv/` should not be committed to GitHub.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Vijay7300/Agentic_AI_Chatbot.git
cd Agentic_AI_Chatbot
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate environment

Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
ALPHAVANTAGE_API_KEY=your_alphavantage_api_key
DATABASE_URL=your_postgresql_connection_string
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=Agentic_AI_Chatbot
```

**Never upload `.env` to GitHub.**

---

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run streamlit_frontend_tool.py
```

The application will open at:

```text
http://localhost:8501
```

---

## 📚 RAG Pipeline

The document RAG pipeline follows:

```text
PDF / DOCX
     ↓
Document Loader
     ↓
Text Splitting
     ↓
BGE Embeddings
     ↓
FAISS Vector Store
     ↓
Similarity Retrieval
     ↓
Relevant Context
     ↓
Groq GPT-OSS-120B
     ↓
Answer
```

---

## 🚀 Future Improvements

* 📝 Advanced document summarization
* 🧠 Long-Term Memory using PostgreSQL
* 🖼️ Image understanding and OCR
* 📊 More external tools
* 🔐 User authentication
* ☁️ Cloud deployment
* ⚡ Performance optimization
* 📱 Responsive UI

---

## 👨‍💻 Author

**Vijay Prajapati**

M.Tech – Data & Computational Sciences
IIT Jodhpur

GitHub:
[https://github.com/Vijay7300](https://github.com/Vijay7300)

---

## 📅 Project Information

**Project:** Agentic AI Chatbot
**Author:** Vijay Prajapati
**Development:** 2026
**Status:** 🚧 Active Development

---

## 📄 License

This project is licensed under the MIT License.

````

### 🎥 About your video

If your video is on **YouTube**, replace:

```markdown
[![Agentic AI Chatbot Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)
````

with your actual YouTube video ID.

For example, if your video is:

```text
https://www.youtube.com/watch?v=AbCd1234
```

then use:

```markdown
[![Agentic AI Chatbot Demo](https://img.youtube.com/vi/AbCd1234/0.jpg)](https://www.youtube.com/watch?v=AbCd1234)
```

This gives your README a **clickable video thumbnail**, which looks much better than simply pasting a URL.

One thing I'd change in the above before you publish: **don't list "Long-Term Memory" as currently implemented yet**. Your current PostgreSQL setup is providing persistent LangGraph conversation/checkpoint state; the dedicated LTM feature is still a future improvement. That distinction will make your README technically accurate.
