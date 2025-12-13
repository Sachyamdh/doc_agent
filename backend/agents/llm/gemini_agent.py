import google.generativeai as genai
from typing import Dict
import os

class GeminiAgent:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        print("Available models:")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"  - {m.name}")
        self.model = genai.GenerativeModel(os.getenv("GEMINI_MODEL","gemini-2.5-flash"))

    def summarize_chunk(self, chunk: Dict) -> str:
        prompt = f"""
Analyze the following {chunk['language']} code from {chunk['path']} 
(lines {chunk['start_line']}-{chunk['end_line']}):

{chunk['content']}

Return a descriptive summary including:
- Functions/classes present
- Purpose of the code
- Any potential notes or insights
"""
        try:
            response = self.model.generate_content(prompt)
            summary = response.text
            print("=========Summaries========")
            print(summary)
            return summary
        except Exception as e:
            print(f"Error generating summary: {e}")
            return f"Error: {str(e)}"