import os
import openai
from typing import Dict

class OpenAIAgent:
    def __init__(self, api_key: str, endpoint: str, deployment: str):
        openai.api_type = "azure"
        openai.api_base = endpoint
        openai.api_version = "2023-07-01-preview"
        openai.api_key = api_key
        self.deployment = deployment

    def summarize_chunk(self, chunk: Dict) -> str:
        """
        Summarize a code chunk and return insights.
        """
        prompt = f"""
You are an AI code/documentation assistant. Analyze the following {chunk['language']} file chunk
from {chunk['path']} (lines {chunk['start_line']}-{chunk['end_line']}).

Content:
{chunk['content']}

Provide a short, structured summary including:
- Functions/classes present
- Purpose of the code
- Any potential notes or insights
"""
        response = openai.ChatCompletion.create(
            engine=self.deployment,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content.strip()
