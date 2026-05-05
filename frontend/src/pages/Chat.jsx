/**
 * @file Chat.jsx
 * @description AI Tutor chat page for EduMind AI.
 *              Connects to 16 RAG pipelines via ragService.
 *              Students type questions and get AI-powered answers.
 *              Supports switching between all 16 RAG pipeline types.
 */
import { useState, useRef, useEffect } from 'react'
import ragService from '../services/ragService'

// ─── Available RAG Pipelines ──────────────────────────────────────────────────
const RAG_PIPELINES = [
  { value: 'naive',            label: 'Naive RAG' },
  { value: 'hyde',             label: 'HyDE RAG' },
  { value: 'fusion',           label: 'Fusion RAG' },
  { value: 'rerank',           label: 'ReRank RAG' },
  { value: 'contextual',       label: 'Contextual RAG' },
  { value: 'speculative',      label: 'Speculative RAG' },
  { value: 'sentence_window',  label: 'Sentence Window' },
  { value: 'graph',            label: 'Graph RAG' },
]

// ─── Single Message Bubble ────────────────────────────────────────────────────
const MessageBubble = ({ message }) => (
  <div className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} mb-4`}>
    <div className={`
      max-w-2xl px-4 py-3 rounded-2xl text-sm leading-relaxed
      ${message.role === 'user'
        ? 'bg-blue-600 text-white rounded-br-sm'
        : 'bg-gray-800 text-gray-100 rounded-bl-sm border border-gray-700'
      }
    `}>
      {/* Role label */}
      <p className={`text-xs font-semibold mb-1 
        ${message.role === 'user' ? 'text-blue-200' : 'text-green-400'}`}>
        {message.role === 'user' ? '👤 You' : '🤖 EduMind AI'}
      </p>
      {/* Message text */}
      <p className="whitespace-pre-wrap">{message.content}</p>
      {/* Pipeline badge */}
      {message.pipeline && (
        <span className="mt-2 inline-block text-xs bg-gray-700
          text-gray-300 px-2 py-0.5 rounded-full">
          {message.pipeline}
        </span>
      )}
    </div>
  </div>
)

// ─── Chat Page ────────────────────────────────────────────────────────────────
const Chat = () => {
  const [messages, setMessages]         = useState([])
  const [input, setInput]               = useState('')
  const [loading, setLoading]           = useState(false)
  const [selectedPipeline, setPipeline] = useState('naive')
  const [error, setError]               = useState(null)
  const bottomRef                       = useRef(null)

  // Auto scroll to bottom on new message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // ─── Send Message ───────────────────────────────────────────────────────────
  const handleSend = async () => {
    if (!input.trim() || loading) return
    setError(null)

    // Add user message to chat
    const userMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      // Call RAG pipeline via service
      const result = await ragService.query(input, selectedPipeline)

      // Add AI response to chat
      const aiMessage = {
        role: 'assistant',
        content: result.answer || result.response || JSON.stringify(result),
        pipeline: selectedPipeline,
      }
      setMessages(prev => [...prev, aiMessage])
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  // Send on Enter key
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="max-w-4xl mx-auto h-full flex flex-col">

      {/* ── Header ── */}
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">🤖 AI Tutor</h1>
          <p className="text-gray-400 text-sm">
            Powered by 16 RAG pipelines + Groq Llama-3
          </p>
        </div>

        {/* Pipeline Selector */}
        <select
          value={selectedPipeline}
          onChange={(e) => setPipeline(e.target.value)}
          className="bg-gray-800 border border-gray-700 text-white
            text-sm rounded-lg px-3 py-2 focus:outline-none
            focus:border-blue-500"
        >
          {RAG_PIPELINES.map(p => (
            <option key={p.value} value={p.value}>{p.label}</option>
          ))}
        </select>
      </div>

      {/* ── Chat Messages ── */}
      <div className="flex-1 overflow-y-auto bg-gray-900 rounded-xl
        border border-gray-800 p-4 mb-4">

        {/* Empty state */}
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center
            justify-center text-center">
            <span className="text-6xl mb-4">🧠</span>
            <h3 className="text-white font-semibold text-lg">
              Ask me anything!
            </h3>
            <p className="text-gray-400 text-sm mt-2 max-w-md">
              I'm powered by {selectedPipeline} RAG pipeline.
              Upload your study materials and ask questions about them.
            </p>
          </div>
        )}

        {/* Messages */}
        {messages.map((msg, idx) => (
          <MessageBubble key={idx} message={msg} />
        ))}

        {/* Loading indicator */}
        {loading && (
          <div className="flex justify-start mb-4">
            <div className="bg-gray-800 border border-gray-700
              px-4 py-3 rounded-2xl rounded-bl-sm">
              <p className="text-xs text-green-400 font-semibold mb-1">
                🤖 EduMind AI
              </p>
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" />
                <span className="w-2 h-2 bg-blue-400 rounded-full animate-bounce [animation-delay:0.1s]" />
                <span className="w-2 h-2 bg-blue-400 rounded-full animate-bounce [animation-delay:0.2s]" />
              </div>
            </div>
          </div>
        )}

        {/* Error message */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/30
            text-red-400 text-sm px-4 py-3 rounded-lg mb-4">
            ⚠️ {error}
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* ── Input Area ── */}
      <div className="flex gap-3">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask your AI tutor anything... (Enter to send)"
          rows={2}
          className="flex-1 bg-gray-900 border border-gray-800
            text-white placeholder-gray-500 rounded-xl px-4 py-3
            text-sm resize-none focus:outline-none focus:border-blue-500
            transition-colors"
        />
        <button
          onClick={handleSend}
          disabled={!input.trim() || loading}
          className="bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700
            disabled:text-gray-500 text-white px-6 rounded-xl
            transition-colors font-medium text-sm"
        >
          {loading ? '...' : 'Send →'}
        </button>
      </div>

    </div>
  )
}

export default Chat