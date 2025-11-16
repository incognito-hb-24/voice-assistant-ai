
import streamlit as st
import pandas as pd

import nlu
import policy
import logic
import db
import utils

db.init_db()

DEFAULT_USER_ID = "u001"
DEFAULT_ACCOUNT_ID = "acc_sav_001"


def get_account_snapshot(account_id):
    row = db.fetch_account(account_id)
    if not row:
        return None
    return {
        "account_id": row[0],
        "user_id": row[1],
        "type": row[2],
        "balance": row[3],
        "credit_limit": row[4],
        "loan_status": row[5],
    }


def df_from_transactions(rows):
    if not rows:
        return pd.DataFrame(columns=["txn_id", "type", "amount", "category", "date"])
    return pd.DataFrame(rows, columns=["txn_id", "type", "amount", "category", "date"])


def main():
    st.set_page_config(page_title="AI Voice Assistant for Financial Operations", layout="wide")

    st.title("AI Voice Assistant for Financial Operations")
    st.caption("Prototype: text input simulates voice-to-text. Backed by SQLite and rule-based NLU.")

    col_main, col_side = st.columns([2, 1])

    with col_main:
        st.subheader("Command")

        sample = st.selectbox(
            "Sample commands",
            [
                "What is my balance?",
                "Show my last 5 transactions",
                "Send 1500 rupees to Ananya",
                "How much did I spend on food?",
                "What is the personal loan interest rate?",
                "Remind me two days before my credit card bill",
            ],
        )

        user_text = st.text_input("Enter your command", value=sample)

        st.markdown("Optional OTP (for high-value transfers). Use 123456 to approve.")
        otp_input = st.text_input("OTP", value="", type="password")

        if st.button("Run assistant"):
            if not user_text.strip():
                st.warning("Please enter a command.")
            else:
                parsed = nlu.parse(user_text)
                st.markdown("NLU Output")
                st.json(parsed)

                decision = policy.check(parsed["intent"], parsed["entities"], parsed["risk"])
                st.markdown("Policy decision")
                st.json(decision)

                if not decision["allowed"]:
                    st.error("Action blocked by policy.")
                    if decision["notes"]:
                        for note in decision["notes"]:
                            st.write("-", note)
                    return

                otp_verified = True
                if decision["step_up"]:
                    otp_verified = utils.is_valid_otp(otp_input)
                    if not otp_verified:
                        st.info("This action requires OTP. Enter 123456 and run again.")
                        return

                intent = parsed["intent"]
                entities = parsed["entities"]
                result = None

                if intent == "check_balance":
                    result = logic.check_balance(DEFAULT_ACCOUNT_ID)
                elif intent == "get_transactions":
                    count = entities.get("count", 5)
                    result = logic.get_transactions(DEFAULT_ACCOUNT_ID, count)
                elif intent == "transfer":
                    amount = entities.get("amount", 0)
                    payee = entities.get("payee")
                    result = logic.transfer(DEFAULT_ACCOUNT_ID, amount, payee, otp_verified)
                elif intent == "loan_rate":
                    loan_type = entities.get("loan_type")
                    if loan_type is None:
                        result = {"success": False, "message": "Specify a loan type such as personal, home, or car."}
                    else:
                        result = logic.loan_rate(loan_type)
                elif intent == "spend_insight":
                    category = entities.get("category")
                    result = logic.spend_insight(DEFAULT_ACCOUNT_ID, category)
                elif intent == "set_reminder":
                    result = logic.set_reminder()
                else:
                    result = logic.fallback()

                if result.get("success"):
                    st.success(result.get("message", ""))
                else:
                    st.error(result.get("message", ""))

                if intent in ["get_transactions", "transfer", "spend_insight"]:
                    tx_rows = db.fetch_transactions(DEFAULT_ACCOUNT_ID, limit=10)
                    st.markdown("Recent transactions")
                    st.dataframe(df_from_transactions(tx_rows))

    with col_side:
        st.subheader("Account snapshot")
        snapshot = get_account_snapshot(DEFAULT_ACCOUNT_ID)
        if snapshot:
            masked_acc = utils.mask_account(snapshot["account_id"])
            st.write("Account:", masked_acc)
            st.write("Type:", snapshot["type"])
            st.write("Balance:", utils.format_currency(snapshot["balance"]))
            if snapshot["credit_limit"] is not None:
                st.write("Credit limit:", utils.format_currency(snapshot["credit_limit"]))
            if snapshot["loan_status"]:
                st.write("Loan status:", snapshot["loan_status"])
        else:
            st.write("Account not found.")

        st.markdown("---")
        st.markdown("Quick test")
        tx_rows = db.fetch_transactions(DEFAULT_ACCOUNT_ID, limit=5)
        st.dataframe(df_from_transactions(tx_rows))


if __name__ == '__main__':
    main()
