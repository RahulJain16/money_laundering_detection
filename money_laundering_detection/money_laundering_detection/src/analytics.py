import pandas as pd

class AdvancedAnalytics:
    def __init__(self, transactions: pd.DataFrame, accounts: pd.DataFrame):
        """
        Initialize the Advanced Analytics module.
        
        :param transactions: Pandas DataFrame containing transaction data
        :param accounts: Pandas DataFrame containing account data
        """
        self.transactions = transactions
        self.accounts = accounts

    def run(self):
        """
        Run all advanced analytics checks.
        """
        print("\n📈 Running Advanced Analytics...")

        self.detect_high_risk_accounts()
        self.detect_frequent_transactions()
        self.detect_cross_border_transactions()

    def detect_high_risk_accounts(self):
        """
        Detect accounts with very large transactions.
        """
        high_risk_accounts = self.transactions[self.transactions["amount"] > 100000]["account_id"].unique()
        if len(high_risk_accounts) > 0:
            for acc in high_risk_accounts:
                print(f"⚠️ High-Risk Account Detected: {acc}")
        else:
            print("✅ No high-risk accounts detected.")

    def detect_frequent_transactions(self):
        """
        Detect accounts with unusually frequent transactions.
        """
        txn_counts = self.transactions["account_id"].value_counts()
        frequent_accounts = txn_counts[txn_counts > 5].index.tolist()

        if frequent_accounts:
            for acc in frequent_accounts:
                print(f"⚠️ Frequent Transactions Detected: {acc} ({txn_counts[acc]} transactions)")
        else:
            print("✅ No accounts with unusually frequent transactions.")

    def detect_cross_border_transactions(self):
        """
        Detect transactions marked as 'cross_border' (if such column exists).
        """
        if "type" in self.transactions.columns:
            cross_border_txns = self.transactions[self.transactions["type"] == "cross_border"]

            if not cross_border_txns.empty:
                for _, row in cross_border_txns.iterrows():
                    print(f"🌍 Cross-Border Transaction: Account {row['account_id']} | Amount {row['amount']}")
            else:
                print("✅ No cross-border transactions detected.")
        else:
            print("ℹ️ No transaction type information available.")
