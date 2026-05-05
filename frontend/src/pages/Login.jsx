/**
 * @file Login.jsx
 * @description Gmail OAuth login page for EduMind AI.
 *              Students sign in with Google — no password needed.
 *              Redirects to dashboard after successful authentication.
 */
import { useAuth } from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'

// ─── Login Page ───────────────────────────────────────────────────────────────
const Login = () => {
  const { login } = useAuth()
  const navigate = useNavigate()

  // Simulate Gmail OAuth login for now
  // Will connect to real Google OAuth in Feature 10
  const handleGoogleLogin = () => {
    try {
      const mockUser = {
        name: 'Kedarnath',
        email: 'kedarnath@gmail.com',
        picture: '',
        role: 'admin',
      }
      login(mockUser, 'mock_token_12345')
      navigate('/dashboard')
    } catch (error) {
      console.error('Login failed:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center">
      <div className="bg-gray-900 border border-gray-800 rounded-2xl
        p-10 w-full max-w-md text-center">

        {/* Logo */}
        <div className="mb-8">
          <span className="text-6xl">🧠</span>
          <h1 className="text-3xl font-bold text-white mt-4">EduMind AI</h1>
          <p className="text-gray-400 mt-2 text-sm">
            Your AI-powered study companion
          </p>
        </div>

        {/* Features List */}
        <div className="text-left bg-gray-800/50 rounded-xl p-4 mb-8">
          {[
            '✅ 16 RAG Pipelines',
            '✅ 7 LangGraph AI Agents',
            '✅ 8 Fine-Tuning Frameworks',
            '✅ 5 Model Serving Engines',
          ].map((feature) => (
            <p key={feature} className="text-gray-300 text-sm py-1">
              {feature}
            </p>
          ))}
        </div>

        {/* Google Login Button */}
        <button
          onClick={handleGoogleLogin}
          className="w-full bg-white hover:bg-gray-100
            text-gray-800 font-semibold py-3 px-6 rounded-xl
            flex items-center justify-center gap-3
            transition-colors duration-200"
        >
          <span className="text-xl">🔵</span>
          Continue with Google
        </button>

        <p className="text-gray-500 text-xs mt-6">
          By signing in you agree to our Terms of Service
        </p>
      </div>
    </div>
  )
}

export default Login