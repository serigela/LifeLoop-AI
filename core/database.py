"""
Database connector for LifeLoop AI using Supabase.
Provides unified interface for data persistence and retrieval.
"""
import os
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, date
from supabase import create_client, Client

logger = logging.getLogger(__name__)


class DatabaseConnector:
    """Singleton database connector for Supabase."""

    _instance = None
    _client: Optional[Client] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        supabase_url = os.getenv("VITE_SUPABASE_URL")
        supabase_key = os.getenv("VITE_SUPABASE_ANON_KEY")

        if not supabase_url or not supabase_key:
            logger.warning("Supabase credentials not configured. Database features disabled.")
            self._client = None
        else:
            try:
                self._client = create_client(supabase_url, supabase_key)
                logger.info("Database connection established")
            except Exception as e:
                logger.error(f"Failed to connect to database: {e}")
                self._client = None

        self._initialized = True

    def is_connected(self) -> bool:
        """Check if database is connected."""
        return self._client is not None

    # User Profile Methods

    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile by ID."""
        if not self._client:
            return None

        try:
            response = self._client.table('users').select('*').eq('id', user_id).maybeSingle().execute()
            return response.data
        except Exception as e:
            logger.error(f"Error fetching user profile: {e}")
            return None

    def upsert_user_profile(self, user_data: Dict[str, Any]) -> bool:
        """Create or update user profile."""
        if not self._client:
            return False

        try:
            self._client.table('users').upsert(user_data).execute()
            logger.info(f"User profile saved: {user_data.get('email')}")
            return True
        except Exception as e:
            logger.error(f"Error saving user profile: {e}")
            return False

    def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> bool:
        """Update user preferences."""
        if not self._client:
            return False

        try:
            self._client.table('users').update({
                'preferences': preferences,
                'updated_at': datetime.now().isoformat()
            }).eq('id', user_id).execute()
            logger.info(f"User preferences updated: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating preferences: {e}")
            return False

    # Insights Methods

    def save_insight(self, insight_data: Dict[str, Any]) -> bool:
        """Save AI-generated insight."""
        if not self._client:
            return False

        try:
            self._client.table('user_insights').insert(insight_data).execute()
            logger.debug(f"Insight saved: {insight_data.get('insight_type')}")
            return True
        except Exception as e:
            logger.error(f"Error saving insight: {e}")
            return False

    def get_recent_insights(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent insights for user."""
        if not self._client:
            return []

        try:
            response = self._client.table('user_insights')\
                .select('*')\
                .eq('user_id', user_id)\
                .order('created_at', desc=True)\
                .limit(limit)\
                .execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Error fetching insights: {e}")
            return []

    # Activity Methods

    def save_activity(self, activity_data: Dict[str, Any]) -> bool:
        """Save user activity."""
        if not self._client:
            return False

        try:
            self._client.table('user_activities').insert(activity_data).execute()
            logger.debug(f"Activity saved: {activity_data.get('activity_type')}")
            return True
        except Exception as e:
            logger.error(f"Error saving activity: {e}")
            return False

    def get_activities(self, user_id: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get user activities for the last N days."""
        if not self._client:
            return []

        try:
            from datetime import timedelta
            cutoff = (datetime.now() - timedelta(days=days)).isoformat()

            response = self._client.table('user_activities')\
                .select('*')\
                .eq('user_id', user_id)\
                .gte('start_time', cutoff)\
                .order('start_time', desc=True)\
                .execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Error fetching activities: {e}")
            return []

    # Transaction Methods

    def save_transaction(self, transaction_data: Dict[str, Any]) -> bool:
        """Save financial transaction."""
        if not self._client:
            return False

        try:
            self._client.table('user_transactions').insert(transaction_data).execute()
            logger.debug(f"Transaction saved: {transaction_data.get('merchant')}")
            return True
        except Exception as e:
            logger.error(f"Error saving transaction: {e}")
            return False

    def get_transactions(self, user_id: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get user transactions for the last N days."""
        if not self._client:
            return []

        try:
            from datetime import timedelta
            cutoff = (datetime.now() - timedelta(days=days)).date().isoformat()

            response = self._client.table('user_transactions')\
                .select('*')\
                .eq('user_id', user_id)\
                .gte('transaction_date', cutoff)\
                .order('transaction_date', desc=True)\
                .execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Error fetching transactions: {e}")
            return []

    def mark_transaction_anomaly(self, transaction_id: str, is_anomaly: bool = True) -> bool:
        """Mark a transaction as anomaly."""
        if not self._client:
            return False

        try:
            self._client.table('user_transactions')\
                .update({'is_anomaly': is_anomaly})\
                .eq('id', transaction_id)\
                .execute()
            return True
        except Exception as e:
            logger.error(f"Error marking anomaly: {e}")
            return False

    # Health Metrics Methods

    def save_health_metric(self, metric_data: Dict[str, Any]) -> bool:
        """Save health metric."""
        if not self._client:
            return False

        try:
            self._client.table('user_health_metrics').insert(metric_data).execute()
            logger.debug(f"Health metric saved: {metric_data.get('metric_type')}")
            return True
        except Exception as e:
            logger.error(f"Error saving health metric: {e}")
            return False

    def get_health_metrics(
        self,
        user_id: str,
        metric_type: Optional[str] = None,
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """Get health metrics for user."""
        if not self._client:
            return []

        try:
            from datetime import timedelta
            cutoff = (datetime.now() - timedelta(days=days)).isoformat()

            query = self._client.table('user_health_metrics')\
                .select('*')\
                .eq('user_id', user_id)\
                .gte('recorded_at', cutoff)

            if metric_type:
                query = query.eq('metric_type', metric_type)

            response = query.order('recorded_at', desc=True).execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Error fetching health metrics: {e}")
            return []

    # Notification Methods

    def save_notification(self, notification_data: Dict[str, Any]) -> bool:
        """Save notification."""
        if not self._client:
            return False

        try:
            self._client.table('user_notifications').insert(notification_data).execute()
            logger.debug(f"Notification saved: {notification_data.get('title')}")
            return True
        except Exception as e:
            logger.error(f"Error saving notification: {e}")
            return False

    def get_unread_notifications(self, user_id: str) -> List[Dict[str, Any]]:
        """Get unread notifications for user."""
        if not self._client:
            return []

        try:
            response = self._client.table('user_notifications')\
                .select('*')\
                .eq('user_id', user_id)\
                .eq('is_read', False)\
                .order('created_at', desc=True)\
                .execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Error fetching notifications: {e}")
            return []

    def mark_notification_read(self, notification_id: str) -> bool:
        """Mark notification as read."""
        if not self._client:
            return False

        try:
            self._client.table('user_notifications')\
                .update({'is_read': True})\
                .eq('id', notification_id)\
                .execute()
            return True
        except Exception as e:
            logger.error(f"Error marking notification read: {e}")
            return False


def get_database() -> DatabaseConnector:
    """Get singleton database connector instance."""
    return DatabaseConnector()
