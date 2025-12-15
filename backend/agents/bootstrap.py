import os
from agents.llm.openai_agent import OpenAIAgent
from agents.llm.gemini_agent import GeminiAgent
from agents.llm.code_analysis_agent import CodeAnalysisAgent
from agents.llm.quality_agent import QualityAgent
from agents.llm.documentation_agent import DocumentationAgent
from agents.planner.planner_agent import PlannerAgent
from agents.orchestrator import AgentOrchestrator

def build_orchestrator():
    openai_agent = OpenAIAgent(
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    )

    gemini_agent = GeminiAgent(os.getenv("GEMINI_API_KEY"))

    orchestrator = AgentOrchestrator(
        planner=PlannerAgent(),
        agents={
            "code_analysis": CodeAnalysisAgent(openai_agent),
            "quality": QualityAgent(openai_agent),
            "documentation": DocumentationAgent(gemini_agent),
        }
    )

    return orchestrator
