"""
TypeScript-specific code analyzer
"""
import re
from typing import Dict, Any, List
from app.core.strategies.base import CodeAnalyzerStrategy, AnalysisResult


class TypeScriptAnalyzer(CodeAnalyzerStrategy):
    """Analyzer for TypeScript code"""
    
    def can_analyze(self, file_extension: str) -> bool:
        """Check if file is TypeScript"""
        return file_extension.lower() in ['.ts', '.tsx']
    
    def get_language(self) -> str:
        """Return language name"""
        return "TypeScript"
    
    async def analyze(self, code_content: str, filename: str) -> AnalysisResult:
        """Analyze TypeScript code"""
        imports = self._extract_imports(code_content)
        interfaces = self._extract_interfaces(code_content)
        types = self._extract_types(code_content)
        functions = self._extract_functions(code_content)
        classes = self._extract_classes(code_content)
        complexity = self._calculate_complexity(code_content)
        
        summary = self._generate_summary(functions, classes, imports, interfaces, types)
        suggestions = self._generate_suggestions(functions, classes, code_content, interfaces, types)
        
        metrics = {
            "total_lines": len(code_content.split('\n')),
            "function_count": len(functions),
            "class_count": len(classes),
            "interface_count": len(interfaces),
            "type_count": len(types),
            "import_count": len(imports)
        }
        
        return AnalysisResult(
            language="TypeScript",
            complexity_score=complexity,
            functions=functions,
            classes=classes,
            imports=imports,
            summary=summary,
            suggestions=suggestions,
            metrics=metrics
        )
    
    def _extract_imports(self, code_content: str) -> List[str]:
        """Extract TypeScript imports"""
        imports = []
        import_pattern = r'import\s+.*?from\s+[\'"][^\'"]+[\'"]'
        for match in re.finditer(import_pattern, code_content):
            imports.append(match.group(0))
        return imports
    
    def _extract_interfaces(self, code_content: str) -> List[Dict[str, Any]]:
        """Extract interface definitions"""
        interfaces = []
        interface_pattern = r'(?:export\s+)?interface\s+(\w+)'
        for match in re.finditer(interface_pattern, code_content):
            interfaces.append({
                "name": match.group(1),
                "type": "interface"
            })
        return interfaces
    
    def _extract_types(self, code_content: str) -> List[Dict[str, Any]]:
        """Extract type definitions"""
        types = []
        type_pattern = r'(?:export\s+)?type\s+(\w+)'
        for match in re.finditer(type_pattern, code_content):
            types.append({
                "name": match.group(1),
                "type": "type"
            })
        return types
    
    def _extract_functions(self, code_content: str) -> List[Dict[str, Any]]:
        """Extract function definitions"""
        functions = []
        lines = code_content.split('\n')
        
        # Match TypeScript function patterns
        patterns = [
            (r'(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*<[^>]*>?\s*\(', 'function'),
            (r'const\s+(\w+)\s*[:=]\s*(?:async\s+)?\([^)]*\)\s*[:=]\s*>', 'arrow'),
            (r'(\w+)\s*[:]\s*(?:async\s+)?\([^)]*\)\s*[:=]\s*>', 'method'),
        ]
        
        for i, line in enumerate(lines):
            for pattern, func_type in patterns:
                match = re.search(pattern, line)
                if match:
                    functions.append({
                        "name": match.group(1),
                        "line_start": i + 1,
                        "line_end": i + 1,
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
                methods = []
                for j in range(i + 1, min(i + 100, len(lines))):
                    method_match = re.search(r'(?:public|private|protected)?\s*(\w+)\s*\([^)]*\)\s*[:{]', lines[j])
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
    
    def _generate_summary(self, functions: List[Dict], classes: List[Dict], 
                         imports: List[str], interfaces: List[Dict], types: List[Dict]) -> str:
        """Generate code summary"""
        parts = []
        if classes:
            parts.append(f"{len(classes)} class(es)")
        if functions:
            parts.append(f"{len(functions)} function(s)")
        if interfaces:
            parts.append(f"{len(interfaces)} interface(s)")
        if types:
            parts.append(f"{len(types)} type(s)")
        if imports:
            parts.append(f"{len(imports)} import(s)")
        
        return f"TypeScript code with {', '.join(parts) if parts else 'no structures detected'}"
    
    def _generate_suggestions(self, functions: List[Dict], classes: List[Dict], 
                            code_content: str, interfaces: List[Dict], types: List[Dict]) -> List[str]:
        """Generate suggestions"""
        suggestions = []
        
        # Check for any types
        if not interfaces and not types:
            suggestions.append("Consider adding TypeScript interfaces or types for better type safety")
        
        # Check for explicit return types
        if re.search(r'function\s+\w+\s*\([^)]*\)\s*{', code_content):
            suggestions.append("Consider adding explicit return types to functions")
        
        return suggestions

