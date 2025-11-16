"""
Code analysis service - orchestrates code analysis workflow
"""
import os
import aiofiles
from pathlib import Path
from typing import Dict, Any, Optional
from app.core.strategies.strategy_factory import StrategyFactory
from app.services.mistral_service import MistralService
from app.core.config import settings
from app.core.logging import setup_logging

logger = setup_logging()


class CodeService:
    """Service for code analysis operations"""
    
    def __init__(self):
        """Initialize service with dependencies"""
        self.mistral_service = MistralService()
        self.strategy_factory = StrategyFactory()
    
    async def analyze_code_file(self, file_path: str, filename: str) -> Dict[str, Any]:
        """
        Analyze a code file using appropriate strategy and AI
        
        Args:
            file_path: Path to uploaded file
            filename: Original filename
            
        Returns:
            Complete analysis results
        """
        try:
            # Read file content
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                code_content = await f.read()
            
            # Get file extension
            file_extension = Path(filename).suffix
            
            # Get appropriate analyzer
            analyzer = self.strategy_factory.get_analyzer(file_extension)
            language = analyzer.get_language()
            
            # Perform basic analysis
            analysis_result = await analyzer.analyze(code_content, filename)
            analysis_dict = analysis_result.model_dump()
            
            # Enhance with AI analysis
            ai_enhancement = await self.mistral_service.analyze_code_with_ai(
                code_content,
                language,
                analysis_dict
            )
            
            # Combine results
            return {
                "filename": filename,
                "language": language,
                "file_extension": file_extension,
                "basic_analysis": analysis_dict,
                "ai_enhancement": ai_enhancement,
                "code_preview": code_content[:500]  # First 500 chars for preview
            }
        except Exception as e:
            logger.error(f"Error analyzing code file: {str(e)}")
            raise
    
    async def answer_code_question(self, question: str, code_content: str, 
                                   language: str) -> Dict[str, str]:
        """
        Answer questions about code
        
        Args:
            question: User's question
            code_content: Code context
            language: Programming language
            
        Returns:
            Answer dictionary
        """
        return await self.mistral_service.answer_question(question, code_content, language)
    
    async def generate_documentation(self, file_path: str, filename: str) -> Dict[str, str]:
        """
        Generate documentation for code file
        
        Args:
            file_path: Path to file
            filename: Original filename
            
        Returns:
            Generated documentation
        """
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                code_content = await f.read()
            
            file_extension = Path(filename).suffix
            analyzer = self.strategy_factory.get_analyzer(file_extension)
            language = analyzer.get_language()
            
            analysis_result = await analyzer.analyze(code_content, filename)
            
            documentation = await self.mistral_service.generate_documentation(
                code_content,
                language,
                analysis_result.model_dump()
            )
            
            return {
                "filename": filename,
                "language": language,
                "documentation": documentation
            }
        except Exception as e:
            logger.error(f"Error generating documentation: {str(e)}")
            raise
    
    def validate_file(self, filename: str, file_size: int) -> tuple[bool, Optional[str]]:
        """
        Validate uploaded file
        
        Args:
            filename: File name
            file_size: File size in bytes
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check file extension
        file_extension = Path(filename).suffix.lower()
        if file_extension not in settings.ALLOWED_EXTENSIONS:
            return False, f"File type {file_extension} not supported"
        
        # Check file size
        if file_size > settings.MAX_FILE_SIZE:
            return False, f"File size exceeds maximum of {settings.MAX_FILE_SIZE / 1024 / 1024}MB"
        
        return True, None

