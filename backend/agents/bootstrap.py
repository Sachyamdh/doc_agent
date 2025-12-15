import os
from agents.llm.openai_agent import OpenAIAgent
from agents.llm.gemini_agent import GeminiAgent
from agents.llm.code_analysis_agent import CodeAnalysisAgent
from agents.llm.quality_agent import QualityAgent
from agents.llm.documentation_agent import DocumentationAgent
from agents.planner.planner_agent import PlannerAgent
from agents.orchestrator import AgentOrchestrator
from utils.logger import setup_logger

logger = setup_logger(__name__)

def build_orchestrator():
    logger.info("Building orchestrator with agents")
    
    try:
        # Initialize OpenAI agent
        logger.debug("Initializing OpenAI agent")
        openai_key = os.getenv("AZURE_OPENAI_KEY")
        openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        
        if not all([openai_key, openai_endpoint, openai_deployment]):
            logger.warning("Missing OpenAI configuration in environment variables")
        
        openai_agent = OpenAIAgent(
            api_key=openai_key,
            endpoint=openai_endpoint,
            deployment=openai_deployment,
        )
        logger.info("OpenAI agent initialized successfully")

        # Initialize Gemini agent
        logger.debug("Initializing Gemini agent")
        gemini_key = os.getenv("GEMINI_API_KEY")
        if not gemini_key:
            logger.warning("Missing GEMINI_API_KEY in environment variables")
        
        gemini_agent = GeminiAgent(gemini_key)
        logger.info("Gemini agent initialized successfully")

        # Build orchestrator
        logger.debug("Creating agent orchestrator")
        orchestrator = AgentOrchestrator(
            planner=PlannerAgent(),
            agents={
                "code_analysis": CodeAnalysisAgent(openai_agent),
                "quality": QualityAgent(openai_agent),
                "documentation": DocumentationAgent(gemini_agent),
            }
        )
        logger.info("Orchestrator built successfully")

        return orchestrator
        
    except Exception as e:
        logger.error(f"Failed to build orchestrator: {str(e)}", exc_info=True)
        raise
