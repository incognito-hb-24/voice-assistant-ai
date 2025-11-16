import re

def parse(text):
    text = text.lower().strip()

    if "balance" in text:
        return {"intent": "check_balance", "entities": {}, "risk": "low"}

    if "transaction" in text or "transactions" in text:
        count = 5
        m = re.search(r"last\s+(\d+)", text)
        if m:
            count = int(m.group(1))
        return {"intent": "get_transactions", "entities": {"count": count}, "risk": "low"}

    if "send" in text or "transfer" in text or "pay" in text:
        amt_match = re.search(r"(\d+[,.]?\d*)", text)
        amount = float(amt_match.group(1)) if amt_match else 0.0
        payee = None
        p = re.search(r"to\s+([a-zA-Z]+)", text)
        if p:
            payee = p.group(1).capitalize()
        risk = "high" if amount >= 1000 else "medium"
        return {"intent": "transfer", "entities": {"amount": amount, "payee": payee}, "risk": risk}

    if "loan" in text or "interest" in text:
        if "personal" in text:
            return {"intent": "loan_rate", "entities": {"loan_type": "personal_loan"}, "risk": "low"}
        if "home" in text:
            return {"intent": "loan_rate", "entities": {"loan_type": "home_loan"}, "risk": "low"}
        if "car" in text:
            return {"intent": "loan_rate", "entities": {"loan_type": "car_loan"}, "risk": "low"}
        return {"intent": "loan_rate", "entities": {"loan_type": None}, "risk": "low"}

    if "spend" in text or "spent" in text:
        category = None
        for cat in ["food", "shopping", "utilities", "travel", "entertainment"]:
            if cat in text:
                category = cat
                break
        return {"intent": "spend_insight", "entities": {"category": category}, "risk": "low"}

    if "remind" in text or "reminder" in text:
        return {"intent": "set_reminder", "entities": {}, "risk": "low"}

    return {"intent": "fallback", "entities": {}, "risk": "low"}
