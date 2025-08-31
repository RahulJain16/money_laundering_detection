from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import os
from src.detector import MoneyLaunderingDetector
from src.analytics import AdvancedAnalytics
from src.compliance import RegulatoryCompliance
from src.utils import load_data, generate_sample_data

app = Flask(__name__)

# Global variables to store data and results
transactions_data = None
accounts_data = None
detection_results = None

@app.route('/')
def index():
    """Home page with file upload and demo options"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file uploads"""
    global transactions_data, accounts_data
    
    try:
        # Check if files were uploaded
        if 'transactions' in request.files and 'accounts' in request.files:
            transactions_file = request.files['transactions']
            accounts_file = request.files['accounts']
            
            if transactions_file.filename and accounts_file.filename:
                # Read uploaded files
                transactions_data = pd.read_csv(transactions_file)
                accounts_data = pd.read_csv(accounts_file)
                
                return jsonify({
                    'success': True,
                    'message': f'Uploaded {len(transactions_data)} transactions and {len(accounts_data)} accounts',
                    'transactions_count': len(transactions_data),
                    'accounts_count': len(accounts_data)
                })
        
        return jsonify({'success': False, 'message': 'Please upload both files'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/demo')
def demo():
    """Generate demo data and run detection"""
    global transactions_data, accounts_data, detection_results
    
    try:
        # Generate sample data
        transactions_data, accounts_data = generate_sample_data(1000)
        
        # Run detection
        detector = MoneyLaunderingDetector(transactions_data, accounts_data)
        alerts = detector.detect()
        
        # Run analytics
        analytics = AdvancedAnalytics(transactions_data, accounts_data)
        analytics.run()
        
        # Generate compliance report
        compliance = RegulatoryCompliance(alerts)
        compliance.generate_report()
        
        detection_results = {
            'alerts': alerts,
            'transactions_count': len(transactions_data),
            'accounts_count': len(accounts_data),
            'alerts_count': len(alerts)
        }
        
        return redirect(url_for('dashboard'))
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/dashboard')
def dashboard():
    """Main dashboard showing detection results"""
    global transactions_data, accounts_data, detection_results
    
    if transactions_data is None or accounts_data is None:
        return redirect(url_for('index'))
    
    return render_template('dashboard.html', 
                         transactions=transactions_data.head(10).to_dict('records'),
                         accounts=accounts_data.to_dict('records'),
                         results=detection_results)

@app.route('/api/run-detection', methods=['POST'])
def run_detection():
    """API endpoint to run detection on uploaded data"""
    global transactions_data, accounts_data, detection_results
    
    if transactions_data is None or accounts_data is None:
        return jsonify({'success': False, 'message': 'No data uploaded'})
    
    try:
        # Customize thresholds if provided
        custom_thresholds = request.json.get('thresholds', {})
        
        # Initialize detector
        detector = MoneyLaunderingDetector(transactions_data, accounts_data)
        
        # Apply custom thresholds
        if 'large_txn_threshold' in custom_thresholds:
            detector.thresholds["large_txn_threshold"] = custom_thresholds['large_txn_threshold']
        if 'structuring_threshold' in custom_thresholds:
            detector.thresholds["structuring_threshold"] = custom_thresholds['structuring_threshold']
        
        # Run detection
        alerts = detector.detect()
        
        # Run analytics
        analytics = AdvancedAnalytics(transactions_data, accounts_data)
        analytics.run()
        
        # Store results
        detection_results = {
            'alerts': alerts,
            'transactions_count': len(transactions_data),
            'accounts_count': len(accounts_data),
            'alerts_count': len(alerts),
            'thresholds_used': detector.thresholds
        }
        
        return jsonify({
            'success': True,
            'alerts_count': len(alerts),
            'alerts': alerts[:10],  # First 10 alerts for preview
            'message': f'Detection completed. Found {len(alerts)} alerts.'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/get-alerts')
def get_alerts():
    """API endpoint to get all alerts"""
    global detection_results
    
    if detection_results is None:
        return jsonify({'success': False, 'message': 'No detection results available'})
    
    return jsonify({
        'success': True,
        'alerts': detection_results['alerts'],
        'summary': {
            'total_alerts': len(detection_results['alerts']),
            'transactions_analyzed': detection_results['transactions_count'],
            'accounts_monitored': detection_results['accounts_count']
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
