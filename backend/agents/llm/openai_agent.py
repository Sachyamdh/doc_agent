from typing import List, Dict, Optional
import os
from openai import AzureOpenAI
from utils.logger import setup_logger

logger = setup_logger(__name__)

class OpenAIAgent:
    def __init__(self, api_key: str, endpoint: str, deployment: str):
        logger.info("Initializing OpenAIAgent")
        try:
            self.client = AzureOpenAI(
                api_key=api_key,
                api_version="2023-07-01-preview",
                azure_endpoint=endpoint
            )
            self.deployment = deployment
            logger.info(f"OpenAIAgent initialized with deployment: {deployment}")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAIAgent: {str(e)}", exc_info=True)
            raise

    def summarize_chunk(self, chunk: Dict) -> str:
        logger.debug(f"Summarizing chunk from {chunk.get('path', 'unknown')} (lines {chunk.get('start_line', '?')}-{chunk.get('end_line', '?')})")
        
        prompt_text = f"""
Analyze the following {chunk['language']} code from {chunk['path']} 
(lines {chunk['start_line']}-{chunk['end_line']}):

{chunk['content']}

Provide a detailed technical analysis covering:
- Key functions/classes with their parameters and return types
- Design patterns and architectural decisions
- Code quality observations (readability, maintainability, performance)
- Potential bugs, security issues, or code smells
- Best practices followed or violated
"""
        try:
            logger.debug(f"Making OpenAI API call for chunk summary (deployment: {self.deployment})")
            response = self.client.chat.completions.create(
                model=self.deployment,  
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer specializing in technical analysis, code quality, and best practices."},
                    {"role": "user", "content": prompt_text}
                ],
                temperature=0.3
            )
            result = response.choices[0].message.content
            logger.debug(f"Chunk summary generated successfully, length: {len(result)} characters")
            return result
        except Exception as e:
            logger.error(f"Error in summarize_chunk for {chunk.get('path', 'unknown')}: {str(e)}", exc_info=True)
            raise

    def analyze_code_quality_and_improvements(self, all_summaries: List[Dict], repo_structure: Dict) -> str:
        logger.info(f"Starting code quality analysis for {len(all_summaries)} summaries")
        
        combined_summaries = "\n\n".join([
            f"File: {s.get('file_path', 'Unknown')}\n{s.get('summary', '')}"
            for s in all_summaries
        ])
        
        structure_text = "\n".join([
            f"{path}: {', '.join(files)}" for path, files in repo_structure.items()
        ])
        
        logger.debug(f"Combined summaries length: {len(combined_summaries)} characters")
        logger.debug(f"Repository structure has {len(repo_structure)} directories")
        
        prompt_text = f"""
You are conducting a comprehensive code quality review and improvement analysis.

REPOSITORY STRUCTURE:
{structure_text}

CODE ANALYSIS:
{combined_summaries}

Provide a detailed analysis in the following format:

## Code Quality Assessment

### Strengths
[List 4-6 specific strengths with examples:
- Strength 1: Detailed explanation with code reference
- Strength 2: Detailed explanation with code reference]

### Weaknesses
[List 4-6 specific weaknesses with examples:
- Weakness 1: Detailed explanation with code reference
- Weakness 2: Detailed explanation with code reference]

### Code Metrics Analysis
- **Complexity**: [Assessment of code complexity]
- **Maintainability**: [Assessment of maintainability]
- **Readability**: [Assessment of readability]
- **Test Coverage**: [Observations about testing]
- **Documentation**: [Assessment of documentation quality]

### Security Considerations
[List potential security issues or vulnerabilities]

### Performance Observations
[List performance-related observations]

## Recommended Improvements

### High Priority
1. **[Specific Issue]**: 
   - Current State: [What's wrong]
   - Recommended Fix: [Detailed solution]
   - Impact: [Why this matters]

2. **[Specific Issue]**: 
   - Current State: [What's wrong]
   - Recommended Fix: [Detailed solution]
   - Impact: [Why this matters]

### Medium Priority
3. **[Specific Issue]**: 
   - Current State: [What's wrong]
   - Recommended Fix: [Detailed solution]
   - Impact: [Why this matters]

4. **[Specific Issue]**: 
   - Current State: [What's wrong]
   - Recommended Fix: [Detailed solution]
   - Impact: [Why this matters]

### Low Priority (Nice to Have)
5. **[Specific Issue]**: 
   - Current State: [What's wrong]
   - Recommended Fix: [Detailed solution]
   - Impact: [Why this matters]

## Best Practices Recommendations
[List specific best practices that should be adopted]

Be extremely specific and actionable in all recommendations.
"""
        
        try:
            logger.debug("Making OpenAI API call for quality analysis")
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a senior software engineer and code quality expert. Provide detailed, actionable feedback with specific examples."
                    },
                    {"role": "user", "content": prompt_text}
                ],
                temperature=0.3,
                max_tokens=2500
            )
            
            result = response.choices[0].message.content
            logger.info(f"Quality analysis completed successfully, length: {len(result)} characters")
            return result
        except Exception as e:
            logger.error(f"Error in analyze_code_quality_and_improvements: {str(e)}", exc_info=True)
            raise
