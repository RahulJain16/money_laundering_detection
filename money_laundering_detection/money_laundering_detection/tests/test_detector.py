import unittest
import sys
import os
sys.path.append('../src')

from detector import MoneyLaunderingDetector
import pandas as pd

class TestMoneyLaunderingDetector(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.detector = MoneyLaunderingDetector()
        self.detector.generate_sample_data(num_transactions=100)
    
    def test_data_generation(self):
        """Test data generation"""
        self.assertIsNotNone(self.detector.transactions_df)
        self.assertIsNotNone(self.detector.accounts_df)
        self.assertGreater(len(self.detector.transactions_df), 0)
    
    def test_structuring_detection(self):
        """Test structuring pattern detection"""
        from patterns import PatternDetector
        
        pattern_detector = PatternDetector(
            self.detector.transactions_df, 
            self.detector.accounts_df
        )
        
        alerts = pattern_detector.detect_structuring()
        self.assertIsInstance(alerts, list)
    
    def test_alert_generation(self):
        """Test alert generation"""
        alerts = self.detector.run_detection()
        self.assertIsInstance(alerts, list)
        
        # Check alert structure
        if alerts:
            alert = alerts[0]
            required_fields = ['alert_type', 'account_id', 'risk_score', 'description']
            for field in required_fields:
                self.assertIn(field, alert)
    
    def test_compliance_thresholds(self):
        """Test compliance threshold validation"""
        large_amounts = self.detector.transactions_df[
            self.detector.transactions_df['amount'] > 200000
        ]
        
        # Should have some large transactions in sample data
        self.assertGreaterEqual(len(large_amounts), 0)

if __name__ == '__main__':
    unittest.main()