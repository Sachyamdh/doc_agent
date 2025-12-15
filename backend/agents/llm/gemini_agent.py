from typing import List, Dict, Optional
import os
import google.generativeai as genai
from utils.logger import setup_logger

logger = setup_logger(__name__)

class GeminiAgent:
    def __init__(self, api_key: str):
        logger.info("Initializing GeminiAgent")
        try:
            genai.configure(api_key=api_key)
            model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
            self.model = genai.GenerativeModel(model_name)
            logger.info(f"GeminiAgent initialized with model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize GeminiAgent: {str(e)}", exc_info=True)
            raise

    def summarize_chunk(self, chunk: Dict) -> str:
        """
        Gemini excels at: High-level understanding, pattern recognition, and contextual analysis.
        """
        logger.debug(f"Summarizing chunk from {chunk.get('path', 'unknown')} with Gemini")
        
        prompt = f"""
Analyze the following {chunk['language']} code from {chunk['path']} 
(lines {chunk['start_line']}-{chunk['end_line']}):

{chunk['content']}

Provide a concise summary focusing on:
- Overall purpose and functionality
- How this code fits into the larger system
- Key algorithms or business logic
- Integration points and dependencies
- Notable patterns or approaches used
"""
        try:
            logger.debug("Making Gemini API call for chunk summary")
            response = self.model.generate_content(prompt)
            summary = response.text
            logger.debug(f"Gemini chunk summary generated, length: {len(summary)} characters")
            return summary
        except Exception as e:
            logger.error(f"Error generating Gemini summary: {str(e)}", exc_info=True)
            return f"Error: {str(e)}"

    def generate_overview_and_architecture(self, all_summaries: List[Dict], repo_structure: Dict) -> str:
        """
        Gemini's strength: High-level overview, architecture understanding, and feature identification.
        """
        logger.info(f"Generating overview and architecture for {len(all_summaries)} summaries")
        
        combined_summaries = "\n\n".join([
            f"File: {s.get('file_path', 'Unknown')}\n{s.get('summary', '')}"
            for s in all_summaries
        ])
        
        structure_text = "\n".join([
            f"{path}: {', '.join(files)}" for path, files in repo_structure.items()
        ])
        
        logger.debug(f"Combined summaries length: {len(combined_summaries)} characters")
        logger.debug(f"Repository structure has {len(repo_structure)} directories")
        
        prompt = f"""
You are analyzing a complete code repository to understand its architecture and features.

REPOSITORY STRUCTURE:
{structure_text}

CODE ANALYSIS:
{combined_summaries}

Provide a comprehensive high-level analysis in the following format:

## Repository Overview
[3-4 sentences describing:
- What this project does (main purpose)
- Who would use it (target audience)
- Key value proposition
- Overall scope and scale]

## Architecture & Technical Approach

### System Architecture
[Describe the overall system architecture:
- Architectural pattern used (MVC, microservices, etc.)
- Component organization
- Data flow
- Key architectural decisions]

### Design Patterns
[List and explain design patterns used:
- Pattern 1: Where and why it's used
- Pattern 2: Where and why it's used]

### Code Organization
[Describe how the code is organized:
- Directory structure rationale
- Module/package organization
- Separation of concerns]

## Important Files

### Core Files
[List 3-5 most important files:
- **filename.ext**: Role and importance in the system
- **filename.ext**: Role and importance in the system]

### Configuration Files
[List configuration files and their purpose]

### Entry Points
[List main entry points or bootstrap files]

## Special Features

### Unique Features
[List 4-6 notable or unique features:
- **Feature 1**: Detailed description and implementation approach
- **Feature 2**: Detailed description and implementation approach]

### Technical Highlights
[Highlight impressive technical implementations or clever solutions]

### Integration & APIs
[Describe external integrations, APIs used, or APIs provided]

## Important Functions/Classes

### Core Components
[List 6-10 most critical functions/classes:
- **ComponentName**: 
  - Purpose: What it does
  - Key Responsibilities: Main tasks
  - Interactions: How it connects with other components
  
- **ComponentName**: 
  - Purpose: What it does
  - Key Responsibilities: Main tasks
  - Interactions: How it connects with other components]

### Utility Functions
[List important utility or helper functions]

## Technology Stack

### Languages
- Primary: [Language and version]
- Secondary: [Other languages used]

### Frameworks & Libraries
- **Core Framework**: [Name and purpose]
- **UI Framework**: [If applicable]
- **State Management**: [If applicable]
- **Testing**: [Testing frameworks]
- **Build Tools**: [Build/bundling tools]

### External Services & APIs
- [List external services, APIs, or third-party integrations]

### Development Tools
- [List development, linting, formatting tools]

### Infrastructure
- [Deployment, hosting, CI/CD information if apparent]

Be descriptive and focus on understanding the big picture and how components work together.
"""
        
        try:
            logger.debug("Making Gemini API call for overview and architecture")
            response = self.model.generate_content(prompt)
            result = response.text
            logger.info(f"Overview and architecture generated successfully, length: {len(result)} characters")
            return result
        except Exception as e:
            logger.error(f"Error generating overview: {str(e)}", exc_info=True)
            return f"Error: {str(e)}"

    def generate_content(self, context: dict) -> str:
        """
        Generate comprehensive documentation from analysis context.
        This is the main method used by DocumentationAgent.
        """
        logger.info("Generating comprehensive documentation")
        
        chunk_summaries = context.get('chunk_summaries', [])
        quality_and_improvements = context.get('quality_and_improvements', '')
        repo_structure = context.get('repo_structure', {})
        
        if not chunk_summaries:
            logger.warning("No chunk summaries provided for documentation generation")
            return "No analysis data provided"

        logger.debug(f"Processing {len(chunk_summaries)} summaries for documentation")
        
        combined_summaries = "\n\n".join([
            f"File: {s.get('path', 'Unknown')}\nLines: {s.get('start_line', 'N/A')}-{s.get('end_line', 'N/A')}\n{s.get('summary', '')}"
            for s in chunk_summaries
        ])
        
        structure_text = "\n".join([
            f"{path}: {', '.join(files)}" for path, files in repo_structure.items()
        ])

        logger.debug("Compiling comprehensive documentation prompt")
        
        prompt = f"""
You are compiling a comprehensive repository documentation from detailed technical analysis.

REPOSITORY STRUCTURE:
{structure_text}

DETAILED CODE ANALYSIS:
{combined_summaries}

QUALITY AND IMPROVEMENTS ANALYSIS:
{quality_and_improvements}

Create a complete, professional documentation report in this format:

## Repository Overview
[3-4 sentences describing the project's main purpose, target users, key value proposition, and scope]

## System Architecture

### Architectural Pattern
[Describe the architectural pattern used and why it fits this project]

### Component Organization
[Explain how the codebase is organized and the rationale]

### Data Flow
[Describe how data moves through the system]

### Key Design Decisions
[Highlight important architectural decisions made]

## Important Files

### Core Files
[List 4-6 critical files with their specific roles and importance]

### Configuration & Setup
[List important configuration files]

### Entry Points
[Identify main application entry points]

## Key Features & Functionality
[List 6-8 main features with detailed descriptions of what they do and how they work]

## Technology Stack

### Languages
[List programming languages used]

### Frameworks & Libraries
[List major frameworks and key libraries]

### External Services & APIs
[List any external services or APIs integrated]

### Development Tools
[List build tools, testing frameworks, etc.]

## Important Functions & Classes
[Extract and list 8-10 most critical functions/classes from the analysis with:
- Name and location
- Purpose and functionality
- Key responsibilities
- Why it's important to the system]

## Code Quality Analysis
[Synthesize the quality analysis provided, organizing it clearly]

## Recommended Improvements
[Organize the improvements from the analysis into clear categories:
- High Priority (critical issues)
- Medium Priority (important enhancements)
- Low Priority (nice to have)]

## Security & Performance Considerations
[Extract and summarize any security or performance observations from the analysis]

## Development Best Practices Observed
[Note any good practices or patterns used in the codebase]

## Project Statistics
- Total Files Analyzed: {len(set(s['path'] for s in chunk_summaries))}
- Total Code Chunks: {len(chunk_summaries)}
- Primary Language: [Identify from analysis]

Create a cohesive, professional report that flows naturally. Synthesize the technical details into clear, actionable documentation.
"""
        
        try:
            logger.debug("Making Gemini API call for documentation generation")
            response = self.model.generate_content(prompt)
            documentation = response.text
            
            final_report = f"""# Comprehensive Repository Analysis Report

{documentation}
"""
            logger.info(f"Documentation generated successfully, total length: {len(final_report)} characters")
            return final_report
            
        except Exception as e:
            logger.error(f"Error generating documentation: {str(e)}", exc_info=True)
            return f"Error generating documentation: {str(e)}"
