# frontend/app.py

import streamlit as st
import requests


# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(

    page_title="Customer Support AI Agent",

    page_icon="🤖",

    layout="centered"
)


# =====================================
# COMPANY HEADER
# =====================================

col1, col2 = st.columns([1, 4])


with col1:

    # company logo
    st.image(
        "frontend/nine a logo.svg",
        width=80
    )


with col2:

    st.title("Customer Support AI Agent")

    st.caption(
        "9A Business Pvt. Ltd."
    )


# =====================================
# SUBTITLE
# =====================================

st.markdown(
    """
Ask customer support related questions like:

- Cancel order
- Refund issue
- Payment failed
- Delivery delay
- Reset password
"""
)


# backend api
API_URL = "http://127.0.0.1:8000/chat"


# =====================================
# CHAT HISTORY
# =====================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# show old messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# =====================================
# USER INPUT
# =====================================

user_query = st.chat_input(
    "Type your question..."
)


# =====================================
# PROCESS USER MESSAGE
# =====================================

if user_query:


    # save user message
    st.session_state.messages.append({

        "role": "user",

        "content": user_query
    })


    # show user message
    with st.chat_message("user"):

        st.markdown(user_query)


    # assistant response
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


                # convert response json
                data = response.json()


                ai_answer = data["answer"]

                escalate = data["escalate"]


            except Exception as e:

                ai_answer = (
                    f"Backend Connection Error:\n\n{e}"
                )

                escalate = False


        # show ai answer
        st.markdown(ai_answer)


        # escalation warning
        if escalate:

            st.warning(
                "This request has been escalated to customer support."
            )


    # save assistant message
    st.session_state.messages.append({

        "role": "assistant",

        "content": ai_answer
    })