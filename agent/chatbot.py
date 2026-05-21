# agent/chatbot.py

import os

from dotenv import load_dotenv
from groq import Groq

# semantic retrieval
from agent.retriever import search_documents

# escalation checker
from agent.escalation import (should_escalate,generate_escalation_response)
# load environment variables
load_dotenv()


# initialize groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def build_context(documents):

    """
    Combine retrieved documents into one context block.
    """

    context = "\n\n".join(
        [doc["content"] for doc in documents]
    )

    return context


def detect_intent(query: str):

    """
    Detect special customer intents.

    This creates smarter chatbot behavior.
    """

    query = query.lower()


    # payment-related sensitive issues
    payment_issues = [

        "payment failed",
        "payment declined",
        "money deducted",
        "money cut",
        "charged twice",
        "refund not received",
        "transaction failed",
        "payment issue",
        "bank charged",
        "upi failed"
    ]


    # delivery/shipping issues
    shipping_issues = [

        "order not delivered",
        "delivery delayed",
        "shipment delayed",
        "track order",
        "where is my order"
    ]


    # account/login issues
    account_issues = [

        "reset password",
        "forgot password",
        "cannot login",
        "account locked",
        "login issue"
    ]


    # detect payment issue
    for issue in payment_issues:

        if issue in query:

            return "payment_issue"


    # detect shipping issue
    for issue in shipping_issues:

        if issue in query:

            return "shipping_issue"


    # detect account issue
    for issue in account_issues:

        if issue in query:

            return "account_issue"


    return "general"


def generate_response(query: str):

    """
    Main RAG pipeline.
    """

    # detect user intent
    intent = detect_intent(query)


    # =========================================
    # PAYMENT ISSUE
    # =========================================

    if intent == "payment_issue":

        return {

            "answer": (
                "I'm sorry for the inconvenience regarding your payment issue.\n\n"

                "Your payment may be under processing by the bank or payment gateway.\n\n"

                "Please wait a few minutes and check your bank statement.\n\n"

                "If the amount was deducted and the order was not confirmed, "
                "please contact customer support immediately.\n\n"

                "📞 Customer Care: +91-9876543210\n"
                "📧 Email: support@company.com"
            ),

            "escalate": True,

            "confidence": "high"
        }


    # =========================================
    # SHIPPING ISSUE
    # =========================================

    if intent == "shipping_issue":

        return {

            "answer": (
                "I understand your concern regarding delivery/shipping.\n\n"

                "Please check your order tracking details in your account.\n\n"

                "If your shipment is delayed beyond the expected delivery date, "
                "please contact customer support.\n\n"

                "📞 Support: +91-9876543210"
            ),

            "escalate": False,

            "confidence": "high"
        }


    # =========================================
    # ACCOUNT ISSUE
    # =========================================

    if intent == "account_issue":

        return {

            "answer": (
                "It seems you are facing an account or login issue.\n\n"

                "Please try using the 'Forgot Password' option on the login page.\n\n"

                "If the issue continues, contact account support.\n\n"

                "📞 Account Support: +91-9876543210\n"
                "📧 Email: support@company.com"
            ),

            "escalate": True,

            "confidence": "high"
        }


    # =========================================
    # RAG PIPELINE
    # =========================================

    # retrieve documents
    documents = search_documents(query)


    # create context
    context = build_context(documents)


    # final prompt
    prompt = f"""
You are a professional customer support AI assistant.

Your job:
- Help users solve problems
- Answer professionally
- Be concise and clear
- Use ONLY provided context
- Do not hallucinate fake information

If the answer is unavailable in context,
say exactly:
"I do not have enough information to answer this."

CONTEXT:
{context}

USER QUESTION:
{query}

ANSWER:
"""


    # generate llm response
    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0
    )


    # extract final answer
    final_answer = response.choices[0].message.content


    # =========================================
    # ESCALATION CHECK
    # =========================================

    if should_escalate(final_answer):

        return generate_escalation_response(query)


    # =========================================
    # SUCCESS RESPONSE
    # =========================================

    return {

        "answer": final_answer,

        "escalate": False,

        "confidence": "high"
    }

# local terminal testing
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

        print("Confidence:", result["confidence"])