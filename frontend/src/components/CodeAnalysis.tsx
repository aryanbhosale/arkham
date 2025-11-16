import { Code2, Zap, TrendingUp, AlertTriangle, CheckCircle, FileText } from 'lucide-react'
import MarkdownRenderer from './MarkdownRenderer'
import { AnalysisResult } from '../services/api'

interface CodeAnalysisProps {
  result: AnalysisResult
}

export default function CodeAnalysis({ result }: CodeAnalysisProps) {
  const { basic_analysis, ai_enhancement, language } = result

  const getComplexityColor = (score: number) => {
    if (score < 3) return 'text-green-600'
    if (score < 6) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getQualityColor = (score: number | null) => {
    if (!score) return 'text-gray-600'
    if (score >= 8) return 'text-green-600'
    if (score >= 6) return 'text-yellow-600'
    return 'text-red-600'
  }

  return (
    <div className="space-y-6">
      {/* Overview Card */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4 flex items-center">
          <Code2 className="h-5 w-5 mr-2 text-primary-600" />
          Analysis Results
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600 mb-1">Language</p>
            <p className="text-lg font-semibold">{language}</p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600 mb-1">Complexity Score</p>
            <p className={`text-lg font-semibold ${getComplexityColor(basic_analysis.complexity_score)}`}>
              {basic_analysis.complexity_score.toFixed(1)}/10
            </p>
          </div>
          {ai_enhancement.code_quality_score !== null && (
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Quality Score</p>
              <p className={`text-lg font-semibold ${getQualityColor(ai_enhancement.code_quality_score)}`}>
                {ai_enhancement.code_quality_score.toFixed(1)}/10
              </p>
            </div>
          )}
        </div>

        {/* Metrics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <TrendingUp className="h-6 w-6 text-primary-600 mx-auto mb-2" />
            <p className="text-2xl font-bold">{basic_analysis.metrics.function_count || 0}</p>
            <p className="text-sm text-gray-600">Functions</p>
          </div>
          <div className="text-center">
            <FileText className="h-6 w-6 text-primary-600 mx-auto mb-2" />
            <p className="text-2xl font-bold">{basic_analysis.metrics.class_count || 0}</p>
            <p className="text-sm text-gray-600">Classes</p>
          </div>
          <div className="text-center">
            <Zap className="h-6 w-6 text-primary-600 mx-auto mb-2" />
            <p className="text-2xl font-bold">{basic_analysis.metrics.import_count || basic_analysis.imports.length}</p>
            <p className="text-sm text-gray-600">Imports</p>
          </div>
          <div className="text-center">
            <Code2 className="h-6 w-6 text-primary-600 mx-auto mb-2" />
            <p className="text-2xl font-bold">{basic_analysis.metrics.total_lines || 0}</p>
            <p className="text-sm text-gray-600">Lines</p>
          </div>
        </div>
      </div>

      {/* Functions & Classes */}
      {(basic_analysis.functions.length > 0 || basic_analysis.classes.length > 0) && (
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Code Structure</h3>

          {basic_analysis.functions.length > 0 && (
            <div className="mb-6">
              <h4 className="font-medium text-gray-700 mb-2">Functions</h4>
              <div className="space-y-2">
                {basic_analysis.functions.slice(0, 10).map((func, idx) => (
                  <div key={idx} className="bg-gray-50 p-3 rounded-lg">
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-sm font-medium">{func.name}</span>
                      <span className="text-xs text-gray-500">
                        Lines {func.line_start}-{func.line_end}
                      </span>
                    </div>
                    {func.parameters && func.parameters.length > 0 && (
                      <p className="text-xs text-gray-600 mt-1">
                        Parameters: {func.parameters.join(', ')}
                      </p>
                    )}
                    {func.docstring && (
                      <p className="text-xs text-gray-600 mt-1 italic">{func.docstring.substring(0, 100)}...</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {basic_analysis.classes.length > 0 && (
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Classes</h4>
              <div className="space-y-2">
                {basic_analysis.classes.slice(0, 10).map((cls, idx) => (
                  <div key={idx} className="bg-gray-50 p-3 rounded-lg">
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-sm font-medium">{cls.name}</span>
                      <span className="text-xs text-gray-500">
                        Lines {cls.line_start}-{cls.line_end}
                      </span>
                    </div>
                    {cls.methods && cls.methods.length > 0 && (
                      <p className="text-xs text-gray-600 mt-1">
                        Methods: {cls.methods.join(', ')}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* AI Insights */}
      {ai_enhancement.ai_insights && (
        <div className="card">
          <h3 className="text-lg font-semibold mb-4 flex items-center">
            <Zap className="h-5 w-5 mr-2 text-primary-600" />
            AI-Powered Insights
          </h3>
          <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
            <MarkdownRenderer content={ai_enhancement.ai_insights} />
          </div>
        </div>
      )}

      {/* Suggestions */}
      {(basic_analysis.suggestions.length > 0 || ai_enhancement.enhanced_suggestions.length > 0) && (
        <div className="card">
          <h3 className="text-lg font-semibold mb-4 flex items-center">
            <AlertTriangle className="h-5 w-5 mr-2 text-yellow-600" />
            Suggestions & Recommendations
          </h3>
          <div className="space-y-4">
            {basic_analysis.suggestions.map((suggestion, idx) => (
              <div key={idx} className="flex items-start bg-yellow-50 p-4 rounded-lg border border-yellow-200">
                <AlertTriangle className="h-4 w-4 text-yellow-600 mr-2 flex-shrink-0 mt-0.5" />
                <p className="text-sm text-yellow-800 flex-1">{suggestion}</p>
              </div>
            ))}
            {ai_enhancement.enhanced_suggestions.map((suggestion, idx) => (
              <div key={`ai-${idx}`} className="bg-blue-50 p-4 rounded-lg border border-blue-200 overflow-hidden">
                <div className="flex items-start mb-3">
                  <CheckCircle className="h-4 w-4 text-blue-600 mr-2 flex-shrink-0 mt-0.5" />
                  <span className="text-xs font-semibold text-blue-700 uppercase tracking-wide">AI Recommendation</span>
                </div>
                <div className="ml-6 -mr-2">
                  <MarkdownRenderer content={suggestion} />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

