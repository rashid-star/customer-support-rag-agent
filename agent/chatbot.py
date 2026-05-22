# agent/chatbot.py

import os

from dotenv import load_dotenv
from groq import Groq

from agent.retriever import search_documents
from agent.escalation import should_escalate


# load environment variables
load_dotenv()


# initialize groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def build_context(documents):

    """
    Convert retrieved documents into clean context.
    """

    context_parts = []


    for doc in documents:

        content = doc["content"]


        # skip noisy or broken text
        if "{{" in content:
            continue


        # skip empty content
        if len(content.strip()) < 20:
            continue


        context_parts.append(content)


    return "\n\n".join(context_parts)


def is_simple_query(query: str):

    """
    Simple greetings or casual queries.
    LLM can answer these without retrieval.
    """

    query = query.lower().strip()


    simple_queries = [

        "hi",
        "hello",
        "hey",
        "good morning",
        "good evening",
        "how are you"
    ]


    return query in simple_queries


def is_support_query(query: str):

    """
    Detect customer support related queries.
    """

    query = query.lower()


    support_keywords = [

        "order",
        "cancel",
        "refund",
        "payment",
        "delivery",
        "shipment",
        "track",
        "return",
        "account",
        "password",
        "login",
        "support"
    ]


    for keyword in support_keywords:

        if keyword in query:
            return True


    return False


def generate_llm_reply(query: str):

    """
    Generate normal conversational response.
    """

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a friendly and professional "
                    "customer support assistant."
                )
            },
            {
                "role": "user",
                "content": query
            }
        ],

        temperature=0.5
    )


    return response.choices[0].message.content.strip()


def generate_response(query: str):

    """
    Main chatbot workflow.
    """


    # =====================================
    # SIMPLE GREETINGS
    # =====================================

    if is_simple_query(query):

        answer = generate_llm_reply(query)

        return {

            "answer": answer,

            "escalate": False
        }


    # =====================================
    # OUT OF SCOPE QUESTIONS
    # =====================================

    if not is_support_query(query):

        return {

            "answer": (
                "I'm designed to assist with customer support related questions "
                "such as orders, payments, refunds, delivery, and account issues."
            ),

            "escalate": False
        }


    # =====================================
    # RETRIEVE RELEVANT DOCUMENTS
    # =====================================

    documents = search_documents(query)


    # no relevant retrieval
    if not documents:

        return {

            "answer": (
                "I could not find enough information to help with your request.\n\n"
                "Please contact support through email:\n"
                "support@company.com"
            ),

            "escalate": True
        }


    # build clean context
    context = build_context(documents)


    # =====================================
    # FINAL RAG PROMPT
    # =====================================

    prompt = f"""
You are a professional customer support assistant.

Instructions:
- Give short and clear answers
- Answer naturally like a real support assistant
- Summarize information instead of copying raw text
- Do not mention placeholders or broken text
- Do not generate fake information
- Stay professional and helpful

If answer is not available,
say:
"I could not find enough information regarding your request."

CONTEXT:
{context}

USER QUESTION:
{query}

ANSWER:
"""


    # =====================================
    # GENERATE FINAL RESPONSE
    # =====================================

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.3
    )


    final_answer = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )


    # =====================================
    # ESCALATION CHECK
    # =====================================

    if should_escalate(final_answer):

        return {

            "answer": (
                "I could not fully resolve your request automatically.\n\n"
                "Please contact customer support through email:\n"
                "support@company.com"
            ),

            "escalate": True
        }


    # =====================================
    # SUCCESS RESPONSE
    # =====================================

    return {

        "answer": final_answer,

        "escalate": False
    }


# local testing
if __name__ == "__main__":

    while True:

        query = input("\nAsk Question: ")


        if query.lower() == "exit":
            break


        result = generate_response(query)


        print("\n" + "=" * 50)
        print("AI RESPONSE")
        print("=" * 50)

        print(result["answer"])

        print("\nEscalate:", result["escalate"])