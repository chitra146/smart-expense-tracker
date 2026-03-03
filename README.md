Smart Expense Tracker   

A Python-based command-line Expense Tracker application designed to log, manage, analyze, and visualize personal financial transactions with built-in budget monitoring.

Project Overview    Expense Tracker - link

Managing daily expenses manually can be inefficient and error-prone.
This project provides a simple yet powerful solution to:

Log daily expenses
Categorize spending
Track monthly budgets
Analyze spending patterns
Visualize financial behavior

The application uses Python and Pandas for data processing and Matplotlib for visualization.

Problem Statement

Individuals often struggle to:
Track daily expenses
Identify overspending categories
Monitor monthly budget limits
Analyze spending trends

This project solves these challenges through a structured expense management system.





Features

Add new expenses (Date, Amount, Category, Description)
View all logged expenses
Category-wise expense summary
Search expenses by date range
Monthly budget monitoring
Data visualization (Bar Chart)
Basic login authentication
Error handling for invalid inputs
Automatic CSV data persistence

Tech Stack

Python
Pandas
Matplotlib
CSV (Data Storage)
Git & GitHub

Project Architecture
User Input
   ↓
Validation
   ↓
CSV Storage (expenses.csv)
   ↓
Pandas Processing
   ↓
Analytics & KPI Calculation
   ↓
Visualization Output

This structured flow simulates real-world data processing pipelines.

Project Structure
smart-expense-tracker/
│
├── expense_tracker.py
├── expenses.csv (auto-generated)
├── README.md
├── requirements.txt
⚙ Installation Guide

1️⃣ Clone the repository:
git clone https://github.com/chitra146/smart-expense-tracker.git

2️⃣ Navigate into project folder:
cd smart-expense-tracker

3️⃣ Install dependencies:
pip install pandas matplotlib
▶How to Run the Project
python expense_tracker.py
Login Credentials
Username: admin
Password: 1234
KPIs Implemented

Total Spending = SUM(amount)
Monthly Spending = SUM(current_month expenses)
Category-wise Spending = GROUP BY category
Budget Utilization % = (Monthly Spending / Budget) × 100

Data Visualization
Category-wise Expense Distribution (Bar Chart)
This helps identify high-spending categories quickly.

Challenges Faced
Handling date validation and filtering
Managing CSV file persistence
Implementing error handling for invalid user inputs
Integrating budget logic with dynamic monthly filtering

Future Enhancements
Streamlit Web Application version
Multi-user authentication system
Database integration (PostgreSQL)
Machine Learning-based expense prediction
Anomaly detection for unusual spending
Interactive dashboard UI

Learning Outcomes
Through this project, I gained hands-on experience in:
Python programming
File handling & data persistence
Data aggregation using Pandas
KPI implementation
Data visualization
Git version control
Structured project documentation

Author

Chitra
Aspiring Data Analyst | Python & SQL Enthusiast
GitHub: https://github.com/chitra146



