from agents.base.base_agent import BaseAgent
from agents.llm.openai_agent import OpenAIAgent

class CodeAnalysisAgent(BaseAgent):
    name = "CodeAnalysisAgent"
    role = "Analyzes code chunks"

    def __init__(self, openai_agent: OpenAIAgent):
        self.openai_agent = openai_agent

    def run(self, context: dict) -> dict:
        summaries = []

        for chunk in context["chunks"]:
            summary = self.openai_agent.summarize_chunk(chunk)
            summaries.append({
                "path": chunk["path"],
                "language": chunk["language"],
                "start_line": chunk["start_line"],
                "end_line": chunk["end_line"],
                "summary": summary
            })

        return {"chunk_summaries": summaries}
