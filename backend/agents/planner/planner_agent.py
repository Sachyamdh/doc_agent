from agents.base.base_agent import BaseAgent

class PlannerAgent(BaseAgent):
    name = "PlannerAgent"
    role = "Plans which agents to execute and in what order"

    def run(self, context: dict) -> dict:
        plan = self.create_plan({
            "total_files": len(context.get("repo_structure", {})),
            "total_chunks": len(context.get("chunks", []))
        })

        return {"plan": plan}

    def create_plan(self, metadata: dict) -> list:
        return [
            "code_analysis",
            "quality",
            "documentation"
        ]
