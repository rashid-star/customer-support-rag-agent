# frontend/app.py

import streamlit as st
import requests


# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(

    page_title="Customer Support AI Agent",

    page_icon="🤖",

    layout="centered"
)


# =========================================
# SIDEBAR
# =========================================

with st.sidebar:

    st.title("⚙️ System Info")

    st.markdown("""
    ### Features
    - RAG Chatbot
    - FAISS Retrieval
    - Escalation System
    - FastAPI Backend
    - Groq LLM
    """)

    st.markdown("---")

    st.success("Backend Connected")


# =========================================
# MAIN TITLE
# =========================================

st.title("🤖 Customer Support AI Agent")


st.markdown(
    """
Ask your customer support questions below.

Examples:
- Cancel my order
- Payment failed
- Refund issue
- Delivery delayed
"""
)


# =========================================
# BACKEND API
# =========================================

API_URL = "http://127.0.0.1:8000/chat"


# =========================================
# CHAT HISTORY
# =========================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# display old messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# =========================================
# USER INPUT
# =========================================

user_query = st.chat_input(
    "Type your question..."
)


# =========================================
# PROCESS USER MESSAGE
# =========================================

if user_query:

    # save user message
    st.session_state.messages.append({

        "role": "user",

        "content": user_query
    })


    # show user message
    with st.chat_message("user"):

        st.markdown(user_query)


    # assistant response area
    with st.chat_message("assistant"):

        # loading animation
        with st.spinner("Generating response..."):

            try:

                # send request to backend
                response = requests.post(

                    API_URL,

                    json={
                        "query": user_query
                    }
                )


                # parse response
                data = response.json()


                ai_answer = data["answer"]

                escalate = data["escalate"]

                confidence = data["confidence"]


            except Exception as e:

                ai_answer = (
                    f"Backend Connection Error:\n\n{e}"
                )

                escalate = False

                confidence = "unknown"


        # show ai answer
        st.markdown(ai_answer)


        # escalation warning
        if escalate:

            st.warning(
                "Escalated to Human Support"
            )


        # confidence badge
        if confidence == "high":

            st.success(
                f"Confidence: {confidence}"
            )

        else:

            st.error(
                f"Confidence: {confidence}"
            )


    # save assistant response
    st.session_state.messages.append({

        "role": "assistant",

        "content": ai_answer
    })