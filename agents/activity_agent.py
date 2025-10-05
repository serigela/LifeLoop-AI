"""
Activity Agent - Analyzes user activity patterns and routines.
Uses clustering algorithms to detect recurring patterns in calendar data.
"""
import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from agents.base_agent import BaseAgent
from core.message_bus import MessageBus

logger = logging.getLogger(__name__)


class ActivityAgent(BaseAgent):
    """
    Monitors and analyzes user activity patterns.
    Detects routines using machine learning clustering.
    """

    def __init__(self, message_bus: MessageBus):
        super().__init__(message_bus, "ActivityAgent", processing_interval=300)
        self.activities_df = None
        self.scaler = StandardScaler()
        self.kmeans = None

    async def initialize(self):
        """Load activity data and initialize ML models."""
        logger.info(f"{self.name}: Loading activity data...")

        self.activities_df = pd.DataFrame({
            'timestamp': pd.date_range(start='2024-01-01', periods=100, freq='H'),
            'activity_type': np.random.choice(['work', 'exercise', 'social', 'rest'], 100),
            'duration_minutes': np.random.randint(15, 180, 100),
            'location': np.random.choice(['home', 'office', 'gym', 'outdoor'], 100),
        })

        self.activities_df['hour'] = self.activities_df['timestamp'].dt.hour
        self.activities_df['day_of_week'] = self.activities_df['timestamp'].dt.dayofweek

        self.kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)

        logger.info(f"{self.name}: Loaded {len(self.activities_df)} activity records")

    async def process(self):
        """Analyze activity patterns and detect routines."""
        logger.info(f"{self.name}: Analyzing activity patterns...")

        features = self.activities_df[['hour', 'day_of_week', 'duration_minutes']].values
        scaled_features = self.scaler.fit_transform(features)

        clusters = self.kmeans.fit_predict(scaled_features)
        self.activities_df['routine_cluster'] = clusters

        routine_summary = {}
        for cluster_id in range(4):
            cluster_data = self.activities_df[self.activities_df['routine_cluster'] == cluster_id]

            if len(cluster_data) > 0:
                routine_summary[f"routine_{cluster_id}"] = {
                    'count': int(len(cluster_data)),
                    'avg_hour': float(cluster_data['hour'].mean()),
                    'most_common_activity': cluster_data['activity_type'].mode()[0] if not cluster_data.empty else 'unknown',
                    'avg_duration': float(cluster_data['duration_minutes'].mean())
                }

        logger.info(f"{self.name}: Detected {len(routine_summary)} routine patterns")

        await self.publish_event(
            event_type="activity_summary",
            data={
                "routines": routine_summary,
                "total_activities": int(len(self.activities_df)),
                "analysis_timestamp": datetime.now().isoformat()
            }
        )

        logger.info(f"{self.name}: Published activity summary")
