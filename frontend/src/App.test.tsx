import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from './App'

describe('App', () => {
  it('renders CodeSage header', () => {
    render(<App />)
    expect(screen.getByText('CodeSage')).toBeInTheDocument()
  })

  it('renders navigation tabs', () => {
    render(<App />)
    expect(screen.getByText('Analyze Code')).toBeInTheDocument()
    expect(screen.getByText('Ask Questions')).toBeInTheDocument()
    expect(screen.getByText('Generate Docs')).toBeInTheDocument()
  })
})

