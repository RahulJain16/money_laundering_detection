import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def load_data(txn_filepath: str = "data/sample_transactions.csv",
              accounts_filepath: str = "data/sample_accounts.csv",
              num_records: int = 5000):
    """
    Load transactions and accounts if files exist, otherwise generate them.
    Returns: (transactions_df, accounts_df)
    """
    if os.path.exists(txn_filepath) and os.path.exists(accounts_filepath):
        transactions = pd.read_csv(txn_filepath)
        accounts = pd.read_csv(accounts_filepath)
    else:
        transactions, accounts = generate_sample_data(num_records)

    return transactions, accounts


def generate_sample_data(num_records: int = 5000):
    """
    Generate synthetic transaction + account dataset.
    """
    np.random.seed(42)

    # Generate accounts
    accounts = []
    for i in range(1, 101):
        acc = {
            "account_id": f"ACC{str(i).zfill(3)}",
            "customer_name": f"Customer_{i}",
            "country": random.choice(["India", "USA", "UK", "UAE", "Singapore"]),
            "risk_level": random.choice(["Low", "Medium", "High"])
        }
        accounts.append(acc)
    accounts_df = pd.DataFrame(accounts)

    # Generate transactions
    account_ids = accounts_df["account_id"].tolist()
    transaction_types = ["Transfer", "Cash Deposit", "Wire Transfer", "Purchase"]

    transactions = []
    start_date = datetime.now() - timedelta(days=180)

    for i in range(num_records):
        account_id = random.choice(account_ids)
        txn_type = random.choice(transaction_types)
        amount = round(np.random.exponential(scale=20000), 2)

        txn = {
            "transaction_id": f"TXN{str(i).zfill(7)}",
            "account_id": account_id,
            "amount": amount,
            "transaction_type": txn_type,
            "timestamp": start_date + timedelta(minutes=random.randint(0, 60*24*180)),
            "cash_transaction": txn_type == "Cash Deposit",
            "is_international": random.choice([True, False]),
            "is_suspicious": False
        }
        transactions.append(txn)

    transactions_df = pd.DataFrame(transactions)

    # ensure data folder exists
    os.makedirs("data", exist_ok=True)
    transactions_df.to_csv("data/sample_transactions.csv", index=False)
    accounts_df.to_csv("data/sample_accounts.csv", index=False)

    return transactions_df, accounts_df
