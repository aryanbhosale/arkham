"""
JavaScript/TypeScript code analyzer
"""
import re
from typing import Dict, Any, List
from app.core.strategies.base import CodeAnalyzerStrategy, AnalysisResult


class JavaScriptAnalyzer(CodeAnalyzerStrategy):
    """Analyzer for JavaScript code"""
    
    def can_analyze(self, file_extension: str) -> bool:
        """Check if file is JavaScript"""
        return file_extension.lower() in ['.js', '.jsx']
    
    def get_language(self) -> str:
        """Return language name"""
        return "JavaScript"
    
    async def analyze(self, code_content: str, filename: str) -> AnalysisResult:
        """Analyze JavaScript code"""
        imports = self._extract_imports(code_content)
        functions = self._extract_functions(code_content)
        classes = self._extract_classes(code_content)
        complexity = self._calculate_complexity(code_content)
        
        summary = self._generate_summary(functions, classes, imports)
        suggestions = self._generate_suggestions(functions, classes, code_content)
        
        metrics = {
            "total_lines": len(code_content.split('\n')),
            "function_count": len(functions),
            "class_count": len(classes),
            "import_count": len(imports),
            "average_function_length": self._avg_function_length(functions)
        }
        
        return AnalysisResult(
            language="JavaScript",
            complexity_score=complexity,
            functions=functions,
            classes=classes,
            imports=imports,
            summary=summary,
            suggestions=suggestions,
            metrics=metrics
        )
    
    def _extract_imports(self, code_content: str) -> List[str]:
        """Extract ES6 imports and require statements"""
        imports = []
        import_pattern = r'(?:import\s+.*?from\s+[\'"][^\'"]+[\'"]|require\s*\([\'"][^\'"]+[\'"]\))'
        for match in re.finditer(import_pattern, code_content):
            imports.append(match.group(0))
        return imports
    
    def _extract_functions(self, code_content: str) -> List[Dict[str, Any]]:
        """Extract function definitions"""
        functions = []
        lines = code_content.split('\n')
        
        # Match various function patterns
        patterns = [
            (r'(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(', 'function'),
            (r'const\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>', 'arrow'),
            (r'(\w+)\s*:\s*(?:async\s+)?\([^)]*\)\s*=>', 'method'),
        ]
        
        for i, line in enumerate(lines):
            for pattern, func_type in patterns:
                match = re.search(pattern, line)
                if match:
                    functions.append({
                        "name": match.group(1),
                        "line_start": i + 1,
                        "line_end": i + 1,  # Simplified
                        "type": func_type
                    })
                    break
        
        return functions
    
    def _extract_classes(self, code_content: str) -> List[Dict[str, Any]]:
        """Extract class definitions"""
        classes = []
        lines = code_content.split('\n')
        
        class_pattern = r'(?:export\s+)?class\s+(\w+)'
        for i, line in enumerate(lines):
            match = re.search(class_pattern, line)
            if match:
                # Extract methods
                methods = []
                for j in range(i + 1, min(i + 100, len(lines))):
                    method_match = re.search(r'(\w+)\s*\([^)]*\)\s*{', lines[j])
                    if method_match:
                        methods.append(method_match.group(1))
                    if lines[j].strip() == '}':
                        break
                
                classes.append({
                    "name": match.group(1),
                    "line_start": i + 1,
                    "line_end": i + 1,
                    "methods": methods
                })
        
        return classes
    
    def _generate_summary(self, functions: List[Dict], classes: List[Dict], imports: List[str]) -> str:
        """Generate code summary"""
        parts = []
        if classes:
            parts.append(f"{len(classes)} class(es)")
        if functions:
            parts.append(f"{len(functions)} function(s)")
        if imports:
            parts.append(f"{len(imports)} import(s)")
        
        return f"JavaScript code with {', '.join(parts) if parts else 'no structures detected'}"
    
    def _generate_suggestions(self, functions: List[Dict], classes: List[Dict], code_content: str) -> List[str]:
        """Generate suggestions"""
        suggestions = []
        
        # Check for console.logs (might want to remove in production)
        if 'console.log' in code_content:
            suggestions.append("Consider removing console.log statements for production")
        
        # Check for var usage
        if re.search(r'\bvar\s+', code_content):
            suggestions.append("Consider using 'const' or 'let' instead of 'var'")
        
        return suggestions
    
    def _avg_function_length(self, functions: List[Dict]) -> float:
        """Calculate average function length"""
        if not functions:
            return 0.0
        lengths = [f.get('line_end', 0) - f.get('line_start', 0) for f in functions]
        return sum(lengths) / len(lengths) if lengths else 0.0

