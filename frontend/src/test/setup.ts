import '@testing-library/jest-dom'
import { afterEach, beforeAll } from 'vitest'
import { cleanup } from '@testing-library/react'

// Set NODE_ENV to test to avoid React production build issues
beforeAll(() => {
  process.env.NODE_ENV = 'test'
})

// Cleanup after each test
afterEach(() => {
  cleanup()
})

