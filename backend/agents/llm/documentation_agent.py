from agents.base.base_agent import BaseAgent

class DocumentationAgent(BaseAgent):
    name = "DocumentationAgent"
    role = "Final documentation compiler"

    def __init__(self, gemini_agent):
        self.gemini_agent = gemini_agent

    def run(self, context: dict) -> dict:
        documentation = self.gemini_agent.generate_content(context)
        return {"documentation": documentation}
