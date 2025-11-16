import { useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { FileText, Upload, Loader2, Download, AlertCircle, CheckCircle } from 'lucide-react'
import MarkdownRenderer from './MarkdownRenderer'
import { generateDocumentation, DocumentationResponse } from '../services/api'

interface DocumentationGeneratorProps {
  codeContent?: string
  analysisResult?: any
}

export default function DocumentationGenerator({ codeContent, analysisResult }: DocumentationGeneratorProps) {
  const [isGenerating, setIsGenerating] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [documentation, setDocumentation] = useState<DocumentationResponse | null>(null)
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)

  const onDrop = async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (!file) return

    setUploadedFile(file)
    setIsGenerating(true)
    setError(null)
    setDocumentation(null)

    try {
      const result = await generateDocumentation(file)
      setDocumentation(result)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate documentation. Please try again.')
    } finally {
      setIsGenerating(false)
    }
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/*': ['.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.cpp', '.c', '.h', '.cs', '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.scala', '.r', '.sql', '.html', '.css', '.scss', '.json', '.yaml', '.yml', '.xml', '.md', '.txt'],
    },
    maxFiles: 1,
    disabled: isGenerating,
  })

  const generateFromAnalyzedCode = async () => {
    if (!codeContent || !analysisResult) return

    setIsGenerating(true)
    setError(null)
    setDocumentation(null)

    try {
      // Create a File object from the code content
      const filename = analysisResult.filename || 'code.py'
      const blob = new Blob([codeContent], { type: 'text/plain' })
      const file = new File([blob], filename, { type: 'text/plain' })
      
      const result = await generateDocumentation(file)
      setDocumentation(result)
      setUploadedFile(file)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate documentation. Please try again.')
    } finally {
      setIsGenerating(false)
    }
  }

  const downloadDocumentation = () => {
    if (!documentation) return

    const blob = new Blob([documentation.documentation], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${documentation.filename.replace(/\.[^/.]+$/, '')}_documentation.md`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <div className="space-y-6">
      <div className="card">
        <h2 className="text-xl font-semibold mb-4 flex items-center">
          <FileText className="h-5 w-5 mr-2 text-primary-600" />
          Generate Documentation
        </h2>

        <p className="text-gray-600 mb-6">
          Generate comprehensive documentation for your code including
          function descriptions, usage examples, and code structure.
        </p>

        {/* Show analyzed file option if available */}
        {codeContent && analysisResult && (
          <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
            <div className="flex items-start justify-between">
              <div className="flex items-start">
                <CheckCircle className="h-5 w-5 text-green-600 mr-3 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <p className="font-medium text-green-900 mb-1">Code file available from analysis</p>
                  <p className="text-sm text-green-700 mb-3">
                    File: <strong>{analysisResult.filename}</strong> ({analysisResult.language})
                  </p>
                  <button
                    onClick={generateFromAnalyzedCode}
                    disabled={isGenerating}
                    className="btn-primary text-sm"
                  >
                    {isGenerating ? (
                      <>
                        <Loader2 className="h-4 w-4 mr-2 animate-spin inline" />
                        Generating...
                      </>
                    ) : (
                      <>
                        <FileText className="h-4 w-4 mr-2 inline" />
                        Generate Documentation for Analyzed File
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {(!codeContent || !analysisResult) && (
          <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-sm text-blue-800 mb-2">
              💡 <strong>Tip:</strong> Upload and analyze a code file in the "Analyze Code" tab first to use it here automatically.
            </p>
            <p className="text-sm text-blue-700">
              Or upload a new file below to generate documentation.
            </p>
          </div>
        )}

        <div className="mb-4">
          <p className="text-sm font-medium text-gray-700 mb-2">Or upload a different file:</p>
        </div>

        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all ${
            isDragActive
              ? 'border-primary-500 bg-primary-50'
              : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
          } ${isGenerating ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          <input {...getInputProps()} />
          
          {isGenerating ? (
            <div className="flex flex-col items-center">
              <Loader2 className="h-12 w-12 text-primary-600 animate-spin mb-4" />
              <p className="text-gray-600">Generating documentation...</p>
              <p className="text-sm text-gray-500 mt-2">This may take a few moments</p>
            </div>
          ) : (
            <div className="flex flex-col items-center">
              <Upload className="h-12 w-12 text-gray-400 mb-4" />
              {isDragActive ? (
                <p className="text-primary-600 font-medium">Drop the file here</p>
              ) : (
                <>
                  <p className="text-gray-700 mb-2">
                    Drag & drop a code file here, or click to select
                  </p>
                  <p className="text-sm text-gray-500">
                    AI will analyze your code and generate comprehensive documentation
                  </p>
                </>
              )}
            </div>
          )}
        </div>

        {uploadedFile && !isGenerating && (
          <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
            <p className="text-sm text-green-800">
              <strong>File:</strong> {uploadedFile.name} ({(uploadedFile.size / 1024).toFixed(2)} KB)
            </p>
          </div>
        )}

        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-start">
            <AlertCircle className="h-5 w-5 text-red-600 mr-2 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}
      </div>

      {/* Generated Documentation */}
      {documentation && (
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold flex items-center">
              <FileText className="h-5 w-5 mr-2 text-primary-600" />
              Generated Documentation
            </h3>
            <button
              onClick={downloadDocumentation}
              className="btn-secondary flex items-center space-x-2"
            >
              <Download className="h-4 w-4" />
              <span>Download</span>
            </button>
          </div>

          <div className="mb-4 p-3 bg-gray-50 rounded-lg">
            <p className="text-sm text-gray-600">
              <strong>File:</strong> {documentation.filename} | <strong>Language:</strong> {documentation.language}
            </p>
          </div>

          <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
            <MarkdownRenderer content={documentation.documentation} />
          </div>
        </div>
      )}
    </div>
  )
}

