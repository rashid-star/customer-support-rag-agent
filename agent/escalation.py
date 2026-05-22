# agent/escalation.py


def should_escalate(response: str):

    """
    Detect low-confidence AI responses.
    """

    response = response.lower()


    low_confidence_phrases = [

        "i could not find enough information",

        "i do not have enough information",

        "unable to determine",

        "not enough information"
    ]


    for phrase in low_confidence_phrases:

        if phrase in response:
            return True


    return False


def classify_support_issue(query: str):

    """
    Detect customer issue category.
    """

    query = query.lower()


    payment_keywords = [

        "payment",
        "money deducted",
        "upi failed",
        "transaction failed",
        "refund not received"
    ]


    delivery_keywords = [

        "delivery",
        "shipment",
        "track order",
        "not delivered"
    ]


    account_keywords = [

        "password",
        "login",
        "account locked",
        "reset password"
    ]


    refund_keywords = [

        "refund",
        "return order",
        "cancel order"
    ]


    for keyword in payment_keywords:

        if keyword in query:
            return "payment"


    for keyword in delivery_keywords:

        if keyword in query:
            return "delivery"


    for keyword in account_keywords:

        if keyword in query:
            return "account"


    for keyword in refund_keywords:

        if keyword in query:
            return "refund"


    return "general"


def get_support_email(issue_type: str):

    """
    Return support email based on issue type.
    """

    support_emails = {

        "payment": "payments@company.com",

        "delivery": "delivery@company.com",

        "account": "accounts@company.com",

        "refund": "refunds@company.com",

        "general": "support@company.com"
    }


    return support_emails.get(
        issue_type,
        support_emails["general"]
    )


def generate_escalation_response(query: str):

    """
    Generate escalation response.
    """

    issue_type = classify_support_issue(query)


    support_email = get_support_email(issue_type)


    return {

        "answer": (

            "I could not fully resolve your request automatically.\n\n"

            "Please contact customer support through email:\n\n"

            f"{support_email}"
        ),

        "escalate": True
    }