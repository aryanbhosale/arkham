"""
API routes for CodeSage
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
import os
import aiofiles
from pathlib import Path
from typing import Optional
from app.services.code_service import CodeService
from app.core.config import settings
from app.core.logging import setup_logging

logger = setup_logging()
router = APIRouter()
code_service = CodeService()

# Ensure upload directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.TEMP_DIR, exist_ok=True)


@router.post("/analyze")
async def analyze_code(file: UploadFile = File(...)):
    """
    Analyze uploaded code file
    
    Args:
        file: Uploaded code file
        
    Returns:
        Analysis results
    """
    try:
        # Validate file
        file_size = 0
        content = await file.read()
        file_size = len(content)
        
        is_valid, error_msg = code_service.validate_file(file.filename, file_size)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Save file temporarily
        file_path = os.path.join(settings.TEMP_DIR, file.filename)
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        try:
            # Analyze file
            result = await code_service.analyze_code_file(file_path, file.filename)
            return JSONResponse(content=result)
        finally:
            # Clean up temp file
            if os.path.exists(file_path):
                os.remove(file_path)
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/question")
async def ask_question(
    question: str = Form(...),
    code_content: str = Form(...),
    language: str = Form("Generic")
):
    """
    Answer questions about code
    
    Args:
        question: User's question
        code_content: Code context
        language: Programming language
        
    Returns:
        Answer to the question
    """
    try:
        if not question or not question.strip():
            raise HTTPException(status_code=400, detail="Question is required")
        
        if not code_content or not code_content.strip():
            raise HTTPException(status_code=400, detail="Code content is required")
        
        result = await code_service.answer_code_question(
            question.strip(),
            code_content,
            language
        )
        
        return JSONResponse(content=result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in question endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to answer question: {str(e)}")


@router.post("/documentation")
async def generate_documentation(file: UploadFile = File(...)):
    """
    Generate documentation for code file
    
    Args:
        file: Uploaded code file
        
    Returns:
        Generated documentation
    """
    try:
        # Validate file
        content = await file.read()
        file_size = len(content)
        
        is_valid, error_msg = code_service.validate_file(file.filename, file_size)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Save file temporarily
        file_path = os.path.join(settings.TEMP_DIR, file.filename)
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        try:
            # Generate documentation
            result = await code_service.generate_documentation(file_path, file.filename)
            return JSONResponse(content=result)
        finally:
            # Clean up temp file
            if os.path.exists(file_path):
                os.remove(file_path)
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in documentation endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Documentation generation failed: {str(e)}")


@router.get("/supported-extensions")
async def get_supported_extensions():
    """Get list of supported file extensions"""
    from app.core.strategies.strategy_factory import StrategyFactory
    return JSONResponse(content={
        "extensions": settings.ALLOWED_EXTENSIONS,
        "max_file_size_mb": settings.MAX_FILE_SIZE / 1024 / 1024
    })

