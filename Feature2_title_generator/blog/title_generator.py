# blog/title_generator.py

import os, json, re
from typing import List
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def suggest_titles(content: str, n: int = 3) -> List[str]:
    """
    Calls Deepseek-Reasoner model to get 3 blog post titles.
    Expects the model to return a JSON array of strings.
    """
    
    system_prompt = """
    You are an expert blog‐title generator.
    Given the following blog post content, suggest three catchy, concise titles.
    You need to be very creative.
    Respond *only* with a JSON array of exactly three strings, e.g.:\n
    ["Title 1", "Title 2", "Title 3"]
    """
    
    DEEPSEEK_KEY = os.getenv("OPENAI_API_KEY")
    
    deepseek_client = OpenAI(
        api_key=DEEPSEEK_KEY,
        base_url="https://api.deepseek.com"
    )
    
    resp = deepseek_client.chat.completions.create(
        model = "deepseek-reasoner",
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content}
        ],
        temperature=0.7
    )
    text = resp.choices[0].message.content.strip()
    
    # post processing to handle halucinating response
    if "```" in resp:
        text = re.sub(r"^```json\s*|```$", "", text, flags=re.IGNORECASE).strip()
        
    # try to parse JSON; fallback to line‐splitting
    try:
        titles = json.loads(text)
    except json.JSONDecodeError:
        titles = [
            line.strip().strip('"')
            for line in text.splitlines()
            if line.strip()
        ]
    return titles[:n]
