from agents.base.base_agent import BaseAgent
from utils.logger import setup_logger

logger = setup_logger(__name__)

class QualityAgent(BaseAgent):
    name = "QualityAgent"
    role = "Code quality and improvements"

    def __init__(self, openai_agent):
        self.openai_agent = openai_agent
        logger.info("QualityAgent initialized")

    def run(self, context: dict) -> dict:
        logger.info("QualityAgent starting execution")
        
        chunk_summaries = context.get("chunk_summaries", [])
        repo_structure = context.get("repo_structure", {})
        
        logger.info(f"Analyzing quality for {len(chunk_summaries)} summaries")
        
        try:
            result = self.openai_agent.analyze_code_quality_and_improvements(
                chunk_summaries,
                repo_structure
            )
            logger.info("Quality analysis completed successfully")
            logger.debug(f"Quality analysis result length: {len(result)} characters")
            return {"quality_and_improvements": result}
        except Exception as e:
            logger.error(f"Error in quality analysis: {str(e)}", exc_info=True)
            raise
