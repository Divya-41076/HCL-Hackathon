import os
import json
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

def generate_spending_insights(transactions: list, account_balance: float) -> str:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    tx_summary = [
        {
            "amount": t["amount"],
            "type": t["type"],
            "status": t["status"],
            "date": t["date"]
        }
        for t in transactions[-10:]
    ]
    prompt = f"""You are a helpful banking assistant. Analyze these recent transactions 
and current balance, then give a 2-3 sentence friendly financial insight.
Be specific with numbers. Keep it concise and actionable.
Current balance: {account_balance}
Recent transactions (last 10): {json.dumps(tx_summary, indent=2)}
Respond with just the insight paragraph. No headers, no bullet points."""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].message.content