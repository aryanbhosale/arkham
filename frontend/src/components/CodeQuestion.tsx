import { useState, useEffect } from 'react'
import { MessageSquare, Send, Loader2, Bot, User } from 'lucide-react'
import MarkdownRenderer from './MarkdownRenderer'
import { askQuestion, QuestionResponse } from '../services/api'

interface CodeQuestionProps {
  codeContent: string
  analysisResult?: any
}

export default function CodeQuestion({ codeContent, analysisResult }: CodeQuestionProps) {
  const [question, setQuestion] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [answers, setAnswers] = useState<QuestionResponse[]>([])
  // Use detected language from analysis if available, otherwise default to Generic
  const detectedLanguage = analysisResult?.language || 'Generic'
  const [language, setLanguage] = useState(detectedLanguage)
  
  // Update language when analysisResult changes
  useEffect(() => {
    if (analysisResult?.language) {
      setLanguage(analysisResult.language)
    }
  }, [analysisResult])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!question.trim() || !codeContent.trim()) {
      return
    }

    setIsLoading(true)
    try {
      const response = await askQuestion(question, codeContent, language)
      setAnswers([...answers, response])
      setQuestion('')
    } catch (error: any) {
      console.error('Error asking question:', error)
      alert('Failed to get answer. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="card">
        <h2 className="text-xl font-semibold mb-4 flex items-center">
          <MessageSquare className="h-5 w-5 mr-2 text-primary-600" />
          Ask Questions About Your Code
        </h2>

        {codeContent ? (
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Programming Language
            </label>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="input-field"
            >
              <option value="Generic">Auto-detect</option>
              <option value="Python">Python</option>
              <option value="JavaScript">JavaScript</option>
              <option value="TypeScript">TypeScript</option>
              <option value="Java">Java</option>
              <option value="C++">C++</option>
              <option value="Go">Go</option>
              <option value="Rust">Rust</option>
            </select>
          </div>
        ) : (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
            <p className="text-sm text-yellow-800 mb-2">
              💡 <strong>No code file available</strong>
            </p>
            <p className="text-sm text-yellow-700">
              Please upload and analyze a code file in the "Analyze Code" tab first to ask questions about it.
            </p>
          </div>
        )}

        {codeContent && (
          <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg">
            <p className="text-sm text-green-800 mb-1">
              ✓ <strong>Code file loaded:</strong> Ready to answer questions about your code
            </p>
            {analysisResult && (
              <p className="text-xs text-green-700">
                File: <strong>{analysisResult.filename}</strong> • Language: <strong>{analysisResult.language}</strong> • {codeContent.split('\n').length} lines
              </p>
            )}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Your Question
            </label>
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="e.g., What does this function do? How can I optimize this code? Explain this algorithm..."
              className="input-field min-h-[100px]"
              disabled={isLoading || !codeContent}
            />
          </div>

          <button
            type="submit"
            disabled={isLoading || !question.trim() || !codeContent}
            className="btn-primary flex items-center space-x-2"
          >
            {isLoading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                <span>Thinking...</span>
              </>
            ) : (
              <>
                <Send className="h-4 w-4" />
                <span>Ask Question</span>
              </>
            )}
          </button>
        </form>
      </div>

      {/* Answers */}
      {answers.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold">Conversation History</h3>
          {answers.map((answer, idx) => (
            <div key={idx} className="card space-y-4">
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0">
                  <div className="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center">
                    <User className="h-4 w-4 text-primary-600" />
                  </div>
                </div>
                <div className="flex-1">
                  <p className="font-medium text-gray-900 mb-1">You asked:</p>
                  <p className="text-gray-700">{answer.question}</p>
                </div>
              </div>

              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0">
                  <div className="h-8 w-8 rounded-full bg-green-100 flex items-center justify-center">
                    <Bot className="h-4 w-4 text-green-600" />
                  </div>
                </div>
                <div className="flex-1">
                  <p className="font-medium text-gray-900 mb-1">AI Response:</p>
                  <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                    <MarkdownRenderer content={answer.answer} />
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {answers.length === 0 && codeContent && (
        <div className="card bg-gray-50">
          <p className="text-center text-gray-600">
            Ask your first question to get started!
          </p>
        </div>
      )}
    </div>
  )
}

