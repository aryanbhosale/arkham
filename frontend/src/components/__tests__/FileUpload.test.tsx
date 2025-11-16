import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import FileUpload from '../FileUpload'

describe('FileUpload', () => {
  it('renders upload area', () => {
    const mockOnAnalysisComplete = vi.fn()
    render(<FileUpload onAnalysisComplete={mockOnAnalysisComplete} />)
    
    expect(screen.getByText(/drag & drop a code file/i)).toBeInTheDocument()
  })

  it('displays correct instructions', () => {
    const mockOnAnalysisComplete = vi.fn()
    render(<FileUpload onAnalysisComplete={mockOnAnalysisComplete} />)
    
    expect(screen.getByText(/supports: python, javascript, typescript/i)).toBeInTheDocument()
  })
})

