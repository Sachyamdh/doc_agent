class OpenAIAgent:
    def __init__(self, api_key: str, endpoint: str, deployment: str):
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version="2023-07-01-preview",
            azure_endpoint=endpoint
        )
        self.deployment = deployment

    def summarize_chunk(self, chunk: Dict) -> str:
        """
        OpenAI excels at: Structured analysis, code quality assessment, and detailed technical insights.
        """
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
        response = self.client.chat.completions.create(
            model=self.deployment,  
            messages=[
                {"role": "system", "content": "You are an expert code reviewer specializing in technical analysis, code quality, and best practices."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content

    def analyze_code_quality_and_improvements(self, all_summaries: List[Dict], repo_structure: Dict) -> str:
        """
        OpenAI's strength: Deep code quality analysis and specific, actionable improvements.
        """
        combined_summaries = "\n\n".join([
            f"File: {s.get('file_path', 'Unknown')}\n{s.get('summary', '')}"
            for s in all_summaries
        ])
        
        structure_text = "\n".join([
            f"{path}: {', '.join(files)}" for path, files in repo_structure.items()
        ])
        
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
        
        return response.choices[0].message.content
