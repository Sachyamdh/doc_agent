import os
from openai import AzureOpenAI
from typing import Dict

class OpenAIAgent:
    def __init__(self, api_key: str, endpoint: str, deployment: str):
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version="2023-07-01-preview",
            azure_endpoint=endpoint
        )
        self.deployment = deployment

    def summarize_chunk(self, chunk: Dict) -> str:
        """
        Summarize a code chunk and return insights.
        """
        prompt_text = f"""
You are an AI code assistant. Analyze the following {chunk['language']} file chunk
from {chunk['path']} (lines {chunk['start_line']}-{chunk['end_line']}).

Content:
{chunk['content']}

Provide a short, structured summary including:
- Functions/classes present
- Purpose of the code
- Any potential notes or insights
"""
        response = self.client.chat.completions.create(
            model=self.deployment,  
            messages=[
                {"role": "system", "content": "You are a helpful code summarizer."},
                {"role": "user", "content": prompt_text}
            ],
        )
        return response.choices[0].message.content