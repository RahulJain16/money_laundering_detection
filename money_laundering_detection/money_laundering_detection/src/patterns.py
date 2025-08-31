import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import networkx as nx
from collections import Counter

class PatternDetector:
    def __init__(self, transactions_df, accounts_df):
        self.transactions_df = transactions_df
        self.accounts_df = accounts_df
        
    def detect_structuring(self):
        """Detect structuring patterns"""
        print("🔍 Detecting Structuring Patterns...")
        alerts = []
        
        # Group by account and day
        daily_groups = self.transactions_df.groupby([
            'account_id',
            self.transactions_df['timestamp'].dt.date
        ]).agg({
            'amount': ['sum', 'count'],
            'cash_transaction': 'sum'
        }).reset_index()
        
        daily_groups.columns = ['account_id', 'date', 'total_amount', 'txn_count', 'cash_count']
        
        for _, row in daily_groups.iterrows():
            if (row['txn_count'] >= 3 and 
                row['total_amount'] > 10000 and 
                row['cash_count'] >= 2):
                
                alerts.append({
                    'alert_type': 'Structuring',
                    'account_id': row['account_id'],
                    'date': row['date'],
                    'transaction_count': row['txn_count'],
                    'total_amount': row['total_amount'],
                    'risk_score': min(100, (row['txn_count'] * 8) + (row['cash_count'] * 10)),
                    'description': f"Account made {row['txn_count']} transactions totaling ₹{row['total_amount']:,.2f}",
                    'detected_at': datetime.now()
                })
        
        print(f"Found {len(alerts)} structuring patterns")
        return alerts
    
    def detect_layering(self):
        """Detect layering patterns"""
        print("🔍 Detecting Layering Patterns...")
        alerts = []
        
        # Create transaction network
        G = nx.DiGraph()
        
        wire_transfers = self.transactions_df[
            self.transactions_df['transaction_type'] == 'Wire Transfer'
        ]
        
        for _, txn in wire_transfers.iterrows():
            G.add_edge(
                txn['account_id'], 
                txn['counter_party'],
                weight=txn['amount'],
                timestamp=txn['timestamp'],
                txn_id=txn['transaction_id']
            )
        
        # Find complex transfer chains
        for account in list(G.nodes())[:50]:  # Limit for performance
            try:
                # Find all paths from this account
                for target in list(G.nodes())[:20]:
                    if target != account and target in G:
                        paths = list(nx.all_simple_paths(G, account, target, cutoff=5))
                        
                        for path in paths:
                            if len(path) >= 3:
                                total_amount = 0
                                try:
                                    for i in range(len(path)-1):
                                        if G.has_edge(path[i], path[i+1]):
                                            total_amount += G[path[i]][path[i+1]]['weight']
                                except:
                                    continue
                                
                                if total_amount > 100000:
                                    alerts.append({
                                        'alert_type': 'Layering',
                                        'account_id': account,
                                        'chain_length': len(path),
                                        'total_amount': total_amount,
                                        'path': ' → '.join(path[:4]),
                                        'risk_score': min(100, (len(path) * 12) + (total_amount / 50000)),
                                        'description': f"Complex transfer chain through {len(path)} entities",
                                        'detected_at': datetime.now()
                                    })
            except Exception as e:
                continue
        
        # Remove duplicate alerts
        unique_alerts = {}
        for alert in alerts:
            key = f"{alert['account_id']}_{alert['path']}"
            if key not in unique_alerts or unique_alerts[key]['risk_score'] < alert['risk_score']:
                unique_alerts[key] = alert
        
        print(f"Found {len(unique_alerts)} layering patterns")
        return list(unique_alerts.values())
    
    def detect_smurfing(self):
        """Detect smurfing patterns"""
        print("🔍 Detecting Smurfing Patterns...")
        alerts = []
        
        # Analyze cash deposits by account
        cash_deposits = self.transactions_df[
            self.transactions_df['cash_transaction'] == True
        ]
        
        account_analysis = cash_deposits.groupby('account_id').agg({
            'counter_party': 'nunique',
            'amount': ['sum', 'count', 'std'],
            'timestamp': ['min', 'max']
        }).reset_index()
        
        account_analysis.columns = ['account_id', 'unique_depositors', 'total_amount', 
                                   'txn_count', 'amount_std', 'first_txn', 'last_txn']
        
        for _, row in account_analysis.iterrows():
            if (row['unique_depositors'] >= 6 and 
                row['total_amount'] > 100000 and
                row['txn_count'] >= 10):
                
                time_span = (row['last_txn'] - row['first_txn']).days
                if time_span <= 45:  # Within 45 days
                    alerts.append({
                        'alert_type': 'Smurfing',
                        'account_id': row['account_id'],
                        'unique_depositors': row['unique_depositors'],
                        'total_amount': row['total_amount'],
                        'transaction_count': row['txn_count'],
                        'time_period_days': time_span,
                        'risk_score': min(100, (row['unique_depositors'] * 6) + (row['txn_count'] * 3)),
                        'description': f"{row['unique_depositors']} depositors, ₹{row['total_amount']:,.2f} in {time_span} days",
                        'detected_at': datetime.now()
                    })
        
        print(f"Found {len(alerts)} smurfing patterns")
        return alerts
    
    def detect_round_amounts(self):
        """Detect suspicious round amount patterns"""
        print("🔍 Detecting Round Amount Patterns...")
        alerts = []
        
        # Identify round amounts
        self.transactions_df['is_round'] = self.transactions_df['amount'].apply(
            lambda x: x % 1000 == 0 or x % 5000 == 0 or x % 10000 == 0 or x % 25000 == 0
        )
        
        account_round_analysis = self.transactions_df.groupby('account_id').agg({
            'is_round': 'sum',
            'transaction_id': 'count',
            'amount': 'sum',
            'is_international': 'sum'
        }).reset_index()
        
        account_round_analysis.columns = ['account_id', 'round_count', 'total_txns', 
                                         'total_amount', 'intl_count']
        
        account_round_analysis['round_percentage'] = (
            account_round_analysis['round_count'] / account_round_analysis['total_txns']
        )
        
        for _, row in account_round_analysis.iterrows():
            if (row['round_percentage'] > 0.6 and 
                row['total_txns'] >= 5 and
                row['total_amount'] > 200000):
                
                alerts.append({
                    'alert_type': 'Round Amount Fraud',
                    'account_id': row['account_id'],
                    'round_percentage': row['round_percentage'] * 100,
                    'round_transactions': row['round_count'],
                    'total_amount': row['total_amount'],
                    'risk_score': min(100, (row['round_percentage'] * 60) + (row['intl_count'] * 8)),
                    'description': f"{row['round_percentage']*100:.1f}% round amounts, total ₹{row['total_amount']:,.2f}",
                    'detected_at': datetime.now()
                })
        
        print(f"Found {len(alerts)} round amount patterns")
        return alerts
    
    def detect_velocity_anomalies(self):
        """Detect transaction velocity anomalies"""
        print("🔍 Detecting Velocity Anomalies...")
        alerts = []
        
        # Calculate hourly velocity
        self.transactions_df['date_hour'] = self.transactions_df['timestamp'].dt.floor('H')
        
        hourly_velocity = self.transactions_df.groupby(['account_id', 'date_hour']).agg({
            'transaction_id': 'count',
            'amount': 'sum'
        }).reset_index()
        
        hourly_velocity.columns = ['account_id', 'date_hour', 'hourly_count', 'hourly_amount']
        
        # Find high velocity accounts
        max_velocity = hourly_velocity.groupby('account_id')['hourly_count'].max()
        
        for account_id, max_vel in max_velocity.items():
            if max_vel >= 8:  # 8+ transactions in one hour
                account_data = hourly_velocity[hourly_velocity['account_id'] == account_id]
                avg_amount = account_data['hourly_amount'].mean()
                
                alerts.append({
                    'alert_type': 'High Velocity',
                    'account_id': account_id,
                    'max_hourly_transactions': max_vel,
                    'avg_hourly_amount': avg_amount,
                    'risk_score': min(100, (max_vel * 8) + (avg_amount / 20000)),
                    'description': f"Up to {max_vel} transactions in single hour",
                    'detected_at': datetime.now()
                })
        
        print(f"Found {len(alerts)} velocity anomalies")
        return alerts
    
    def detect_dormant_reactivation(self):
        """Detect dormant account reactivation"""
        print("🔍 Detecting Dormant Account Reactivation...")
        alerts = []
        
        account_activity = self.transactions_df.groupby('account_id').agg({
            'timestamp': ['min', 'max', 'count'],
            'amount': 'sum'
        }).reset_index()
        
        account_activity.columns = ['account_id', 'first_txn', 'last_txn', 'txn_count', 'total_amount']
        
        for _, row in account_activity.iterrows():
            if row['txn_count'] >= 2:
                account_txns = self.transactions_df[
                    self.transactions_df['account_id'] == row['account_id']
                ].sort_values('timestamp')
                
                # Find gaps in activity
                gaps = account_txns['timestamp'].diff().dt.days
                max_gap = gaps.max()
                
                if max_gap >= 90:  # 90+ days dormant
                    recent_txns = account_txns[
                        account_txns['timestamp'] >= (datetime.now() - timedelta(days=30))
                    ]
                    
                    if len(recent_txns) >= 3 and recent_txns['amount'].sum() > 200000:
                        alerts.append({
                            'alert_type': 'Dormant Reactivation',
                            'account_id': row['account_id'],
                            'dormant_period_days': int(max_gap),
                            'recent_transactions': len(recent_txns),
                            'recent_amount': recent_txns['amount'].sum(),
                            'risk_score': min(100, (max_gap / 5) + (len(recent_txns) * 8)),
                            'description': f"Dormant {int(max_gap)} days, then ₹{recent_txns['amount'].sum():,.2f}",
                            'detected_at': datetime.now()
                        })
        
        print(f"Found {len(alerts)} dormant reactivation patterns")
        return alerts