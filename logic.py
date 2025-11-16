from datetime import datetime
import time
import random
import string

import database as db


def generate_txn_id():
    now = int(time.time())
    rand = "".join(random.choices(string.ascii_uppercase, k=3))
    return f"TXN{now}{rand}"


def check_balance(account_id):
    acc = db.fetch_account(account_id)
    if not acc:
        return {"success": False, "message": "Account not found."}
    balance = acc[3]
    msg = f"Your current balance is {balance} rupees."
    return {"success": True, "message": msg, "balance": balance}


def get_transactions(account_id, count):
    rows = db.fetch_transactions(account_id, count)
    msg = f"Showing last {count} transactions."
    return {"success": True, "message": msg, "transactions": rows}


def loan_rate(loan_type):
    row = db.fetch_loan_rate(loan_type)
    if not row:
        return {"success": False, "message": "Loan type not found."}
    rate = row[0]
    msg = f"The interest rate for this loan is {rate} percent."
    return {"success": True, "message": msg, "rate": rate}


def spend_insight(account_id, category):
    rows = db.fetch_all_transactions(account_id)
    if category:
        rows = [r for r in rows if r[3] == category]
    total = sum([r[2] for r in rows if r[1] == "debit"])
    if category:
        msg = f"You have spent approximately {total} rupees on {category}."
    else:
        msg = f"Your total spending is approximately {total} rupees."
    return {"success": True, "message": msg, "total_spent": total}


def transfer(account_id, amount, payee_name, otp_verified):
    acc = db.fetch_account(account_id)
    if not acc:
        return {"success": False, "message": "Account not found."}

    balance = acc[3]
    if balance is None or balance < amount:
        return {"success": False, "message": "Insufficient balance."}

    payee = db.fetch_payee(payee_name)
    if not payee:
        return {"success": False, "message": "Payee not found in your saved list."}

    if not otp_verified:
        return {"success": False, "message": "OTP verification required."}

    new_balance = balance - amount
    db.update_balance(account_id, new_balance)

    txn_id = generate_txn_id()
    date = datetime.today().date().isoformat()
    db.insert_transaction(txn_id, account_id, "debit", amount, "transfer", date)

    msg = f"Transfer of {amount} rupees to {payee_name} completed."
    return {"success": True, "message": msg, "new_balance": new_balance}


def set_reminder():
    msg = "Reminder has been set successfully."
    return {"success": True, "message": msg}


def fallback():
    msg = "Sorry, I could not understand that. Please try again."
    return {"success": False, "message": msg}
