"""
Base strategy interface for code analysis
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel


class AnalysisResult(BaseModel):
    """Standard analysis result structure"""
    language: str
    complexity_score: float
    functions: List[Dict[str, Any]]
    classes: List[Dict[str, Any]]
    imports: List[str]
    summary: str
    suggestions: List[str]
    metrics: Dict[str, Any]


class CodeAnalyzerStrategy(ABC):
    """Abstract base class for code analyzers"""
    
    @abstractmethod
    def can_analyze(self, file_extension: str) -> bool:
        """Check if this analyzer can handle the file type"""
        pass
    
    @abstractmethod
    async def analyze(self, code_content: str, filename: str) -> AnalysisResult:
        """Analyze code and return structured results"""
        pass
    
    @abstractmethod
    def get_language(self) -> str:
        """Get the language this analyzer handles"""
        pass
    
    def _extract_imports(self, code_content: str) -> List[str]:
        """Extract import statements (can be overridden by subclasses)"""
        imports = []
        for line in code_content.split('\n'):
            line = line.strip()
            if line.startswith('import ') or line.startswith('from '):
                imports.append(line)
        return imports
    
    def _calculate_complexity(self, code_content: str) -> float:
        """Calculate basic complexity score"""
        lines = [l.strip() for l in code_content.split('\n') if l.strip()]
        if not lines:
            return 0.0
        
        # Simple complexity: lines, control structures, nesting
        control_keywords = ['if', 'else', 'elif', 'for', 'while', 'switch', 'case', 'try', 'except', 'catch']
        complexity = len(lines) * 0.1
        
        for line in lines:
            for keyword in control_keywords:
                if keyword in line:
                    complexity += 0.5
            # Count nesting (indentation)
            indent_level = len(line) - len(line.lstrip())
            complexity += indent_level * 0.1
        
        return min(complexity, 10.0)  # Cap at 10

