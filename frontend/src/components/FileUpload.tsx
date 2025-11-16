import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileCode, Loader2, AlertCircle } from 'lucide-react'
import { analyzeCode, AnalysisResult } from '../services/api'

interface FileUploadProps {
  onAnalysisComplete: (result: AnalysisResult, content: string) => void
}

export default function FileUpload({ onAnalysisComplete }: FileUploadProps) {
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (!file) return

    setUploadedFile(file)
    setIsUploading(true)
    setError(null)

    try {
      const result = await analyzeCode(file)
      
      // Read file content for preview
      const reader = new FileReader()
      reader.onload = (e) => {
        const content = e.target?.result as string
        onAnalysisComplete(result, content)
      }
      reader.readAsText(file)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze file. Please try again.')
    } finally {
      setIsUploading(false)
    }
  }, [onAnalysisComplete])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/*': ['.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.cpp', '.c', '.h', '.cs', '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.scala', '.r', '.sql', '.html', '.css', '.scss', '.json', '.yaml', '.yml', '.xml', '.md', '.txt'],
    },
    maxFiles: 1,
    disabled: isUploading,
  })

  return (
    <div className="card">
      <h2 className="text-xl font-semibold mb-4 flex items-center">
        <FileCode className="h-5 w-5 mr-2 text-primary-600" />
        Upload Code File
      </h2>

      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all ${
          isDragActive
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
        } ${isUploading ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
        <input {...getInputProps()} />
        
        {isUploading ? (
          <div className="flex flex-col items-center">
            <Loader2 className="h-12 w-12 text-primary-600 animate-spin mb-4" />
            <p className="text-gray-600">Analyzing code...</p>
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
                  Supports: Python, JavaScript, TypeScript, Java, C++, Go, Rust, and more
                </p>
              </>
            )}
          </div>
        )}
      </div>

      {uploadedFile && !isUploading && (
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
  )
}

