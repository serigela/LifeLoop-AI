/*
  # LifeLoop AI Database Schema
  
  Creates the core schema for LifeLoop AI personal automation system.
  
  ## Tables Created
  
  ### 1. users
  - `id` (uuid, primary key) - User identifier
  - `email` (text, unique) - User email address
  - `name` (text) - User display name
  - `timezone` (text) - User timezone
  - `preferences` (jsonb) - User preferences and settings
  - `created_at` (timestamptz) - Account creation timestamp
  - `updated_at` (timestamptz) - Last update timestamp
  
  ### 2. user_insights
  - `id` (uuid, primary key) - Insight identifier
  - `user_id` (uuid, foreign key) - User reference
  - `insight_type` (text) - Type of insight (activity/finance/email/holistic)
  - `summary` (text) - AI-generated summary
  - `recommendations` (jsonb) - Array of recommendations
  - `metadata` (jsonb) - Additional insight data
  - `created_at` (timestamptz) - Insight generation timestamp
  
  ### 3. user_activities
  - `id` (uuid, primary key) - Activity identifier
  - `user_id` (uuid, foreign key) - User reference
  - `activity_type` (text) - Type of activity (work/exercise/social/rest)
  - `duration_minutes` (integer) - Activity duration
  - `location` (text) - Activity location
  - `notes` (text) - Additional notes
  - `start_time` (timestamptz) - Activity start time
  - `end_time` (timestamptz) - Activity end time
  - `created_at` (timestamptz) - Record creation timestamp
  
  ### 4. user_transactions
  - `id` (uuid, primary key) - Transaction identifier
  - `user_id` (uuid, foreign key) - User reference
  - `merchant` (text) - Merchant name
  - `amount` (decimal) - Transaction amount
  - `category` (text) - Expense category
  - `description` (text) - Transaction description
  - `transaction_date` (date) - Transaction date
  - `is_anomaly` (boolean) - Anomaly flag
  - `created_at` (timestamptz) - Record creation timestamp
  
  ### 5. user_health_metrics
  - `id` (uuid, primary key) - Metric identifier
  - `user_id` (uuid, foreign key) - User reference
  - `metric_type` (text) - Type of metric (steps/sleep/heart_rate/weight)
  - `value` (decimal) - Metric value
  - `unit` (text) - Measurement unit
  - `recorded_at` (timestamptz) - Metric timestamp
  - `source` (text) - Data source (fitbit/apple_health/manual)
  - `created_at` (timestamptz) - Record creation timestamp
  
  ### 6. user_notifications
  - `id` (uuid, primary key) - Notification identifier
  - `user_id` (uuid, foreign key) - User reference
  - `notification_type` (text) - Type of notification
  - `title` (text) - Notification title
  - `message` (text) - Notification message
  - `priority` (text) - Priority level (high/medium/low)
  - `is_read` (boolean) - Read status
  - `sent_at` (timestamptz) - Send timestamp
  - `created_at` (timestamptz) - Record creation timestamp
  
  ## Security
  
  All tables have Row Level Security (RLS) enabled with policies ensuring:
  - Users can only access their own data
  - Authenticated users required for all operations
*/

-- Create users table
CREATE TABLE IF NOT EXISTS users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email text UNIQUE NOT NULL,
  name text NOT NULL,
  timezone text DEFAULT 'UTC',
  preferences jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create user_insights table
CREATE TABLE IF NOT EXISTS user_insights (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id) ON DELETE CASCADE NOT NULL,
  insight_type text NOT NULL,
  summary text NOT NULL,
  recommendations jsonb DEFAULT '[]',
  metadata jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now()
);

-- Create user_activities table
CREATE TABLE IF NOT EXISTS user_activities (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id) ON DELETE CASCADE NOT NULL,
  activity_type text NOT NULL,
  duration_minutes integer NOT NULL,
  location text,
  notes text,
  start_time timestamptz NOT NULL,
  end_time timestamptz,
  created_at timestamptz DEFAULT now()
);

-- Create user_transactions table
CREATE TABLE IF NOT EXISTS user_transactions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id) ON DELETE CASCADE NOT NULL,
  merchant text NOT NULL,
  amount decimal(10, 2) NOT NULL,
  category text NOT NULL,
  description text,
  transaction_date date NOT NULL,
  is_anomaly boolean DEFAULT false,
  created_at timestamptz DEFAULT now()
);

-- Create user_health_metrics table
CREATE TABLE IF NOT EXISTS user_health_metrics (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id) ON DELETE CASCADE NOT NULL,
  metric_type text NOT NULL,
  value decimal(10, 2) NOT NULL,
  unit text NOT NULL,
  recorded_at timestamptz NOT NULL,
  source text DEFAULT 'manual',
  created_at timestamptz DEFAULT now()
);

-- Create user_notifications table
CREATE TABLE IF NOT EXISTS user_notifications (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id) ON DELETE CASCADE NOT NULL,
  notification_type text NOT NULL,
  title text NOT NULL,
  message text NOT NULL,
  priority text DEFAULT 'medium',
  is_read boolean DEFAULT false,
  sent_at timestamptz,
  created_at timestamptz DEFAULT now()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_user_insights_user_id ON user_insights(user_id);
CREATE INDEX IF NOT EXISTS idx_user_insights_created_at ON user_insights(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_user_activities_user_id ON user_activities(user_id);
CREATE INDEX IF NOT EXISTS idx_user_activities_start_time ON user_activities(start_time DESC);
CREATE INDEX IF NOT EXISTS idx_user_transactions_user_id ON user_transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_transactions_date ON user_transactions(transaction_date DESC);
CREATE INDEX IF NOT EXISTS idx_user_health_metrics_user_id ON user_health_metrics(user_id);
CREATE INDEX IF NOT EXISTS idx_user_health_metrics_recorded_at ON user_health_metrics(recorded_at DESC);
CREATE INDEX IF NOT EXISTS idx_user_notifications_user_id ON user_notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_user_notifications_is_read ON user_notifications(is_read);

-- Enable Row Level Security on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_insights ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_health_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_notifications ENABLE ROW LEVEL SECURITY;

-- RLS Policies for users table
CREATE POLICY "Users can view own profile"
  ON users FOR SELECT
  TO authenticated
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON users FOR UPDATE
  TO authenticated
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

-- RLS Policies for user_insights table
CREATE POLICY "Users can view own insights"
  ON user_insights FOR SELECT
  TO authenticated
  USING (user_id = auth.uid());

CREATE POLICY "Users can insert own insights"
  ON user_insights FOR INSERT
  TO authenticated
  WITH CHECK (user_id = auth.uid());

-- RLS Policies for user_activities table
CREATE POLICY "Users can view own activities"
  ON user_activities FOR SELECT
  TO authenticated
  USING (user_id = auth.uid());

CREATE POLICY "Users can insert own activities"
  ON user_activities FOR INSERT
  TO authenticated
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update own activities"
  ON user_activities FOR UPDATE
  TO authenticated
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can delete own activities"
  ON user_activities FOR DELETE
  TO authenticated
  USING (user_id = auth.uid());

-- RLS Policies for user_transactions table
CREATE POLICY "Users can view own transactions"
  ON user_transactions FOR SELECT
  TO authenticated
  USING (user_id = auth.uid());

CREATE POLICY "Users can insert own transactions"
  ON user_transactions FOR INSERT
  TO authenticated
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update own transactions"
  ON user_transactions FOR UPDATE
  TO authenticated
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can delete own transactions"
  ON user_transactions FOR DELETE
  TO authenticated
  USING (user_id = auth.uid());

-- RLS Policies for user_health_metrics table
CREATE POLICY "Users can view own health metrics"
  ON user_health_metrics FOR SELECT
  TO authenticated
  USING (user_id = auth.uid());

CREATE POLICY "Users can insert own health metrics"
  ON user_health_metrics FOR INSERT
  TO authenticated
  WITH CHECK (user_id = auth.uid());

-- RLS Policies for user_notifications table
CREATE POLICY "Users can view own notifications"
  ON user_notifications FOR SELECT
  TO authenticated
  USING (user_id = auth.uid());

CREATE POLICY "Users can update own notifications"
  ON user_notifications FOR UPDATE
  TO authenticated
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update updated_at on users table
CREATE TRIGGER update_users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
