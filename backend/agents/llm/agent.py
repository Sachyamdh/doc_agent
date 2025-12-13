from typing import List, Dict, Optional
from .openai_agent import OpenAIAgent
from .gemini_agent import GeminiAgent
import os

class MultiAIAgent:
    def __init__(self, code_model="openai", doc_model="gemini"):

        self.openai_key = os.getenv("AZURE_OPENAI_KEY")
        self.openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.gemini_url = os.getenv("GEMINI_API_URL")

        # Assign agents
        self.code_agent = self._init_agent(code_model)
        self.doc_agent = self._init_agent(doc_model)

    def _init_agent(self, model_name):
        if model_name.lower() == "openai":
            return OpenAIAgent(self.openai_key, self.openai_endpoint, self.openai_deployment)
        elif model_name.lower() == "gemini":
            return GeminiAgent(self.gemini_key, self.gemini_url)
        else:
            raise ValueError("Unsupported AI model")

    def analyze_chunks(self, chunks: List[Dict], progress_callback=None) -> List[Dict]:
        """
        Analyze code chunks and return structured summaries
        """
        summaries = []
        total = len(chunks)

        for idx, chunk in enumerate(chunks):
            summary = self.code_agent.summarize_chunk(chunk)
            summaries.append({**chunk, "summary": summary})
            if progress_callback:
                progress_callback(idx + 1, total)
        print("=========Summaries========")
        print(summaries)
        return summaries

    def generate_document(self, summaries: List[Dict]) -> str:
        """
        Convert code analysis into a structured Markdown document
        """
        combined_input = "\n\n".join([f"{s['path']}:\n{s['summary']}" for s in summaries])
        document_chunk = {
            "content": combined_input,
            "path": "combined_analysis",
            "language": "text",
            "start_line": 0,
            "end_line": 0
        }
        return self.doc_agent.summarize_chunk(document_chunk)
