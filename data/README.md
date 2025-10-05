# Sample Data for LifeLoop AI

This directory contains sample datasets for demonstrating the LifeLoop AI system.

## Files

### transactions.csv
Financial transaction data including:
- date: Transaction date
- merchant: Merchant name
- amount: Transaction amount in USD
- category: Expense category (groceries, entertainment, transport, etc.)
- description: Transaction description

### calendar_events.csv
Calendar and activity data including:
- date: Event date
- time: Event start time
- event_type: Type of activity (work, exercise, social, rest)
- duration_minutes: Duration in minutes
- location: Event location
- description: Event description

## Usage

These files are automatically loaded by the respective agents:
- `transactions.csv` is used by the Finance Agent
- `calendar_events.csv` is used by the Activity Agent

The agents also generate additional synthetic data for demonstration purposes.
