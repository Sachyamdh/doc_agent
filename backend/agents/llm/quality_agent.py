from agents.base.base_agent import BaseAgent

class QualityAgent(BaseAgent):
    name = "QualityAgent"
    role = "Code quality and improvements"

    def __init__(self, openai_agent):
        self.openai_agent = openai_agent

    def run(self, context: dict) -> dict:
        result = self.openai_agent.analyze_code_quality_and_improvements(
            context["chunk_summaries"],
            context["repo_structure"]
        )
        return {"quality_and_improvements": result}
