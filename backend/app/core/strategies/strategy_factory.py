"""
Factory for creating appropriate code analyzer strategies
"""
from typing import Optional
from app.core.strategies.base import CodeAnalyzerStrategy
from app.core.strategies.python_analyzer import PythonAnalyzer
from app.core.strategies.javascript_analyzer import JavaScriptAnalyzer
from app.core.strategies.typescript_analyzer import TypeScriptAnalyzer
from app.core.strategies.generic_analyzer import GenericAnalyzer


class StrategyFactory:
    """Factory for creating code analyzer strategies"""
    
    _analyzers: list[CodeAnalyzerStrategy] = [
        PythonAnalyzer(),
        TypeScriptAnalyzer(),
        JavaScriptAnalyzer(),
        GenericAnalyzer()  # Always last as fallback
    ]
    
    @classmethod
    def get_analyzer(cls, file_extension: str) -> CodeAnalyzerStrategy:
        """
        Get appropriate analyzer for file extension
        
        Args:
            file_extension: File extension (e.g., '.py', '.js', '.ts')
            
        Returns:
            CodeAnalyzerStrategy instance
        """
        for analyzer in cls._analyzers:
            if analyzer.can_analyze(file_extension):
                return analyzer
        
        # Fallback to generic (should never reach here due to GenericAnalyzer)
        return GenericAnalyzer()
    
    @classmethod
    def get_supported_extensions(cls) -> list[str]:
        """Get list of supported file extensions"""
        extensions = []
        for analyzer in cls._analyzers:
            if hasattr(analyzer, 'SUPPORTED_EXTENSIONS'):
                extensions.extend(analyzer.SUPPORTED_EXTENSIONS)
        return list(set(extensions))

