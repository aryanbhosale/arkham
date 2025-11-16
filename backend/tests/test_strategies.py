"""
Tests for code analyzer strategies
"""
import pytest
from app.core.strategies.python_analyzer import PythonAnalyzer
from app.core.strategies.javascript_analyzer import JavaScriptAnalyzer
from app.core.strategies.typescript_analyzer import TypeScriptAnalyzer
from app.core.strategies.generic_analyzer import GenericAnalyzer
from app.core.strategies.strategy_factory import StrategyFactory


class TestPythonAnalyzer:
    """Tests for Python analyzer"""
    
    def test_can_analyze_python_files(self):
        analyzer = PythonAnalyzer()
        assert analyzer.can_analyze('.py')
        assert analyzer.can_analyze('.PY')
        assert not analyzer.can_analyze('.js')
    
    def test_analyze_simple_python_code(self):
        analyzer = PythonAnalyzer()
        code = """
def hello(name: str) -> str:
    \"\"\"Greet someone\"\"\"
    return f"Hello, {name}!"

class Greeter:
    def __init__(self, name: str):
        self.name = name
"""
        import asyncio
        result = asyncio.run(analyzer.analyze(code, "test.py"))
        
        assert result.language == "Python"
        assert len(result.functions) > 0
        assert len(result.classes) > 0
        assert result.complexity_score > 0


class TestJavaScriptAnalyzer:
    """Tests for JavaScript analyzer"""
    
    def test_can_analyze_javascript_files(self):
        analyzer = JavaScriptAnalyzer()
        assert analyzer.can_analyze('.js')
        assert analyzer.can_analyze('.jsx')
        assert not analyzer.can_analyze('.py')
    
    def test_analyze_simple_javascript_code(self):
        analyzer = JavaScriptAnalyzer()
        code = """
function greet(name) {
    return `Hello, ${name}!`;
}

const arrowFunc = (x) => x * 2;

class Calculator {
    add(a, b) {
        return a + b;
    }
}
"""
        import asyncio
        result = asyncio.run(analyzer.analyze(code, "test.js"))
        
        assert result.language == "JavaScript"
        assert len(result.functions) > 0
        assert result.complexity_score > 0


class TestTypeScriptAnalyzer:
    """Tests for TypeScript analyzer"""
    
    def test_can_analyze_typescript_files(self):
        analyzer = TypeScriptAnalyzer()
        assert analyzer.can_analyze('.ts')
        assert analyzer.can_analyze('.tsx')
        assert not analyzer.can_analyze('.js')
    
    def test_analyze_simple_typescript_code(self):
        analyzer = TypeScriptAnalyzer()
        code = """
interface User {
    name: string;
    age: number;
}

function greet(user: User): string {
    return `Hello, ${user.name}!`;
}
"""
        import asyncio
        result = asyncio.run(analyzer.analyze(code, "test.ts"))
        
        assert result.language == "TypeScript"
        assert result.complexity_score > 0


class TestGenericAnalyzer:
    """Tests for generic analyzer"""
    
    def test_can_analyze_any_file(self):
        analyzer = GenericAnalyzer()
        assert analyzer.can_analyze('.py')
        assert analyzer.can_analyze('.js')
        assert analyzer.can_analyze('.txt')
    
    def test_analyze_generic_code(self):
        analyzer = GenericAnalyzer()
        code = "Some code here\nfunction test() {}\nclass MyClass {}"
        import asyncio
        result = asyncio.run(analyzer.analyze(code, "test.txt"))
        
        assert result.language == "Generic"
        assert result.complexity_score >= 0


class TestStrategyFactory:
    """Tests for strategy factory"""
    
    def test_get_python_analyzer(self):
        analyzer = StrategyFactory.get_analyzer('.py')
        assert isinstance(analyzer, PythonAnalyzer)
    
    def test_get_javascript_analyzer(self):
        analyzer = StrategyFactory.get_analyzer('.js')
        assert isinstance(analyzer, JavaScriptAnalyzer)
    
    def test_get_typescript_analyzer(self):
        analyzer = StrategyFactory.get_analyzer('.ts')
        assert isinstance(analyzer, TypeScriptAnalyzer)
    
    def test_get_generic_analyzer_for_unknown(self):
        analyzer = StrategyFactory.get_analyzer('.unknown')
        assert isinstance(analyzer, GenericAnalyzer)

