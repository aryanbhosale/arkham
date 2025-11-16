import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'

interface MarkdownRendererProps {
  content: string
  className?: string
}

export default function MarkdownRenderer({ content, className = '' }: MarkdownRendererProps) {
  // Clean up trailing dashes and horizontal rules more aggressively
  let cleanedContent = content
    // Remove horizontal rules at end of content (with or without newlines)
    .replace(/\n---+\s*$/g, '') // Trailing horizontal rules with newline
    .replace(/---+\s*$/g, '') // Trailing horizontal rules without newline
    // Remove standalone horizontal rules (surrounded by newlines)
    .replace(/\n---+\n/g, '\n\n')
    .replace(/\n---+\r\n/g, '\n\n')
    .replace(/\r\n---+\r\n/g, '\r\n\r\n')
    // Remove lines that are only dashes (3 or more)
    .replace(/^---+\s*$/gm, '')
    // Remove trailing dashes at the very end
    .replace(/---+\s*$/, '')
    // Clean up multiple consecutive newlines
    .replace(/\n{3,}/g, '\n\n')
    .trim()
  
  // Final pass: remove any remaining trailing dashes
  cleanedContent = cleanedContent.replace(/---+\s*$/, '').trim()
  
  return (
    <div className={`markdown-content ${className}`}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        className=""
        components={{
        code({ node, className, children, ...props }: any) {
          const match = /language-(\w+)/.exec(className || '')
          const codeString = String(children).replace(/\n$/, '')
          
          // Check if this is a code block (has multiple lines or is in a pre tag)
          const isCodeBlock = codeString.includes('\n') || codeString.length > 50 || (match && match[1])
          
          if (isCodeBlock) {
            // Detect language from className or content
            let language = 'text'
            if (match && match[1]) {
              language = match[1]
            } else {
              // Auto-detect language from content patterns
              const content = codeString.toLowerCase()
              if (content.includes('def ') || content.includes('class ') || content.includes('import ') || 
                  content.includes('@dataclass') || content.includes('raise ') || content.includes('-> none') ||
                  content.includes('// before:') || content.includes('// after:')) {
                language = 'python'
              } else if (content.includes('function ') || content.includes('const ') || content.includes('let ') || 
                         content.includes('export ') || content.includes('interface ') || content.includes('type ') ||
                         content.includes('// before') || content.includes('// after')) {
                language = 'javascript'
              } else if (content.includes('public ') || content.includes('private ') || content.includes('class ') && content.includes('{')) {
                language = 'java'
              }
            }
            
            return (
              <div className="code-block-wrapper my-4">
                <div className="code-block-header">
                  <span className="code-language">{language}</span>
                </div>
                <SyntaxHighlighter
                  style={vscDarkPlus}
                  language={language}
                  PreTag="div"
                  className="code-block-content"
                  customStyle={{
                    margin: 0,
                    borderRadius: 0,
                    padding: '1rem',
                    fontSize: '0.875rem',
                    lineHeight: '1.5',
                    background: '#1e1e1e',
                  } as React.CSSProperties}
                >
                  {codeString}
                </SyntaxHighlighter>
              </div>
            )
          }
          
          // Inline code
          return (
            <code className="inline-code" {...props}>
              {children}
            </code>
          )
        },
        pre({ children, ...props }: any) {
          // Check if pre contains a code element
          const codeElement = (children as any)?.props?.children
          if (codeElement && typeof codeElement === 'string' && (codeElement.includes('\n') || codeElement.length > 50)) {
            // This is a code block, let the code component handle it
            return <>{children}</>
          }
          return <pre {...props}>{children}</pre>
        },
        table({ children }) {
          return (
            <div className="overflow-x-auto my-4">
              <table>
                {children}
              </table>
            </div>
          )
        },
        a: ({ href, children }) => (
          <a href={href} target="_blank" rel="noopener noreferrer">
            {children}
          </a>
        ),
        hr: () => null, // Hide horizontal rules completely
        }}
      >
        {cleanedContent}
      </ReactMarkdown>
    </div>
  )
}

