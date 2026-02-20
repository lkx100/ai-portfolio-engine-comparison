import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv(".env")

def analyze_strategies(results: dict) -> str:
    API_KEY = os.environ.get("GROQ_API_KEY")
    
    if not API_KEY:
        return "GROQ_API_KEY not set in environment! Please do so. Else refer README"
    
    client = Groq(api_key=API_KEY)

    prompt = f"""
    Analyze the following portfolio strategy performance metrics and provide a concise comparison.

    Strategy Results (JSON):
    {json.dumps(results, indent=2)}

    Please address the following:
    1. Compare the two strategies on total return and CAGR
    2. Highlight risk-return trade-offs (note: both strategies have similar volatility)
    3. Explain what the max drawdown difference implies for an investor
    4. Suggest a market condition where each strategy might outperform the other
    5. Suggest one concrete improvement to either strategy

    Be specific — reference the actual numbers in your response.
    """

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "system",
                "content": "You are a quantitative finance analyst who gives precise, numbers-driven analysis."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content