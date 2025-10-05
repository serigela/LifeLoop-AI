"""
Finance Agent - Analyzes spending patterns and detects anomalies.
Uses classification and anomaly detection to provide financial insights.
"""
import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

from agents.base_agent import BaseAgent
from core.message_bus import MessageBus

logger = logging.getLogger(__name__)


class FinanceAgent(BaseAgent):
    """
    Monitors financial transactions and spending patterns.
    Classifies expenses and detects anomalies using ML.
    """

    def __init__(self, message_bus: MessageBus):
        super().__init__(message_bus, "FinanceAgent", processing_interval=180)
        self.transactions_df = None
        self.classifier = None
        self.label_encoder = LabelEncoder()
        self.spending_baseline = None

    async def initialize(self):
        """Load transaction data and train classification model."""
        logger.info(f"{self.name}: Loading transaction data...")

        np.random.seed(42)
        categories = ['groceries', 'entertainment', 'transport', 'utilities', 'dining', 'shopping']
        n_transactions = 200

        self.transactions_df = pd.DataFrame({
            'timestamp': pd.date_range(start='2024-01-01', periods=n_transactions, freq='D'),
            'amount': np.random.exponential(50, n_transactions) + 10,
            'merchant': [f"Merchant_{i%30}" for i in range(n_transactions)],
            'category': np.random.choice(categories, n_transactions),
        })

        self.transactions_df['day_of_week'] = self.transactions_df['timestamp'].dt.dayofweek
        self.transactions_df['hour'] = np.random.randint(0, 24, n_transactions)

        self.transactions_df['category_encoded'] = self.label_encoder.fit_transform(
            self.transactions_df['category']
        )

        X = self.transactions_df[['amount', 'day_of_week', 'hour']].values
        y = self.transactions_df['category_encoded'].values

        self.classifier = RandomForestClassifier(n_estimators=50, random_state=42)
        self.classifier.fit(X, y)

        self.spending_baseline = {
            'mean': float(self.transactions_df['amount'].mean()),
            'std': float(self.transactions_df['amount'].std()),
            'median': float(self.transactions_df['amount'].median())
        }

        logger.info(f"{self.name}: Loaded {len(self.transactions_df)} transactions")
        logger.info(f"{self.name}: Trained classification model with {len(categories)} categories")

    async def process(self):
        """Analyze recent transactions and detect anomalies."""
        logger.info(f"{self.name}: Analyzing financial patterns...")

        recent_days = 30
        recent_date = datetime.now() - timedelta(days=recent_days)
        recent_transactions = self.transactions_df[
            self.transactions_df['timestamp'] >= pd.Timestamp(recent_date)
        ]

        category_spending = recent_transactions.groupby('category')['amount'].sum().to_dict()

        anomaly_threshold = self.spending_baseline['mean'] + 2 * self.spending_baseline['std']
        anomalies = recent_transactions[recent_transactions['amount'] > anomaly_threshold]

        insights = {
            'total_spent': float(recent_transactions['amount'].sum()),
            'transaction_count': int(len(recent_transactions)),
            'category_breakdown': {k: float(v) for k, v in category_spending.items()},
            'average_transaction': float(recent_transactions['amount'].mean()),
            'anomalies_detected': int(len(anomalies)),
            'baseline_mean': self.spending_baseline['mean'],
            'analysis_period_days': recent_days
        }

        if len(anomalies) > 0:
            logger.warning(f"{self.name}: Detected {len(anomalies)} unusual transactions")
            insights['anomaly_details'] = [
                {
                    'amount': float(row['amount']),
                    'merchant': row['merchant'],
                    'category': row['category']
                }
                for _, row in anomalies.head(5).iterrows()
            ]

        logger.info(f"{self.name}: Total spending in last {recent_days} days: ${insights['total_spent']:.2f}")

        await self.publish_event(
            event_type="finance_insight",
            data={
                "insights": insights,
                "analysis_timestamp": datetime.now().isoformat()
            }
        )

        logger.info(f"{self.name}: Published finance insights")
