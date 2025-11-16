"""
Tests for service layer
"""
import pytest
from app.services.code_service import CodeService
from app.core.config import settings
import os
import tempfile


class TestCodeService:
    """Tests for CodeService"""
    
    def test_validate_file_valid(self):
        service = CodeService()
        is_valid, error = service.validate_file('test.py', 1024)
        assert is_valid
        assert error is None
    
    def test_validate_file_invalid_extension(self):
        service = CodeService()
        is_valid, error = service.validate_file('test.exe', 1024)
        assert not is_valid
        assert error is not None
    
    def test_validate_file_too_large(self):
        service = CodeService()
        large_size = settings.MAX_FILE_SIZE + 1
        is_valid, error = service.validate_file('test.py', large_size)
        assert not is_valid
        assert error is not None

