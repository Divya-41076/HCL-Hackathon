import os
import json
import csv
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# Sample CSV data
csv_data = [
    ["transaction_id", "amount", "type", "status", "date"],
    [1, 2000, "TRANSFER", "COMPLETED", "2025-04-10"],
    [2, 1500, "TRANSFER", "COMPLETED", "2025-04-11"],
    [3, 500,  "TRANSFER", "COMPLETED", "2025-04-12"],
    [4, 3000, "TRANSFER", "COMPLETED", "2025-04-12"],
    [5, 200,  "TRANSFER", "COMPLETED", "2025-04-13"],
]

# Write CSV
with open("test_transactions.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(csv_data)

# Read CSV
transactions = []
with open("test_transactions.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        transactions.append({
            "amount": float(row["amount"]),
            "type": row["type"],
            "status": row["status"],
            "date": row["date"]
        })

account_balance = 9500.00

# Call Groq
api_key = os.getenv("GROQ_API_KEY")
print("API KEY FOUND:", bool(api_key))

client = Groq(api_key=api_key)

prompt = f"""You are a helpful banking assistant. Analyze these recent transactions
and current balance, then give a 2-3 sentence friendly financial insight.
Be specific with numbers. Keep it concise and actionable.

Current balance: {account_balance}
Recent transactions: {json.dumps(transactions, indent=2)}

Respond with just the insight paragraph. No headers, no bullet points."""

try:
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.7
    )
    print("\nAI INSIGHT:")
    print(response.choices[0].message.content)
except Exception as e:
    print("ERROR:", e)