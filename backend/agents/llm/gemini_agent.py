from typing import List, Dict, Optional
import os
import google.generativeai as genai

class GeminiAgent:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-1.5-flash"))

    def summarize_chunk(self, chunk: Dict) -> str:
        """
        Gemini excels at: High-level understanding, pattern recognition, and contextual analysis.
        """
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
            response = self.model.generate_content(prompt)
            summary = response.text
            return summary
        except Exception as e:
            print(f"Error generating summary: {e}")
            return f"Error: {str(e)}"

    def generate_overview_and_architecture(self, all_summaries: List[Dict], repo_structure: Dict) -> str:
        """
        Gemini's strength: High-level overview, architecture understanding, and feature identification.
        """
        combined_summaries = "\n\n".join([
            f"File: {s.get('file_path', 'Unknown')}\n{s.get('summary', '')}"
            for s in all_summaries
        ])
        
        structure_text = "\n".join([
            f"{path}: {', '.join(files)}" for path, files in repo_structure.items()
        ])
        
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
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating overview: {e}")
            return f"Error: {str(e)}"
