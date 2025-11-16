"""
Mistral AI service for code analysis and Q&A
"""
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from app.core.config import settings
from app.core.logging import setup_logging
from typing import List, Dict, Any
import json
import re

logger = setup_logging()


class MistralService:
    """Service for interacting with Mistral AI API"""
    
    def __init__(self):
        """Initialize Mistral client"""
        api_key = settings.MISTRAL_API_KEY
        if not api_key or api_key.strip() == "":
            logger.warning("MISTRAL_API_KEY is not set. AI features will be unavailable.")
            self.client = None
        else:
            self.client = MistralClient(api_key=api_key.strip())
        self.model = "mistral-medium"  # Using mistral-medium for better code understanding
    
    async def analyze_code_with_ai(self, code_content: str, language: str, 
                                   analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use Mistral AI to provide intelligent code analysis
        
        Args:
            code_content: The code to analyze
            language: Programming language
            analysis_result: Basic analysis results
            
        Returns:
            Enhanced analysis with AI insights
        """
        if not self.client:
            logger.warning("Mistral AI client not initialized. Skipping AI analysis.")
            return {
                "ai_insights": "AI analysis unavailable: MISTRAL_API_KEY not configured. Please set your Mistral API key in the .env file.",
                "enhanced_suggestions": [],
                "code_quality_score": None
            }
        
        try:
            prompt = self._build_analysis_prompt(code_content, language, analysis_result)
            
            messages = [
                ChatMessage(role="system", content="""You are an expert code reviewer and software architect. Your role is to provide SPECIFIC, ACTIONABLE code review feedback.

CRITICAL RULES - VIOLATIONS WILL RESULT IN POOR FEEDBACK:
1. NEVER use vague phrases like "4 functions", "some methods", "various places" - ALWAYS name exact functions/classes
2. When suggesting docstrings, list each function explicitly: "Add docstrings to: `apply()` in DocumentNavigationStrategy, `apply()` in TicketNavigationStrategy, `__init__()` in NavigationState"
3. ALWAYS specify exact locations using actual function/class/method names from the code (e.g., "In `TicketNavigationStrategy.apply()` method at line ~110")
4. ALWAYS provide concrete code examples showing BEFORE and AFTER with real function/class names
5. NEVER include empty or generic sections (e.g., "Algorithm Improvements:" with no content)
6. If you cannot provide a specific suggestion with exact function names, OMIT that suggestion entirely
7. Focus on implementable improvements with clear steps that name exact code elements

EXAMPLE OF GOOD SUGGESTION:
"Add docstrings to: `apply()` method in `DocumentNavigationStrategy` class (line ~80), `apply()` method in `TicketNavigationStrategy` class (line ~110), `__init__()` method in `NavigationState` class (line ~55), and `_normalize_field()` helper function (line ~45)"

EXAMPLE OF BAD SUGGESTION:
"Consider adding docstrings to 4 function(s)" - THIS IS TOO VAGUE AND UNACCEPTABLE

Your suggestions must be detailed enough that a developer can immediately implement them without guessing what to do or where to do it."""),
                ChatMessage(role="user", content=prompt)
            ]
            
            response = self.client.chat(
                model=self.model,
                messages=messages,
                temperature=0.3,  # Lower temperature for more consistent, factual responses
                max_tokens=4000  # Increased for detailed, actionable suggestions
            )
            
            ai_analysis = response.choices[0].message.content
            
            return {
                "ai_insights": ai_analysis,
                "enhanced_suggestions": self._extract_suggestions(ai_analysis),
                "code_quality_score": self._extract_quality_score(ai_analysis)
            }
        except Exception as e:
            logger.error(f"Error in Mistral AI analysis: {str(e)}")
            return {
                "ai_insights": "AI analysis temporarily unavailable",
                "enhanced_suggestions": [],
                "code_quality_score": None
            }
    
    async def answer_question(self, question: str, code_context: str, 
                             language: str) -> Dict[str, str]:
        """
        Answer questions about code using Mistral AI
        
        Args:
            question: User's question about the code
            code_context: Relevant code context
            language: Programming language
            
        Returns:
            Answer dictionary
        """
        if not self.client:
            logger.warning("Mistral AI client not initialized. Cannot answer question.")
            return {
                "answer": "AI Q&A is unavailable: MISTRAL_API_KEY not configured. Please set your Mistral API key in the .env file.",
                "question": question,
                "language": language
            }
        
        try:
            prompt = self._build_qa_prompt(question, code_context, language)
            
            messages = [
                ChatMessage(role="system", content="You are a helpful coding assistant. Answer questions about code clearly and concisely, providing examples when helpful."),
                ChatMessage(role="user", content=prompt)
            ]
            
            response = self.client.chat(
                model=self.model,
                messages=messages,
                temperature=0.5,
                max_tokens=1500
            )
            
            answer = response.choices[0].message.content
            
            return {
                "answer": answer,
                "question": question,
                "language": language
            }
        except Exception as e:
            logger.error(f"Error in Mistral AI Q&A: {str(e)}")
            return {
                "answer": "I apologize, but I'm having trouble processing your question right now. Please try again.",
                "question": question,
                "language": language
            }
    
    async def generate_documentation(self, code_content: str, language: str, 
                                    analysis_result: Dict[str, Any]) -> str:
        """
        Generate comprehensive documentation for code
        
        Args:
            code_content: The code to document
            language: Programming language
            analysis_result: Analysis results
            
        Returns:
            Generated documentation
        """
        if not self.client:
            logger.warning("Mistral AI client not initialized. Cannot generate documentation.")
            return "# Documentation Generation Unavailable\n\nMISTRAL_API_KEY not configured. Please set your Mistral API key in the .env file to generate documentation."
        
        try:
            prompt = self._build_documentation_prompt(code_content, language, analysis_result)
            
            messages = [
                ChatMessage(role="system", content="You are a technical writer specializing in code documentation. Generate clear, comprehensive documentation following best practices."),
                ChatMessage(role="user", content=prompt)
            ]
            
            response = self.client.chat(
                model=self.model,
                messages=messages,
                temperature=0.4,
                max_tokens=3000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating documentation: {str(e)}")
            return "Documentation generation temporarily unavailable."
    
    def _build_analysis_prompt(self, code_content: str, language: str, 
                              analysis_result: Dict[str, Any]) -> str:
        """Build prompt for code analysis"""
        # Extract function and class names for context
        functions = analysis_result.get('functions', [])
        classes = analysis_result.get('classes', [])
        
        function_names = [f.get('name', '') for f in functions[:10]]
        class_names = [c.get('name', '') for c in classes[:10]]
        
        return f"""Analyze the following {language} code and provide a detailed, actionable code review.

CRITICAL REQUIREMENTS:
- Only include sections that have actual, specific suggestions
- For each suggestion, provide: WHAT to change, WHERE (function/class/line), WHY, and HOW (with code example)
- If a category has no suggestions, omit it entirely
- Be specific: mention function names, line numbers (approximate), and provide before/after code examples
- Focus on concrete, implementable improvements

Code to analyze:
```{language}
{code_content[:4000]}
```

Code Structure Context:
- Functions found: {', '.join(function_names) if function_names else 'None detected'}
- Classes found: {', '.join(class_names) if class_names else 'None detected'}
- Complexity score: {analysis_result.get('complexity_score', 'N/A')}

CRITICAL: When mentioning functions, classes, or methods, you MUST use their exact names from the code above.
- If suggesting docstrings, name the exact functions: "Add docstring to `function_name()`" NOT "Add docstrings to 4 functions"
- If suggesting improvements, specify: "In `ClassName.method_name()` at line ~X" NOT "In some methods"
- Always reference actual identifiers from the code structure context above

Provide your analysis in the following structured format. ONLY include sections with actual suggestions:

# Code Quality Assessment

**Overall Score:** [X]/10

**Reasoning:** [2-3 sentences explaining the score]

# Specific Recommendations

For each recommendation, use this format:

## [Category]: [Brief Title]

**Location:** [EXACT function/class/method name from code above, e.g., `DocumentNavigationStrategy.apply()` or `NavigationState.__init__()` at line ~X]
**Issue:** [What's wrong or could be improved - be specific about the exact code element]
**Impact:** [Why this matters]
**Solution:** 
```{language}
// Before:
[existing code with exact function/class names]

// After:
[improved code]
```

**Implementation Steps:**
1. [Step 1 - be specific about which function/class to modify]
2. [Step 2]

---

CRITICAL REQUIREMENTS FOR ALL SUGGESTIONS:
- MUST name exact functions/classes/methods (e.g., "Add docstring to `apply()` method in `DocumentNavigationStrategy` class")
- MUST specify exact locations (e.g., "In `TicketNavigationStrategy.apply()` method, line ~110")
- MUST provide concrete code examples with actual function/class names
- NEVER use vague phrases like "4 functions", "some methods", "various places"
- If suggesting docstrings, list each function: "Add docstrings to: `apply()` in DocumentNavigationStrategy, `apply()` in TicketNavigationStrategy, `__init__()` in NavigationState, and `_normalize_field()` helper function"

Only include recommendations that have:
- Specific location with exact function/class/method names
- Clear problem statement referencing actual code elements
- Concrete code example showing the fix with real identifiers
- Implementation steps that name exact functions/classes to modify

If there are no suggestions in a category (e.g., no security issues, no performance problems), DO NOT include that category.

IMPORTANT: Do NOT include horizontal rules (---) or separators at the end of your response. End cleanly without trailing dashes or separators."""
    
    def _build_qa_prompt(self, question: str, code_context: str, language: str) -> str:
        """Build prompt for Q&A"""
        return f"""Answer the following question about this {language} code:

Question: {question}

Code Context:
```{language}
{code_context[:2000]}
```

Provide a clear, detailed answer with examples if helpful."""
    
    def _build_documentation_prompt(self, code_content: str, language: str, 
                                   analysis_result: Dict[str, Any]) -> str:
        """Build prompt for documentation generation"""
        return f"""Generate comprehensive documentation for this {language} code:

1. Overview: High-level description of what the code does
2. Functions/Methods: Document each function with parameters, return values, and examples
3. Classes: Document classes with their purpose, properties, and methods
4. Usage Examples: Provide usage examples
5. Dependencies: List required dependencies

Code:
```{language}
{code_content[:4000]}
```

Analysis Context:
{json.dumps(analysis_result, indent=2)}

Generate professional, well-structured documentation."""
    
    def _extract_suggestions(self, ai_analysis: str) -> List[str]:
        """Extract actionable suggestions from AI analysis, preserving markdown formatting"""
        suggestions = []
        lines = ai_analysis.split('\n')
        current_suggestion = []
        in_suggestion = False
        
        for i, line in enumerate(lines):
            # Look for recommendation headers (## or ###)
            if line.strip().startswith('##') and any(keyword in line.lower() for keyword in ['recommendation', 'suggestion', 'improvement', 'issue', 'fix', 'type safety', 'error handling', 'bug fix', 'code clarity', 'performance', 'security', 'incomplete']):
                if current_suggestion:
                    # Join preserving newlines for markdown
                    suggestion_text = '\n'.join(current_suggestion).strip()
                    # Remove trailing dashes
                    suggestion_text = re.sub(r'\n---+?\s*$', '', suggestion_text)
                    suggestion_text = re.sub(r'---+?\s*$', '', suggestion_text)
                    suggestion_text = suggestion_text.strip()
                    if suggestion_text and len(suggestion_text) > 20:
                        suggestions.append(suggestion_text)
                current_suggestion = [line]
                in_suggestion = True
            elif in_suggestion:
                # Stop collecting if we hit another main section header
                if line.strip().startswith('#') and not line.strip().startswith('##'):
                    if current_suggestion:
                        suggestion_text = '\n'.join(current_suggestion).strip()
                        suggestion_text = re.sub(r'\n---+?\s*$', '', suggestion_text)
                        suggestion_text = re.sub(r'---+?\s*$', '', suggestion_text)
                        suggestion_text = suggestion_text.strip()
                        if suggestion_text and len(suggestion_text) > 20:
                            suggestions.append(suggestion_text)
                    current_suggestion = []
                    in_suggestion = False
                else:
                    # Continue collecting, preserving the line as-is
                    current_suggestion.append(line)
        
        # Add last suggestion
        if current_suggestion:
            suggestion_text = '\n'.join(current_suggestion).strip()
            suggestion_text = re.sub(r'\n---+?\s*$', '', suggestion_text)
            suggestion_text = re.sub(r'---+?\s*$', '', suggestion_text)
            suggestion_text = suggestion_text.strip()
            if suggestion_text and len(suggestion_text) > 20:
                suggestions.append(suggestion_text)
        
        # Fallback: extract bullet points if structured format not found
        if not suggestions:
            for line in lines:
                if any(keyword in line.lower() for keyword in ['suggest', 'recommend', 'consider', 'should', 'improve', 'fix', 'change']):
                    if line.strip().startswith(('-', '*', '•', '1.', '2.', '3.', '**')):
                        clean_line = line.strip().lstrip('-*•123456789. ').strip()
                        if len(clean_line) > 20:  # Only meaningful suggestions
                            suggestions.append(clean_line)
        
        # Clean all suggestions to remove trailing dashes, but preserve markdown
        cleaned_suggestions = []
        for suggestion in suggestions[:15]:
            # Remove trailing dashes but keep newlines for markdown
            cleaned = re.sub(r'\n---+?\s*$', '', suggestion, flags=re.MULTILINE)
            cleaned = re.sub(r'---+?\s*$', '', cleaned)
            cleaned = cleaned.strip()
            # Final check - remove if it ends with dashes
            if cleaned and not cleaned.rstrip('-').strip() == '':
                cleaned = cleaned.rstrip('-').strip()
            if cleaned and len(cleaned) > 10:  # Only add meaningful suggestions
                cleaned_suggestions.append(cleaned)
        
        return cleaned_suggestions
    
    def _extract_quality_score(self, ai_analysis: str) -> float:
        """Extract quality score from AI analysis"""
        import re
        # Look for score patterns like "8/10", "score: 7", etc.
        score_patterns = [
            r'(\d+)/10',
            r'score[:\s]+(\d+)',
            r'quality[:\s]+(\d+)',
            r'rate[:\s]+(\d+)'
        ]
        
        for pattern in score_patterns:
            match = re.search(pattern, ai_analysis.lower())
            if match:
                score = float(match.group(1))
                return min(max(score, 0), 10)  # Clamp between 0 and 10
        
        return None

