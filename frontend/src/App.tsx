import { useState } from 'react'
import FileUpload from './components/FileUpload'
import CodeAnalysis from './components/CodeAnalysis'
import CodeQuestion from './components/CodeQuestion'
import DocumentationGenerator from './components/DocumentationGenerator'
import { FileText, MessageSquare, FileCheck, Sparkles } from 'lucide-react'

type Tab = 'analyze' | 'question' | 'documentation'

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('analyze')
  const [analysisResult, setAnalysisResult] = useState<any>(null)
  const [codeContent, setCodeContent] = useState<string>('')

  const tabs = [
    { id: 'analyze' as Tab, label: 'Analyze Code', icon: FileCheck },
    { id: 'question' as Tab, label: 'Ask Questions', icon: MessageSquare },
    { id: 'documentation' as Tab, label: 'Generate Docs', icon: FileText },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Sparkles className="h-8 w-8 text-primary-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">CodeSage</h1>
                <p className="text-sm text-gray-600">AI-Powered Code Understanding Platform</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6">
        <div className="flex space-x-1 bg-white p-1 rounded-lg shadow-sm border border-gray-200">
          {tabs.map((tab) => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex-1 flex items-center justify-center space-x-2 px-4 py-3 rounded-md transition-all ${
                  activeTab === tab.id
                    ? 'bg-primary-600 text-white shadow-md'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <Icon className="h-5 w-5" />
                <span className="font-medium">{tab.label}</span>
              </button>
            )
          })}
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'analyze' && (
          <div className="space-y-6">
            <FileUpload
              onAnalysisComplete={(result, content) => {
                setAnalysisResult(result)
                setCodeContent(content)
              }}
            />
            {analysisResult && (
              <CodeAnalysis result={analysisResult} />
            )}
          </div>
        )}

        {activeTab === 'question' && (
          <CodeQuestion 
            codeContent={codeContent}
            analysisResult={analysisResult}
          />
        )}

        {activeTab === 'documentation' && (
          <DocumentationGenerator 
            codeContent={codeContent}
            analysisResult={analysisResult}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="mt-16 bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <p className="text-center text-gray-600 text-sm">
            Powered by Mistral AI • Built with React, TypeScript, FastAPI, and vLLM
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App

