def format_currency(amount):
    if amount is None:
        return "0.00"
    return f"{amount:,.2f}"


def mask_account(account_id):
    if not account_id:
        return ""
    if len(account_id) <= 4:
        return account_id
    return "XXXX" + account_id[-4:]


def is_valid_otp(otp_text, expected="123456"):
    if not otp_text:
        return False
    return otp_text.strip() == expected
