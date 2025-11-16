/**
 * API service for communicating with CodeSage backend
 */
import axios from 'axios'

// In Docker, use relative path for API calls (nginx will proxy)
// In development, use full URL
const API_BASE_URL = import.meta.env.VITE_API_URL || (import.meta.env.PROD === true ? '/api/v1' : 'http://localhost:8000/api/v1')

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface AnalysisResult {
  filename: string
  language: string
  file_extension: string
  basic_analysis: {
    language: string
    complexity_score: number
    functions: Array<{
      name: string
      line_start: number
      line_end: number
      parameters?: string[]
      docstring?: string
    }>
    classes: Array<{
      name: string
      line_start: number
      line_end: number
      methods?: string[]
    }>
    imports: string[]
    summary: string
    suggestions: string[]
    metrics: Record<string, any>
  }
  ai_enhancement: {
    ai_insights: string
    enhanced_suggestions: string[]
    code_quality_score: number | null
  }
  code_preview: string
}

export interface QuestionResponse {
  answer: string
  question: string
  language: string
}

export interface DocumentationResponse {
  filename: string
  language: string
  documentation: string
}

/**
 * Analyze uploaded code file
 */
export const analyzeCode = async (file: File): Promise<AnalysisResult> => {
  const formData = new FormData()
  formData.append('file', file)

  const response = await api.post<AnalysisResult>('/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return response.data
}

/**
 * Ask a question about code
 */
export const askQuestion = async (
  question: string,
  codeContent: string,
  language: string = 'Generic'
): Promise<QuestionResponse> => {
  const formData = new FormData()
  formData.append('question', question)
  formData.append('code_content', codeContent)
  formData.append('language', language)

  const response = await api.post<QuestionResponse>('/question', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return response.data
}

/**
 * Generate documentation for code file
 */
export const generateDocumentation = async (file: File): Promise<DocumentationResponse> => {
  const formData = new FormData()
  formData.append('file', file)

  const response = await api.post<DocumentationResponse>('/documentation', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return response.data
}

/**
 * Get supported file extensions
 */
export const getSupportedExtensions = async (): Promise<{
  extensions: string[]
  max_file_size_mb: number
}> => {
  const response = await api.get('/supported-extensions')
  return response.data
}

export default api

