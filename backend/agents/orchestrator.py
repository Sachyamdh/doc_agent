from utils.logger import setup_logger

logger = setup_logger(__name__)

class AgentOrchestrator:
    def __init__(self, planner, agents: dict):
        self.planner = planner
        self.agents = agents
        logger.info(f"AgentOrchestrator initialized with {len(agents)} agents: {list(agents.keys())}")

    def run(self, chunks, repo_structure):
        logger.info("Starting orchestrator run")
        logger.debug(f"Processing {len(chunks)} chunks")
        
        context = {
            "chunks": chunks,
            "repo_structure": repo_structure
        }

        try:
            logger.info("Running planner agent")
            planner_result = self.planner.run(context)
            plan = planner_result["plan"]
            logger.info(f"Planner created plan with {len(plan)} steps: {plan}")
        except Exception as e:
            logger.error(f"Planner failed: {str(e)}", exc_info=True)
            raise

        for step in plan:
            try:
                logger.info(f"Executing plan step: {step}")
                if step not in self.agents:
                    logger.error(f"Agent '{step}' not found in available agents: {list(self.agents.keys())}")
                    raise ValueError(f"Agent '{step}' not found")
                
                result = self.agents[step].run(context)
                context.update(result)
                logger.info(f"Step '{step}' completed successfully")
                logger.debug(f"Context updated with keys: {list(result.keys())}")
            except Exception as e:
                logger.error(f"Error executing step '{step}': {str(e)}", exc_info=True)
                raise

        logger.info("Orchestrator run completed successfully")
        return context
