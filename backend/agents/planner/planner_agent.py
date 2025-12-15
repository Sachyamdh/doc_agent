from agents.base.base_agent import BaseAgent
from utils.logger import setup_logger

logger = setup_logger(__name__)

class PlannerAgent(BaseAgent):
    name = "PlannerAgent"
    role = "Plans which agents to execute and in what order"

    def run(self, context: dict) -> dict:
        logger.info("PlannerAgent starting execution")
        logger.debug(f"Context contains {len(context.get('chunks', []))} chunks")
        
        try:
            plan = self.create_plan({
                "total_files": len(context.get("repo_structure", {})),
                "total_chunks": len(context.get("chunks", []))
            })
            logger.info(f"Plan created: {plan}")
            return {"plan": plan}
        except Exception as e:
            logger.error(f"Error creating plan: {str(e)}", exc_info=True)
            raise

    def create_plan(self, metadata: dict) -> list:
        logger.debug(f"Creating plan with metadata: {metadata}")
        plan = [
            "code_analysis",
            "quality",
            "documentation"
        ]
        logger.debug(f"Generated plan with {len(plan)} steps")
        return plan
