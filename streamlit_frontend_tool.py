import streamlit as st
import tempfile
import os

from langgraph_tool_backend import (
    chatbot,
    retrieve_all_threads,
    process_document
)

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage
)

import uuid

st.write("GROQ SECRET EXISTS:", "GROQ_API_KEY" in st.secrets)

# ============================================================
# Custom UI Styling
# ============================================================

st.markdown("""
<style>

/* ============================================================
   MAIN APP
   ============================================================ */

.stApp {
    background-color: #0f1117;
    color: #f5f7fa;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background-color: #151821;
    border-right: 1px solid #292d3a;
}


/* Sidebar normal text */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {
    color: #e5e7eb !important;
}


/* Sidebar headings */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
}


/* ============================================================
   MAIN TITLE
   ============================================================ */

.main-title {
    color: #ffffff !important;
    font-size: 34px;
    font-weight: 700;
    text-align: center;
    margin-top: 20px;
    margin-bottom: 5px;
}

.main-subtitle {
    color: #aab2c0 !important;
    font-size: 15px;
    text-align: center;
    margin-bottom: 30px;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    background-color: #1b1f2a !important;
    color: #ffffff !important;
    border: 1px solid #343a4a !important;
    border-radius: 10px !important;
}

.stButton > button:hover {
    background-color: #272d3d !important;
    color: #ffffff !important;
    border-color: #667eea !important;
}


/* ============================================================
   FILE UPLOADER
   ============================================================ */

[data-testid="stFileUploader"] {
    background-color: #1b1f2a !important;
    border-radius: 12px;
    padding: 8px;
}


/* File uploader text */
[data-testid="stFileUploader"] label {
    color: #ffffff !important;
}

[data-testid="stFileUploader"] section {
    background-color: #202531 !important;
    border: 1px dashed #4b5563 !important;
}

[data-testid="stFileUploader"] span {
    color: #e5e7eb !important;
}


/* ============================================================
   EXPANDERS
   ============================================================ */

[data-testid="stExpander"] {
    background-color: #191d27 !important;
    border: 1px solid #303544 !important;
    border-radius: 10px;
}

[data-testid="stExpander"] summary {
    color: #ffffff !important;
}

[data-testid="stExpander"] summary span {
    color: #ffffff !important;
}


/* ============================================================
   CHAT MESSAGE
   ============================================================ */

[data-testid="stChatMessage"] {
    border-radius: 14px;
    margin-bottom: 10px;
}


/* ============================================================
   CHAT INPUT
   ============================================================ */

[data-testid="stChatInput"] {
    background-color: #1b1f2a !important;
}

[data-testid="stChatInput"] textarea {
    color: #ffffff !important;
    background-color: #1b1f2a !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #9ca3af !important;
}


/* ============================================================
   STATUS / TOOL
   ============================================================ */

[data-testid="stStatusWidget"] {
    border-radius: 10px;
}


/* ============================================================
   DIVIDER
   ============================================================ */

hr {
    border-color: #292d3a !important;
}


/* ============================================================
   HIDE STREAMLIT BRANDING
   ============================================================ */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* ============================================================
   FIX CHAT TEXT VISIBILITY
   ============================================================ */

/* All chat text */
[data-testid="stChatMessage"] {
    color: #f5f7fa !important;
}

/* Markdown inside chat messages */
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] span,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li {
    color: #f5f7fa !important;
}

/* Headings inside assistant responses */
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3,
[data-testid="stChatMessage"] h4,
[data-testid="stChatMessage"] h5,
[data-testid="stChatMessage"] h6 {
    color: #ffffff !important;
}

/* Bold text */
[data-testid="stChatMessage"] strong {
    color: #ffffff !important;
}

/* Tables inside assistant responses */
[data-testid="stChatMessage"] table {
    color: #f5f7fa !important;
    border-color: #343a4a !important;
}

[data-testid="stChatMessage"] th {
    color: #ffffff !important;
    background-color: #1b1f2a !important;
}

[data-testid="stChatMessage"] td {
    color: #e5e7eb !important;
    border-color: #343a4a !important;
}

/* Code blocks */
[data-testid="stChatMessage"] code {
    color: #f5f7fa !important;
}

/* User message text */
[data-testid="stChatMessage"] p {
    color: #f5f7fa !important;
}


/* ============================================================
   MAIN PAGE MARKDOWN
   ============================================================ */

.main .stMarkdown p {
    color: #e5e7eb !important;
}

.main .stMarkdown h1,
.main .stMarkdown h2,
.main .stMarkdown h3 {
    color: #ffffff !important;
}

/* Chat input text */
[data-testid="stChatInput"] textarea {
    color: #ffffff !important;
    caret-color: #ffffff !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #9ca3af !important;
}


</style>
""", unsafe_allow_html=True)


# ============================================================
# Utility Functions
# ============================================================

def generate_thread_id():
    return str(uuid.uuid4())


def reset_chat():

    thread_id = generate_thread_id()

    st.session_state["thread_id"] = thread_id

    add_thread(thread_id)

    st.session_state["message_history"] = []


def add_thread(thread_id):

    if thread_id not in st.session_state["chat_threads"]:

        st.session_state["chat_threads"].append(thread_id)


def load_conversation(thread_id):

    state = chatbot.get_state(
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    return state.values.get("messages", [])


def get_conversation_title(thread_id):
    """
    Get the first user message and use it
    as the conversation title.
    """

    messages = load_conversation(thread_id)

    for msg in messages:

        if isinstance(msg, HumanMessage):

            title = msg.content.strip()

            if title:

                if len(title) > 35:
                    title = title[:35] + "..."

                return title

    return "New Chat"


# ============================================================
# Session Setup
# ============================================================

if "message_history" not in st.session_state:

    st.session_state["message_history"] = []


if "thread_id" not in st.session_state:

    st.session_state["thread_id"] = generate_thread_id()


if "chat_threads" not in st.session_state:

    st.session_state["chat_threads"] = retrieve_all_threads()


add_thread(st.session_state["thread_id"])


# ============================================================
# Sidebar UI
# ============================================================

st.sidebar.markdown(
    """
    <h2 style="margin-bottom:0;">
        🤖 Agentic AI
    </h2>
    <p style="color:#9ca3af; margin-top:4px;">
        Multi-tool AI Assistant
    </p>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# New Chat
# ------------------------------------------------------------

if st.sidebar.button("➕ New Chat"):

    reset_chat()

    st.rerun()



# ============================================================
# Document RAG
# ============================================================

st.sidebar.header("📚 Document RAG")


uploaded_file = st.sidebar.file_uploader(
    "📄 Upload Document",
    type=["pdf", "docx"],
    help="Upload a PDF or DOCX document for RAG."
)


if uploaded_file is not None:

    st.sidebar.success(
        f"📄 {uploaded_file.name}"
    )


    # --------------------------------------------------------
    # Process Document
    # --------------------------------------------------------

    if st.sidebar.button(
        "🔄 Process Document",
        use_container_width=True
    ):

        try:

            # Create temporary file
            suffix = os.path.splitext(
                uploaded_file.name
            )[1]

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix
            ) as tmp_file:

                tmp_file.write(
                    uploaded_file.getbuffer()
                )

                temp_file_path = tmp_file.name


            # Process document
            with st.sidebar.status(
                "Processing document...",
                expanded=True
            ):

                result = process_document(
                    temp_file_path,
                    uploaded_file.name
                )

                st.write(
                    f"📄 Pages: {result['pages']}"
                )

                st.write(
                    f"🧩 Chunks: {result['chunks']}"
                )

                st.write(
                    "🔎 Creating FAISS index..."
                )


            # Store document information
            st.session_state[
                "current_document"
            ] = uploaded_file.name


            st.sidebar.success(
                "✅ Document processed successfully!"
            )


            # Remove temporary file
            os.remove(
                temp_file_path
            )


        except Exception as e:

            st.sidebar.error(
                f"❌ Error: {str(e)}"
            )


    # --------------------------------------------------------
    # Summarize Document
    # --------------------------------------------------------

    if st.sidebar.button(
        "📝 Summarize Document",
        use_container_width=True
    ):

        st.sidebar.info(
            "Document summarization will be connected next."
        )


# ============================================================
# What Can I Ask?
# ============================================================

st.sidebar.header(" What can I ask?")


with st.sidebar.expander(" Calculator"):

    st.markdown("""
    **Examples:**
    
    • What is 125 × 48?
    
    • Calculate √144
    """)


with st.sidebar.expander(" Web Search"):

    st.markdown("""
    **Examples:**
    
    • What is the latest AI news?

    • Search for recent developments in LLMs.
    """)


with st.sidebar.expander(" Stock Price"):

    st.markdown("""
    **Examples:**
    • What's NVIDIA's latest stock price?
    
    • Give me today's Microsoft stock price.
    """)


with st.sidebar.expander(" Document RAG"):

    st.markdown("""
    **Upload and process a PDF/DOCX first.**
    
    **Examples:**
    • Explain KNN from the document.
    
    • What is the main idea of this document?
    
    • Explain this topic using the document.
    """)


with st.sidebar.expander(" General Chat"):

    st.markdown("""
    You can also ask general questions.
    
    **Examples:**
    • Explain CNN architecture.
    
    • Help me understand Python.
    """)




# ------------------------------------------------------------
# Previous Conversations
# ------------------------------------------------------------

st.sidebar.header("My Conversations")


for thread_id in st.session_state["chat_threads"][::-1]:

    # Get meaningful title
    title = get_conversation_title(thread_id)

    # Show title to user
    # Keep thread_id internally as the button key
    if st.sidebar.button(
        title,
        key=f"thread_{thread_id}"
    ):

        st.session_state["thread_id"] = thread_id

        messages = load_conversation(thread_id)

        temp_messages = []

        for msg in messages:

            if isinstance(msg, HumanMessage):

                role = "user"

            elif isinstance(msg, AIMessage):

                role = "assistant"

            else:

                # Ignore ToolMessage in chat history
                continue

            temp_messages.append({
                "role": role,
                "content": msg.content
            })

        st.session_state["message_history"] = temp_messages

        st.rerun()


# ============================================================
# Main UI
# ============================================================

st.markdown(
    """
    <div class="main-title">
        🤖 Agentic AI Assistant
    </div>
    <div class="main-subtitle">
        Your intelligent multi-tool AI assistant
    </div>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# Display Conversation History
# ------------------------------------------------------------

for message in st.session_state["message_history"]:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# ============================================================
# User Input
# ============================================================

user_input = st.chat_input("Type here")


if user_input:

    # --------------------------------------------------------
    # Display User Message
    # --------------------------------------------------------

    st.session_state["message_history"].append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):

        st.write(user_input)


    # --------------------------------------------------------
    # LangGraph + LangSmith Configuration
    # --------------------------------------------------------

    CONFIG = {

        "configurable": {

            "thread_id": st.session_state["thread_id"]

        },

        "metadata": {

            "thread_id": st.session_state["thread_id"]

        },

        "run_name": "chat_turn",

    }


    # --------------------------------------------------------
    # Get AI Response
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        # Holder for the Streamlit status box
        status_holder = {
            "box": None
        }


        def ai_only_stream():

            """
            Stream LangGraph messages.

            ToolMessage:
                Show tool execution status.

            AIMessage:
                Stream only the assistant's response.
            """

            for message_chunk, metadata in chatbot.stream(

                {
                    "messages": [
                        HumanMessage(content=user_input)
                    ]
                },

                config=CONFIG,

                stream_mode="messages"

            ):

                # ==================================================
                # TOOL MESSAGE
                # ==================================================

                if isinstance(message_chunk, ToolMessage):

                    tool_name = getattr(
                        message_chunk,
                        "name",
                        "tool"
                    )

                    # Create status box
                    if status_holder["box"] is None:

                        status_holder["box"] = st.status(
                            f"🔧 Using `{tool_name}`...",
                            expanded=True
                        )

                    # Update existing status box
                    else:

                        status_holder["box"].update(

                            label=f"🔧 Using `{tool_name}`...",

                            state="running",

                            expanded=True

                        )


                # ==================================================
                # AI MESSAGE
                # ==================================================

                elif isinstance(message_chunk, AIMessage):

                    # Only stream text generated by the AI
                    if message_chunk.content:

                        yield message_chunk.content


        # --------------------------------------------------------
        # Start Streaming
        # --------------------------------------------------------

        ai_message = st.write_stream(
            ai_only_stream()
        )


        # --------------------------------------------------------
        # Tool Finished
        # --------------------------------------------------------

        if status_holder["box"] is not None:

            status_holder["box"].update(

                label="✅ Tool finished",

                state="complete",

                expanded=False

            )


    # --------------------------------------------------------
    # Save AI Response
    # --------------------------------------------------------

    st.session_state["message_history"].append({

        "role": "assistant",

        "content": ai_message

    })