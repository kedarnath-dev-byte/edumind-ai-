/**
 * @file AuthContext.jsx
 * @description Global authentication state for EduMind AI.
 *              Stores logged-in user data and provides login/logout
 *              functions to any component in the app.
 *              Eliminates prop drilling — any component can access
 *              auth state directly via useAuth() hook.
 */
import { createContext, useContext, useState, useEffect } from 'react'

// ─── Create Context ───────────────────────────────────────────────────────────
const AuthContext = createContext(null)

// ─── Auth Provider ────────────────────────────────────────────────────────────
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  // Check if user is already logged in on app start
  useEffect(() => {
    try {
      const savedUser = localStorage.getItem('edumind_user')
      const savedToken = localStorage.getItem('edumind_token')
      if (savedUser && savedToken) {
        setUser(JSON.parse(savedUser))
      }
    } catch (error) {
      console.error('Failed to restore auth session:', error)
    } finally {
      setLoading(false)
    }
  }, [])

  // ─── Login ──────────────────────────────────────────────────────────────────
  const login = (userData, token) => {
    try {
      localStorage.setItem('edumind_user', JSON.stringify(userData))
      localStorage.setItem('edumind_token', token)
      setUser(userData)
    } catch (error) {
      console.error('Failed to save auth session:', error)
    }
  }

  // ─── Logout ─────────────────────────────────────────────────────────────────
  const logout = () => {
    localStorage.removeItem('edumind_user')
    localStorage.removeItem('edumind_token')
    setUser(null)
  }

  // ─── Context Value ───────────────────────────────────────────────────────────
  const value = {
    user,
    loading,
    login,
    logout,
    isAuthenticated: !!user,
  }

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  )
}

// ─── Custom Hook ─────────────────────────────────────────────────────────────
export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used inside AuthProvider')
  }
  return context
}

export default AuthContext