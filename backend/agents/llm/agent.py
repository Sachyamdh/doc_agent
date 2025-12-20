from typing import List, Dict, Optional
from .openai_agent import OpenAIAgent
from .gemini_agent import GeminiAgent
import os

class MultiAIAgent:
    def __init__(self):
        self.openai_key = os.getenv("AZURE_OPENAI_KEY")
        self.openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        self.gemini_key = os.getenv("GEMINI_API_KEY")

        self.openai_agent = OpenAIAgent(
            self.openai_key, 
            self.openai_endpoint, 
            self.openai_deployment
        )
        self.gemini_agent = GeminiAgent(self.gemini_key)

    def analyze_chunks(self, chunks: List[Dict], repo_structure: Dict, progress_callback=None) -> Dict:
        """
        Complete analysis using OpenAI:
        1. Analyzes all code chunks (technical understanding)
        2. Generates quality and improvement recommendations
        
        OpenAI handles everything here because it's better at:
        - Understanding code logic and functions
        - Finding bugs and security issues
        - Providing specific improvements
        - Technical accuracy
        
        Returns complete analysis ready for documentation compilation.
        """
        total = len(chunks)
        chunk_summaries = []

        print("Step 1/2: Analyzing chunks with OpenAI...")
        for idx, chunk in enumerate(chunks):
            chunk_result = {
                'path': chunk['path'],
                'language': chunk['language'],
                'start_line': chunk['start_line'],
                'end_line': chunk['end_line']
            }

            try:
                summary = self.openai_agent.summarize_chunk(chunk)
                chunk_result['summary'] = summary
                chunk_summaries.append(chunk_result)
            except Exception as e:
                print(f"OpenAI chunk analysis failed for {chunk['path']}: {e}")
                chunk_result['summary'] = f"Error: {str(e)}"
                chunk_summaries.append(chunk_result)

            if progress_callback:
                progress_callback(idx + 1, total, "chunk_analysis")

        print("\nStep 2/2: Generating quality and improvements with OpenAI...")
        try:
            quality_and_improvements = self.openai_agent.analyze_code_quality_and_improvements(
                chunk_summaries,
                repo_structure
            )
        except Exception as e:
            print(f"OpenAI quality analysis failed: {e}")
            quality_and_improvements = f"Quality analysis unavailable: {str(e)}"

        if progress_callback:
            progress_callback(total, total, "quality_analysis")

        return {
            'chunk_summaries': chunk_summaries,
            'quality_and_improvements': quality_and_improvements,
            'metadata': {
                'total_chunks': len(chunk_summaries),
                'total_files': len(set(s['path'] for s in chunk_summaries)),
                'analysis_complete': True
            }
        }

    def generate_document(self, analysis_results: Dict, repo_structure: Dict) -> str:
        chunk_summaries = analysis_results.get('chunk_summaries', [])
        quality_and_improvements = analysis_results.get('quality_and_improvements', '')
        
        if not chunk_summaries:
            return "No analysis data provided"

        combined_summaries = "\n\n".join([
            f"File: {s.get('path', 'Unknown')}\nLines: {s.get('start_line', 'N/A')}-{s.get('end_line', 'N/A')}\n{s.get('summary', '')}"
            for s in chunk_summaries
        ])
        
        structure_text = "\n".join([
            f"{path}: {', '.join(files)}" for path, files in repo_structure.items()
        ])

        print("Compiling comprehensive documentation with Gemini...")
        
        prompt = f"""
You are compiling a comprehensive repository documentation from detailed technical analysis.

REPOSITORY STRUCTURE:
{structure_text}

DETAILED CODE ANALYSIS (from OpenAI):
{combined_summaries}

QUALITY AND IMPROVEMENTS ANALYSIS (from OpenAI):
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
            response = self.gemini_agent.model.generate_content(prompt)
            documentation = response.text
            
            final_report = f"""# Comprehensive Repository Analysis Report

{documentation}
"""
            return final_report
            
        except Exception as e:
            print(f"Gemini documentation generation failed: {e}")
            return f"Error generating documentation: {str(e)}"

    def analyze_repository_full(self, chunks: List[Dict], repo_structure: Dict, progress_callback=None) -> Dict:
        """
        Complete workflow:
        1. OpenAI: Analyze chunks + quality
        2. Gemini: Compile into documentation
        """
        print("Starting comprehensive repository analysis...")
        
        analysis_results = self.analyze_chunks(chunks, repo_structure, progress_callback)
        
        print("\nGenerating final documentation...")
        documentation = self.generate_document(analysis_results, repo_structure)
        
        return {
            'analysis_results': analysis_results,
            'documentation': documentation,
            'metadata': analysis_results['metadata']
        }