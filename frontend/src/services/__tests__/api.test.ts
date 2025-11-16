import { describe, it, expect } from 'vitest'
import type { AnalysisResult, QuestionResponse, DocumentationResponse } from '../api'

describe('API Service Types', () => {
  it('should have correct AnalysisResult interface structure', () => {
    const mockResult: AnalysisResult = {
      filename: 'test.py',
      language: 'Python',
      file_extension: '.py',
      basic_analysis: {
        language: 'Python',
        complexity_score: 5.0,
        functions: [],
        classes: [],
        imports: [],
        summary: 'Test summary',
        suggestions: [],
        metrics: {}
      },
      ai_enhancement: {
        ai_insights: 'Test insights',
        enhanced_suggestions: [],
        code_quality_score: 8.0
      },
      code_preview: 'test code'
    }

    expect(mockResult.filename).toBe('test.py')
    expect(mockResult.language).toBe('Python')
    expect(mockResult.basic_analysis).toBeDefined()
    expect(mockResult.ai_enhancement).toBeDefined()
  })

  it('should have correct QuestionResponse interface structure', () => {
    const mockResponse: QuestionResponse = {
      answer: 'Test answer',
      question: 'Test question',
      language: 'Python'
    }

    expect(mockResponse.answer).toBe('Test answer')
    expect(mockResponse.question).toBe('Test question')
    expect(mockResponse.language).toBe('Python')
  })

  it('should have correct DocumentationResponse interface structure', () => {
    const mockResponse: DocumentationResponse = {
      filename: 'test.py',
      language: 'Python',
      documentation: 'Generated documentation'
    }

    expect(mockResponse.filename).toBe('test.py')
    expect(mockResponse.language).toBe('Python')
    expect(mockResponse.documentation).toBe('Generated documentation')
  })
})

