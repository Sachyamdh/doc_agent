from agents.base.base_agent import BaseAgent
from utils.logger import setup_logger

logger = setup_logger(__name__)

class DocumentationAgent(BaseAgent):
    name = "DocumentationAgent"
    role = "Final documentation compiler"

    def __init__(self, gemini_agent):
        self.gemini_agent = gemini_agent
        logger.info("DocumentationAgent initialized")

    def run(self, context: dict) -> dict:
        logger.info("DocumentationAgent starting execution")
        
        try:
            logger.debug("Generating documentation with Gemini agent")
            documentation = self.gemini_agent.generate_content(context)
            logger.info("Documentation generated successfully")
            logger.debug(f"Documentation length: {len(documentation)} characters")
            return {"documentation": documentation}
        except Exception as e:
            logger.error(f"Error generating documentation: {str(e)}", exc_info=True)
            raise
