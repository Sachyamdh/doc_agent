import os
import requests
from typing import Dict

class GeminiAgent:
    def __init__(self, api_key: str, api_url: str):
        self.api_key = api_key
        self.api_url = api_url

    def summarize_chunk(self, chunk: Dict) -> str:
        prompt = f"""
Analyze the following {chunk['language']} code from {chunk['path']} 
(lines {chunk['start_line']}-{chunk['end_line']}):

{chunk['content']}

Return a descriptive.
"""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"prompt": prompt, "max_tokens": 500}

        res = requests.post(self.api_url, json=payload, headers=headers)
        res.raise_for_status()
        data = res.json()
        print("=========Summaries========")
        print(data.get("summary", "No summary returned"))
        return data.get("summary", "No summary returned")
