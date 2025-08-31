# src/detector.py
import pandas as pd
import uuid

class MoneyLaunderingDetector:
    def __init__(self, transactions=None, accounts=None):
        self.transactions = transactions if transactions is not None else pd.DataFrame()
        self.accounts = accounts if accounts is not None else pd.DataFrame()

        # ✅ Thresholds are now customizable
        self.thresholds = {
            "large_txn_threshold": 100000,      # ₹1,00,000
            "structuring_threshold": 1000000,   # ₹10,00,000 total/day
        }

    # ✅ Load your own CSV data
    def load_data(self, transactions_file, accounts_file):
        self.transactions = pd.read_csv(transactions_file)
        self.accounts = pd.read_csv(accounts_file)

    # ---------------------- Detection Methods ---------------------- #

    def detect_large_transactions(self):
        alerts = []
        for _, txn in self.transactions.iterrows():
            if txn["amount"] > self.thresholds["large_txn_threshold"]:
                alerts.append({
                    "account_id": txn["account_id"],
                    "alert_id": self._generate_alert_id(),
                    "reason": "Unusually Large Transaction"
                })
        return alerts

    def detect_structuring(self):
        alerts = []

        # 🔍 Debug: check available columns
        print("Columns in transactions DataFrame:", self.transactions.columns)

        # Use 'timestamp' column for date
        if "timestamp" not in self.transactions.columns:
            raise KeyError("No timestamp column found in transactions DataFrame.")

        # Convert to datetime and extract date only
        self.transactions["date"] = pd.to_datetime(self.transactions["timestamp"]).dt.date

        # Group by account and date → sum amounts
        grouped = self.transactions.groupby(["account_id", "date"])["amount"].sum().reset_index()
        for _, row in grouped.iterrows():
            if row["amount"] > self.thresholds["structuring_threshold"]:
                alerts.append({
                    "account_id": row["account_id"],
                    "alert_id": self._generate_alert_id(),
                    "reason": "Structuring/Smurfing Detected"
                })
        return alerts

    # ✅ Custom Pattern Hook
    def detect_custom_pattern(self):
        """
        Add your own detection logic here.
        Example: Flag accounts with > 5 transactions in a single day.
        """
        alerts = []

        # Use 'timestamp' column for date
        if "timestamp" not in self.transactions.columns:
            raise KeyError("No timestamp column found in transactions DataFrame.")

        # Convert to datetime and extract date only
        self.transactions["date"] = pd.to_datetime(self.transactions["timestamp"]).dt.date

        grouped = self.transactions.groupby(["account_id", "date"]).size().reset_index(name="txn_count")
        for _, row in grouped.iterrows():
            if row["txn_count"] > 5:
                alerts.append({
                    "account_id": row["account_id"],
                    "alert_id": self._generate_alert_id(),
                    "reason": f"Unusual activity: {row['txn_count']} transactions on {row['date']}"
                })
        return alerts

    # ---------------------- Orchestrator ---------------------- #
    def detect(self):
        alerts = []
        alerts.extend(self.detect_large_transactions())
        alerts.extend(self.detect_structuring())
        alerts.extend(self.detect_custom_pattern())  # ✅ Plugged in custom rule
        return alerts

    # ---------------------- Helpers ---------------------- #
    def _generate_alert_id(self):
        return "A" + str(uuid.uuid4().int)[:4]  # short unique ID
