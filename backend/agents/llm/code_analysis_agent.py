from agents.base.base_agent import BaseAgent
from agents.llm.openai_agent import OpenAIAgent
from utils.logger import setup_logger

logger = setup_logger(__name__)

class CodeAnalysisAgent(BaseAgent):
    name = "CodeAnalysisAgent"
    role = "Analyzes code chunks"

    def __init__(self, openai_agent: OpenAIAgent):
        self.openai_agent = openai_agent
        logger.info("CodeAnalysisAgent initialized")

    def run(self, context: dict) -> dict:
        logger.info("CodeAnalysisAgent starting execution")
        chunks = context.get("chunks", [])
        logger.info(f"Processing {len(chunks)} code chunks")
        
        summaries = []

        for idx, chunk in enumerate(chunks):
            try:
                logger.debug(f"Analyzing chunk {idx + 1}/{len(chunks)}: {chunk.get('path', 'unknown')}")
                summary = self.openai_agent.summarize_chunk(chunk)
                summaries.append({
                    "path": chunk["path"],
                    "language": chunk["language"],
                    "start_line": chunk["start_line"],
                    "end_line": chunk["end_line"],
                    "summary": summary
                })
                logger.debug(f"Chunk {idx + 1} analyzed successfully")
            except Exception as e:
                logger.error(f"Error analyzing chunk {idx + 1} ({chunk.get('path', 'unknown')}): {str(e)}", exc_info=True)
                summaries.append({
                    "path": chunk.get("path", "unknown"),
                    "language": chunk.get("language", "unknown"),
                    "start_line": chunk.get("start_line", 0),
                    "end_line": chunk.get("end_line", 0),
                    "summary": f"Error during analysis: {str(e)}"
                })

        logger.info(f"CodeAnalysisAgent completed: {len(summaries)} summaries generated")
        return {"chunk_summaries": summaries}
