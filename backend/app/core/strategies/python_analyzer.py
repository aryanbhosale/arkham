"""
Python-specific code analyzer using AST parsing
"""
import ast
import re
from typing import Dict, Any, List
from app.core.strategies.base import CodeAnalyzerStrategy, AnalysisResult


class PythonAnalyzer(CodeAnalyzerStrategy):
    """Analyzer for Python code"""
    
    def can_analyze(self, file_extension: str) -> bool:
        """Check if file is Python"""
        return file_extension.lower() in ['.py', '.pyw']
    
    def get_language(self) -> str:
        """Return language name"""
        return "Python"
    
    async def analyze(self, code_content: str, filename: str) -> AnalysisResult:
        """Analyze Python code using AST"""
        try:
            tree = ast.parse(code_content)
        except SyntaxError:
            # Fallback to basic analysis if AST parsing fails
            return await self._basic_analysis(code_content, filename)
        
        functions = []
        classes = []
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = self._extract_function_info(node, code_content)
                functions.append(func_info)
            elif isinstance(node, ast.ClassDef):
                class_info = self._extract_class_info(node, code_content)
                classes.append(class_info)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                imports.append(ast.unparse(node))
        
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
            language="Python",
            complexity_score=complexity,
            functions=functions,
            classes=classes,
            imports=imports,
            summary=summary,
            suggestions=suggestions,
            metrics=metrics
        )
    
    def _extract_function_info(self, node: ast.FunctionDef, code_content: str) -> Dict[str, Any]:
        """Extract function information"""
        lines = code_content.split('\n')
        start_line = node.lineno - 1
        end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line + 10
        
        decorators = [ast.unparse(d) for d in node.decorator_list]
        args = [arg.arg for arg in node.args.args]
        
        docstring = ast.get_docstring(node) or ""
        
        return {
            "name": node.name,
            "line_start": start_line + 1,
            "line_end": end_line + 1,
            "parameters": args,
            "decorators": decorators,
            "docstring": docstring,
            "is_async": isinstance(node, ast.AsyncFunctionDef)
        }
    
    def _extract_class_info(self, node: ast.ClassDef, code_content: str) -> Dict[str, Any]:
        """Extract class information"""
        bases = [ast.unparse(b) for b in node.bases]
        decorators = [ast.unparse(d) for d in node.decorator_list]
        docstring = ast.get_docstring(node) or ""
        
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(item.name)
        
        return {
            "name": node.name,
            "line_start": node.lineno,
            "line_end": node.end_lineno if hasattr(node, 'end_lineno') else node.lineno + 10,
            "bases": bases,
            "decorators": decorators,
            "methods": methods,
            "docstring": docstring
        }
    
    def _generate_summary(self, functions: List[Dict], classes: List[Dict], imports: List[str]) -> str:
        """Generate code summary"""
        parts = []
        if classes:
            parts.append(f"{len(classes)} class(es)")
        if functions:
            parts.append(f"{len(functions)} function(s)")
        if imports:
            parts.append(f"{len(imports)} import(s)")
        
        if not parts:
            return "Empty Python file"
        
        return f"Python code with {', '.join(parts)}"
    
    def _generate_suggestions(self, functions: List[Dict], classes: List[Dict], code_content: str) -> List[str]:
        """Generate code improvement suggestions"""
        suggestions = []
        
        # Check for missing docstrings
        functions_without_docs = [f for f in functions if not f.get('docstring')]
        if functions_without_docs:
            suggestions.append(f"Consider adding docstrings to {len(functions_without_docs)} function(s)")
        
        # Check for long functions
        long_functions = [f for f in functions if (f['line_end'] - f['line_start']) > 50]
        if long_functions:
            suggestions.append(f"Consider refactoring {len(long_functions)} long function(s)")
        
        # Check for type hints
        if '->' not in code_content and ':' not in re.findall(r'def \w+\([^)]*\):', code_content):
            suggestions.append("Consider adding type hints for better code clarity")
        
        return suggestions
    
    def _avg_function_length(self, functions: List[Dict]) -> float:
        """Calculate average function length"""
        if not functions:
            return 0.0
        lengths = [f['line_end'] - f['line_start'] for f in functions]
        return sum(lengths) / len(lengths)
    
    async def _basic_analysis(self, code_content: str, filename: str) -> AnalysisResult:
        """Fallback basic analysis when AST parsing fails"""
        imports = self._extract_imports(code_content)
        complexity = self._calculate_complexity(code_content)
        
        # Extract function names using regex
        function_pattern = r'def\s+(\w+)\s*\('
        functions = [{"name": m.group(1), "line_start": 0, "line_end": 0} 
                    for m in re.finditer(function_pattern, code_content)]
        
        # Extract class names
        class_pattern = r'class\s+(\w+)'
        classes = [{"name": m.group(1), "line_start": 0, "line_end": 0}
                  for m in re.finditer(class_pattern, code_content)]
        
        return AnalysisResult(
            language="Python",
            complexity_score=complexity,
            functions=functions,
            classes=classes,
            imports=imports,
            summary=f"Python code with {len(functions)} function(s) and {len(classes)} class(es)",
            suggestions=["Code contains syntax errors - AST parsing failed"],
            metrics={"total_lines": len(code_content.split('\n'))}
        )

