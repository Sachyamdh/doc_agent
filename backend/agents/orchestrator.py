class AgentOrchestrator:
    def __init__(self, planner, agents: dict):
        self.planner = planner
        self.agents = agents

    def run(self, chunks, repo_structure):
        context = {
            "chunks": chunks,
            "repo_structure": repo_structure
        }

        planner_result = self.planner.run(context)
        plan = planner_result["plan"]


        for step in plan:
            result = self.agents[step].run(context)
            context.update(result)

        return context
