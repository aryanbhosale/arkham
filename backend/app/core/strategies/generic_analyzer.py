"""
Generic code analyzer for unsupported languages
"""
from typing import Dict, Any, List
from app.core.strategies.base import CodeAnalyzerStrategy, AnalysisResult


class GenericAnalyzer(CodeAnalyzerStrategy):
    """Generic analyzer for any code file"""
    
    def can_analyze(self, file_extension: str) -> bool:
        """Can analyze any file type (fallback)"""
        return True
    
    def get_language(self) -> str:
        """Return generic language name"""
        return "Generic"
    
    async def analyze(self, code_content: str, filename: str) -> AnalysisResult:
        """Perform basic generic analysis"""
        imports = self._extract_imports(code_content)
        complexity = self._calculate_complexity(code_content)
        lines = code_content.split('\n')
        
        # Basic structure detection
        functions = []
        classes = []
        
        # Try to detect common patterns
        for i, line in enumerate(lines):
            stripped = line.strip()
            # Look for function-like patterns
            if any(keyword in stripped for keyword in ['function', 'def', 'fn ', 'func ']):
                if '(' in stripped:
                    func_name = stripped.split('(')[0].split()[-1] if stripped.split('(')[0].split() else "unknown"
                    functions.append({
                        "name": func_name,
                        "line_start": i + 1,
                        "line_end": i + 1
                    })
            # Look for class-like patterns
            if any(keyword in stripped for keyword in ['class ', 'struct ', 'interface ']):
                class_name = stripped.split()[1].split('{')[0].split(':')[0] if len(stripped.split()) > 1 else "unknown"
                classes.append({
                    "name": class_name,
                    "line_start": i + 1,
                    "line_end": i + 1
                })
        
        summary = f"Code file with {len(functions)} potential function(s) and {len(classes)} potential class(es)"
        suggestions = [
            "Consider using a language-specific analyzer for better insights"
        ]
        
        metrics = {
            "total_lines": len(lines),
            "non_empty_lines": len([l for l in lines if l.strip()]),
            "function_count": len(functions),
            "class_count": len(classes)
        }
        
        return AnalysisResult(
            language="Generic",
            complexity_score=complexity,
            functions=functions,
            classes=classes,
            imports=imports,
            summary=summary,
            suggestions=suggestions,
            metrics=metrics
        )

