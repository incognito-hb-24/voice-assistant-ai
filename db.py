
import sqlite3
from pathlib import Path

DB_PATH = Path('/content/drive/MyDrive/Voice_Assistant_ai/voicebank.db')

def get_conn():
    return sqlite3.connect(DB_PATH)

# User
def fetch_user(user_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
    row = cur.fetchone()
    conn.close()
    return row

# Accounts
def fetch_account(account_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM accounts WHERE account_id=?', (account_id,))
    row = cur.fetchone()
    conn.close()
    return row

def update_balance(account_id, new_balance):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('UPDATE accounts SET balance=? WHERE account_id=?', (new_balance, account_id))
    conn.commit()
    conn.close()

# Transactions
def insert_transaction(txn_id, account_id, txn_type, amount, category, date):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?)',
        (txn_id, account_id, txn_type, amount, category, date)
    )
    conn.commit()
    conn.close()

def fetch_transactions(account_id, limit=5):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        'SELECT txn_id, type, amount, category, date FROM transactions WHERE account_id=? ORDER BY date DESC LIMIT ?',
        (account_id, limit)
    )
    rows = cur.fetchall()
    conn.close()
    return rows

def fetch_all_transactions(account_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        'SELECT txn_id, type, amount, category, date FROM transactions WHERE account_id=? ORDER BY date DESC',
        (account_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows

# Payees
def fetch_payee(payee_name):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT upi_id FROM payees WHERE payee_name=?', (payee_name,))
    row = cur.fetchone()
    conn.close()
    return row

# Loan interest rates
def fetch_loan_rate(loan_type):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT interest_rate FROM loan_rates WHERE loan_type=?', (loan_type,))
    row = cur.fetchone()
    conn.close()
    return row
