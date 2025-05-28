# scripts/generate_insights.py

import os
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def generate_insights_from_csv(df: pd.DataFrame) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Convert important data into markdown table format for prompt
    table = df[["Time", "Flight", "Status", "Gate"]].to_markdown(index=False)

    # Prompt for operational analysis
    prompt = f"""
You are a ground operations AI assistant reviewing aircraft taxiing and gate operations at Ottawa International Airport.

Below is a log of aircraft movements. Please analyze and summarize any notable insights such as:
- Flights that held for long durations
- Successful gate arrivals
- Possible traffic conflicts or delays
- Any operational inefficiencies

Data:
{table}

Your summary:
"""

    # Send request and return generated summary
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert aviation operations analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        # Error handling
        return f"Error generating summary: {e}"
