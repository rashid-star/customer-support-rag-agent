# agent/escalation.py


def should_escalate(response: str):

    """
    Detect whether AI response should
    be escalated to human support.
    """

    # convert response to lowercase
    response = response.lower()


    # low-confidence phrases
    low_confidence_phrases = [

        "i do not have enough information",

        "i cannot answer",

        "not available in the context",

        "i am not sure",

        "unable to determine",

        "please contact support",

        "human support",

        "unable to help"
    ]


    # check for escalation phrases
    for phrase in low_confidence_phrases:

        if phrase in response:

            return True


    return False


def classify_support_issue(query: str):

    """
    Classify customer issue type.

    Helps route issues properly.
    """

    query = query.lower()


    # =========================================
    # PAYMENT ISSUES
    # =========================================

    payment_keywords = [

        "payment failed",
        "payment declined",
        "money deducted",
        "money cut",
        "charged twice",
        "refund not received",
        "transaction failed",
        "bank charged",
        "upi failed"
    ]


    # =========================================
    # DELIVERY ISSUES
    # =========================================

    delivery_keywords = [

        "delivery delayed",
        "shipment delayed",
        "where is my order",
        "track order",
        "not delivered",
        "late delivery"
    ]


    # =========================================
    # ACCOUNT ISSUES
    # =========================================

    account_keywords = [

        "forgot password",
        "reset password",
        "login failed",
        "cannot login",
        "account locked",
        "account issue"
    ]


    # =========================================
    # REFUND ISSUES
    # =========================================

    refund_keywords = [

        "refund",
        "return order",
        "cancel order",
        "refund delayed"
    ]


    # detect payment issue
    for keyword in payment_keywords:

        if keyword in query:

            return "payment"


    # detect delivery issue
    for keyword in delivery_keywords:

        if keyword in query:

            return "delivery"


    # detect account issue
    for keyword in account_keywords:

        if keyword in query:

            return "account"


    # detect refund issue
    for keyword in refund_keywords:

        if keyword in query:

            return "refund"


    return "general"


def get_support_contact(issue_type: str):

    """
    Return support contact details
    based on issue category.
    """

    support_contacts = {

        "payment": {

            "team": "Payment Support Team",

            "phone": "+91-9876543210",

            "email": "payments@company.com",

            "priority": "high"
        },


        "delivery": {

            "team": "Delivery Support Team",

            "phone": "+91-9123456780",

            "email": "delivery@company.com",

            "priority": "medium"
        },


        "account": {

            "team": "Account Support Team",

            "phone": "+91-9988776655",

            "email": "accounts@company.com",

            "priority": "high"
        },


        "refund": {

            "team": "Refund Support Team",

            "phone": "+91-9876501234",

            "email": "refunds@company.com",

            "priority": "medium"
        },


        "general": {

            "team": "Customer Support Team",

            "phone": "+91-9000000000",

            "email": "support@company.com",

            "priority": "normal"
        }
    }


    return support_contacts.get(
        issue_type,
        support_contacts["general"]
    )


def generate_escalation_response(query: str):

    """
    Generate professional escalation response.
    """

    # classify issue
    issue_type = classify_support_issue(query)


    # fetch support details
    support_info = get_support_contact(issue_type)


    # build final response
    response = {

        "answer": (

            f"We were unable to fully resolve your issue automatically.\n\n"

            f"Your request has been forwarded to the "
            f"{support_info['team']}.\n\n"

            f"📞 Phone: {support_info['phone']}\n"

            f"📧 Email: {support_info['email']}\n\n"

            f"Priority Level: {support_info['priority'].upper()}"
        ),

        "escalate": True,

        "confidence": "low",

        "issue_type": issue_type,

        "support_team": support_info["team"],

        "priority": support_info["priority"]
    }


    return response