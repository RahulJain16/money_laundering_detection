# run.py
from src.detector import MoneyLaunderingDetector
from src.analytics import AdvancedAnalytics
from src.compliance import RegulatoryCompliance
from src.utils import load_data, generate_sample_data

def main():
    print("="*80)
    print("🏛️  MONEY LAUNDERING DETECTION SYSTEM v2.0")
    print("🇮🇳 PMLA (Prevention of Money Laundering Act) Compliant")
    print("🔒 Advanced Pattern Detection & Regulatory Reporting")
    print("="*80)

    print("\n📊 Initializing data...")

    # ✅ Use your own CSVs OR fallback to sample data
    try:
        # Replace with your files
        transactions, accounts = load_data(
            "data/transactions.csv",
            "data/accounts.csv"
        )
        print(f"✅ Loaded {len(transactions)} transactions from file")
        print(f"✅ Loaded {len(accounts)} accounts from file")
    except FileNotFoundError:
        print("⚠️ No CSVs found, generating sample data...")
        transactions, accounts = generate_sample_data()
        print(f"✅ Generated {len(transactions)} sample transactions")
        print(f"✅ Generated {len(accounts)} sample accounts")

    # ✅ Initialize detector
    detector = MoneyLaunderingDetector(transactions, accounts)

    # 🔧 Customization (change thresholds here)
    detector.thresholds["large_txn_threshold"] = 50000     # ₹50k
    detector.thresholds["structuring_threshold"] = 200000  # ₹2L

    # ✅ Run detection
    print("\n🔍 Running detection algorithms...")
    alerts = detector.detect()

    if alerts:
        print("\n🚨 Alerts Generated:")
        for alert in alerts:
            print(f" - Account {alert['account_id']} | {alert['alert_id']} | {alert['reason']}")
    else:
        print("✅ No suspicious activity detected.")

    # ✅ Advanced analytics
    print("\n📈 Running Advanced Analytics...")
    analytics = AdvancedAnalytics(transactions, accounts)
    analytics.run()

    # ✅ Compliance reporting
    print("\n📝 Generating Compliance Report...")
    compliance = RegulatoryCompliance(alerts)
    compliance.generate_report()

if __name__ == "__main__":
    main()
