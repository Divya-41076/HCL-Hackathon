import os
import json
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)


def generate_spending_insights(transactions: list, account_balance: float) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "AI insights unavailable — GROQ_API_KEY not found."

    if not transactions:
        return "No transactions found to analyze yet."

    client = Groq(api_key=api_key)

    tx_summary = []
    for t in transactions[-10:]:
        try:
            tx_summary.append(
                {
                    "amount": float(
                        t.get("amount")
                        if isinstance(t, dict)
                        else getattr(t, "amount", 0)
                    ),
                    "type": (
                        t.get("type")
                        if isinstance(t, dict)
                        else getattr(t, "type", "TRANSFER")
                    ),
                    "status": (
                        t.get("status")
                        if isinstance(t, dict)
                        else getattr(t, "status", "COMPLETED")
                    ),
                    "date": str(
                        t.get("date") if isinstance(t, dict) else getattr(t, "date", "")
                    ),
                }
            )
        except Exception:
            continue

    balance = float(account_balance)

    prompt = f"""You are a helpful banking assistant. Analyze these recent transactions
and current balance, then give a 2-3 sentence friendly financial insight.
Be specific with numbers. Keep it concise and actionable.

Current balance: {balance}
Recent transactions (last 10): {json.dumps(tx_summary, indent=2)}

Respond with just the insight paragraph. No headers, no bullet points."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Unable to generate insights at the moment. {str(e)}"
