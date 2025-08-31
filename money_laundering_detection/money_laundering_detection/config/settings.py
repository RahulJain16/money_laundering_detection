"""
Configuration settings for Money Laundering Detection System
"""

# Detection thresholds
DETECTION_THRESHOLDS = {
    'structuring_threshold': 10000,
    'velocity_threshold': 5,
    'round_amount_threshold': 0.7,
    'cross_border_threshold': 3,
    'dormant_reactivation_days': 90
}

# Regulatory compliance (India - PMLA)
REGULATORY_THRESHOLDS = {
    'ctr_threshold': 1000000,        # ₹10 Lakh
    'str_risk_threshold': 80,        # Risk score
    'large_cash_threshold': 200000,  # ₹2 Lakh
    'cross_border_threshold': 500000 # ₹5 Lakh
}

# ML Model parameters
ML_CONFIG = {
    'isolation_forest_contamination': 0.1,
    'random_forest_n_estimators': 100,
    'feature_selection_threshold': 0.01
}

# Database connection (if using real database)
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'aml_detection',
    'username': 'aml_user',
    'password': 'secure_password'
}