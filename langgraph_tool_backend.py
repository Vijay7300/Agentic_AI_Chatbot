from langgraph.graph import StateGraph, START
from typing import TypedDict, Annotated
import atexit

from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    SystemMessage,
)

from langchain_groq import ChatGroq
from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from ddgs import DDGS
from langchain_core.tools import tool

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv

import math
import os
import requests
import streamlit as st



load_dotenv()



# LLM

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key and hasattr(st, "secrets"):
    groq_api_key = st.secrets.get("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY is not configured.")

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=groq_api_key,
    temperature=0
)


 # EXISTING TOOLS
@tool
def web_search(query: str) -> str:
    """
    Search the web using DuckDuckGo.

    Use this tool when the user needs current information
    that cannot be answered using another available tool.
    """

    try:

        results = DDGS().text(
            query,
            max_results=5
        )

        if not results:
            return "No search results found."

        output = []

        for result in results:

            output.append(
                f"Title: {result.get('title', '')}\n"
                f"URL: {result.get('href', '')}\n"
                f"Snippet: {result.get('body', '')}"
            )

        return "\n\n".join(output)

    except Exception as e:

        return f"Web search error: {str(e)}"




@tool
def calculator(
    first_num: float,
    second_num: float | None = None,
    operation: str = "add"
) -> dict:
    """
    Perform mathematical calculations.

    Supported operations:
    add, sub, mul, div,
    power, mod, floor_div,
    sqrt, abs,
    percentage,
    max, min, avg,
    log, ln,
    sin, cos, tan
    """
 
    if second_num is None:
        second_num = 0.0
    try:

        if operation == "add":
            result = first_num + second_num

        elif operation == "sub":
            result = first_num - second_num

        elif operation == "mul":
            result = first_num * second_num

        elif operation == "div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed"}

            result = first_num / second_num

        elif operation == "power":
            result = first_num ** second_num

        elif operation == "mod":
            if second_num == 0:
                return {"error": "Modulo by zero is not allowed"}

            result = first_num % second_num

        elif operation == "floor_div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed"}

            result = first_num // second_num

        elif operation == "sqrt":
            if first_num < 0:
                return {
                    "error": "Square root of a negative number is not real"
                }

            result = math.sqrt(first_num)

        elif operation == "abs":
            result = abs(first_num)

        elif operation == "percentage":
            result = (first_num / 100) * second_num

        elif operation == "max":
            result = max(first_num, second_num)

        elif operation == "min":
            result = min(first_num, second_num)

        elif operation == "avg":
            result = (first_num + second_num) / 2

        elif operation == "log":
            if first_num <= 0:
                return {
                    "error": "Logarithm requires a positive number"
                }

            result = math.log10(first_num)

        elif operation == "ln":
            if first_num <= 0:
                return {
                    "error": "Natural logarithm requires a positive number"
                }

            result = math.log(first_num)

        elif operation == "sin":
            result = math.sin(math.radians(first_num))

        elif operation == "cos":
            result = math.cos(math.radians(first_num))

        elif operation == "tan":
            result = math.tan(math.radians(first_num))

        else:
            return {
                "error": f"Unsupported operation '{operation}'"
            }

        return {
            "first_num": first_num,
            "second_num": second_num,
            "operation": operation,
            "result": result
        }

    except Exception as e:

        return {
            "error": str(e)
        }


@tool
def get_stock_price(symbol: str) -> dict:
    """
    Get the latest available stock quote.

    ALWAYS use this tool for:
    - current stock price
    - latest stock price
    - today's stock price
    - current market price
    """

    api_key = os.getenv("ALPHAVANTAGE_API_KEY")

    if not api_key:
        return {
            "error": "ALPHAVANTAGE_API_KEY is not configured"
        }

    url = (
        "https://www.alphavantage.co/query"
        f"?function=GLOBAL_QUOTE"
        f"&symbol={symbol.upper()}"
        f"&apikey={api_key}"
    )

    try:

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        return {
            "error": str(e)
        }


########### RAG - Parts

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5"
)



splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)



# Global Retriever

retriever = None
current_document = None



def process_document(file_path, file_name):
    """
    Load a PDF or DOCX document, split it into chunks,
    create embeddings, and build a FAISS vector store.
    """

    global retriever
    global current_document

    
    # Select Loader

    if file_name.lower().endswith(".pdf"):

        loader = PyPDFLoader(file_path)

    elif file_name.lower().endswith(".docx"):

        loader = Docx2txtLoader(file_path)

    else:

        raise ValueError(
            "Unsupported file type. "
            "Please upload PDF or DOCX."
        )


    docs = loader.load()


    chunks = splitter.split_documents(docs)


    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )


  
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 4
        }
    )


    current_document = file_name


    return {
        "file_name": file_name,
        "pages": len(docs),
        "chunks": len(chunks)
    }


# Default Test Document

try:

    process_document(
        "intro-to-ml.pdf",
        "intro-to-ml.pdf"
    )

except Exception:

    retriever = None
    current_document = None


# RAG Tool
@tool
def rag_tool(query: str) -> dict:
    """
    Retrieve relevant information from the currently
    processed document.

    Use this tool when the user's question requires
    information from the uploaded document.
    """

    if retriever is None:

        return {
            "error": (
                "No document has been processed yet. "
                "Please upload and process a PDF or DOCX document."
            )
        }


    result = retriever.invoke(query)


    context = [
        doc.page_content
        for doc in result
    ]


    metadata = [
        doc.metadata
        for doc in result
    ]


    return {
        "query": query,
        "document": current_document,
        "context": context,
        "metadata": metadata
    }


# ALL TOOLS

tools = [
    web_search,
    get_stock_price,
    calculator,
    rag_tool
]


llm_with_tools = llm.bind_tools(tools)


# STATE

class ChatState(TypedDict):

    messages: Annotated[
        list[BaseMessage],
        add_messages
    ]


# 6. CHAT NODE
def chat_node(state: ChatState):

    system_message = SystemMessage(
        content="""
You are a helpful AI assistant with access to several tools.

Tool usage rules:

1. If the user asks for a current, latest, today's,
   or real-time stock price, ALWAYS use get_stock_price.

2. Convert company names to ticker symbols when needed.

3. Do not answer current stock-price questions from
   your own knowledge.

4. Use calculator for mathematical calculations.

5. Use the web search tool when the user asks for
   current information that cannot be answered by
   another available tool.

6. Use rag_tool when the user's question is related
   to information contained in the uploaded PDF.

7. When using RAG, base the answer on the retrieved
   document context.

8. If the question does not require a tool, answer
   directly using your normal language-model knowledge.
"""
    )

    messages = [
        system_message
    ] + state["messages"]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }


# TOOL NODE

tool_node = ToolNode(tools)



# POSTGRESQL CHECKPOINTER


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not configured")


checkpointer_context = PostgresSaver.from_conn_string(
    DATABASE_URL
)

checkpointer = checkpointer_context.__enter__()


checkpointer.setup()


 
# LANGGRAPH


graph = StateGraph(ChatState)


graph.add_node(
    "chat_node",
    chat_node
)

graph.add_node(
    "tools",
    tool_node
)


graph.add_edge(
    START,
    "chat_node"
)


graph.add_conditional_edges(
    "chat_node",
    tools_condition
)


graph.add_edge(
    "tools",
    "chat_node"
)


chatbot = graph.compile(
    checkpointer=checkpointer
)


#  THREAD RETRIEVAL


def retrieve_all_threads():

    all_threads = set()

    for checkpoint in checkpointer.list(None):

        thread_id = checkpoint.config[
            "configurable"
        ]["thread_id"]

        all_threads.add(thread_id)

    return list(all_threads)



config = {
    "configurable": {
        "thread_id": "test-thread-1"
    }
}

result = chatbot.invoke(
    {
        "messages": [
            HumanMessage(
                content="According to the PDF, how do we choose the ideal value of K in KNN?"
            )
        ]
    },
    config=config
)

atexit.register(checkpointer_context.__exit__, None, None, None)

print(result["messages"][-1].content)