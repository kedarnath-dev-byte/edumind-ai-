/**
 * @file Admin.jsx
 * @description Admin dashboard for EduMind AI.
 *              Only accessible by Kedarnath (admin role).
 *              Shows all student activity, queries, and system stats.
 */
import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'

// ─── Stat Card ────────────────────────────────────────────────────────────────
const AdminCard = ({ icon, label, value, color }) => (
  <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
    <div className="flex items-center gap-3 mb-2">
      <span className="text-2xl">{icon}</span>
      <p className="text-gray-400 text-sm">{label}</p>
    </div>
    <p className={`text-3xl font-bold text-${color}-400`}>{value}</p>
  </div>
)

// ─── Admin Page ───────────────────────────────────────────────────────────────
const Admin = () => {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [stats, setStats] = useState(null)

  // Guard — only admin can access
  useEffect(() => {
    if (user?.role !== 'admin') {
      navigate('/dashboard')
    }
    // Simulate loading admin stats
    setStats({
      totalStudents: 24,
      totalQueries: 312,
      totalDocuments: 87,
      activeAgents: 7,
      pipelinesUsed: 16,
      finetuningJobs: 3,
    })
  }, [user, navigate])

  if (!stats) return (
    <div className="text-gray-400 text-center mt-20">Loading...</div>
  )

  return (
    <div className="max-w-6xl mx-auto">

      {/* ── Header ── */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">
          👑 Admin Dashboard
        </h1>
        <p className="text-gray-400 text-sm mt-1">
          Welcome, {user?.name}. Here's the full system overview.
        </p>
      </div>

      {/* ── Stats Grid ── */}
      <div className="grid grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        <AdminCard icon="👥" label="Total Students"
          value={stats.totalStudents}    color="blue"   />
        <AdminCard icon="💬" label="Total Queries"
          value={stats.totalQueries}     color="green"  />
        <AdminCard icon="📄" label="Total Documents"
          value={stats.totalDocuments}   color="purple" />
        <AdminCard icon="🤖" label="Active Agents"
          value={stats.activeAgents}     color="orange" />
        <AdminCard icon="🔀" label="RAG Pipelines"
          value={stats.pipelinesUsed}    color="pink"   />
        <AdminCard icon="⚙️"  label="Fine-Tuning Jobs"
          value={stats.finetuningJobs}   color="yellow" />
      </div>

      {/* ── Recent Activity ── */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h2 className="text-white font-semibold mb-4">
          📊 Recent Student Activity
        </h2>
        <div className="flex flex-col gap-3">
          {[
            { student: 'student1@gmail.com', action: 'Asked about LoRA fine-tuning',    pipeline: 'HyDE RAG',   time: '2 min ago' },
            { student: 'student2@gmail.com', action: 'Uploaded deep_learning.pdf',      pipeline: 'Upload',     time: '5 min ago' },
            { student: 'student3@gmail.com', action: 'Asked about transformer architecture', pipeline: 'Fusion RAG', time: '12 min ago' },
            { student: 'student4@gmail.com', action: 'Started fine-tuning job',         pipeline: 'QLoRA',      time: '1 hr ago'  },
          ].map((activity, idx) => (
            <div key={idx}
              className="flex items-center justify-between
              border-b border-gray-800 pb-3 last:border-0 last:pb-0">
              <div>
                <p className="text-white text-sm">{activity.action}</p>
                <p className="text-gray-500 text-xs mt-0.5">
                  {activity.student}
                </p>
              </div>
              <div className="text-right">
                <span className="text-xs bg-blue-500/20 text-blue-400
                  px-2 py-1 rounded-full">
                  {activity.pipeline}
                </span>
                <p className="text-gray-500 text-xs mt-1">{activity.time}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

    </div>
  )
}

export default Admin