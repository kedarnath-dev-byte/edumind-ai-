/**
 * @file FineTuning.jsx
 * @description Fine-Tuning monitoring page for EduMind AI.
 *              Shows all 8 fine-tuning frameworks and their job status.
 *              Displays training progress, loss curves, and job history.
 *              Connects to FastAPI fine-tuning endpoints.
 */
import { useState } from 'react'

// ─── Fine-Tuning Frameworks ───────────────────────────────────────────────────
const FRAMEWORKS = [
  { id: 'sft',          label: 'SFT',          name: 'Supervised Fine-Tuning',  color: 'blue',   icon: '🎯' },
  { id: 'lora',         label: 'LoRA',         name: 'Low-Rank Adaptation',     color: 'purple', icon: '🔗' },
  { id: 'qlora',        label: 'QLoRA',        name: 'Quantized LoRA',          color: 'pink',   icon: '⚡' },
  { id: 'dpo',          label: 'DPO',          name: 'Direct Preference Opt.',  color: 'green',  icon: '🎮' },
  { id: 'rlhf',         label: 'RLHF',         name: 'RL from Human Feedback',  color: 'orange', icon: '🤝' },
  { id: 'adapter',      label: 'Adapter',      name: 'Adapter Tuning',          color: 'yellow', icon: '🔌' },
  { id: 'prefix',       label: 'Prefix',       name: 'Prefix Tuning',           color: 'red',    icon: '📌' },
  { id: 'peft',         label: 'PEFT',         name: 'Parameter Efficient FT',  color: 'cyan',   icon: '🛠️' },
]

// ─── Mock Jobs ────────────────────────────────────────────────────────────────
const MOCK_JOBS = [
  { id: 'job_001', framework: 'LoRA',   model: 'Llama-3-8B', status: 'completed', progress: 100, loss: '0.234' },
  { id: 'job_002', framework: 'QLoRA',  model: 'Llama-3-8B', status: 'running',   progress: 67,  loss: '0.412' },
  { id: 'job_003', framework: 'DPO',    model: 'Llama-3-8B', status: 'pending',   progress: 0,   loss: '-'     },
  { id: 'job_004', framework: 'SFT',    model: 'Llama-3-8B', status: 'completed', progress: 100, loss: '0.189' },
]

// ─── Status Badge ─────────────────────────────────────────────────────────────
const StatusBadge = ({ status }) => {
  const styles = {
    completed: 'bg-green-500/20  text-green-400',
    running:   'bg-blue-500/20   text-blue-400',
    pending:   'bg-yellow-500/20 text-yellow-400',
    failed:    'bg-red-500/20    text-red-400',
  }
  const icons = {
    completed: '✅', running: '🔄', pending: '⏳', failed: '❌'
  }
  return (
    <span className={`text-xs px-2 py-1 rounded-full ${styles[status]}`}>
      {icons[status]} {status}
    </span>
  )
}

// ─── Framework Card ───────────────────────────────────────────────────────────
const FrameworkCard = ({ fw, isSelected, onClick }) => (
  <button
    onClick={onClick}
    className={`
      bg-gray-900 border rounded-xl p-4 text-left
      transition-all duration-200 w-full
      ${isSelected
        ? `border-${fw.color}-500 bg-${fw.color}-500/10`
        : 'border-gray-800 hover:border-gray-600'
      }
    `}
  >
    <div className="flex items-center gap-2 mb-2">
      <span className="text-2xl">{fw.icon}</span>
      <span className={`text-${fw.color}-400 font-bold`}>{fw.label}</span>
    </div>
    <p className="text-gray-400 text-xs">{fw.name}</p>
  </button>
)

// ─── Job Row ──────────────────────────────────────────────────────────────────
const JobRow = ({ job }) => (
  <div className="border-b border-gray-800 pb-4 last:border-0 last:pb-0">
    <div className="flex items-center justify-between mb-2">
      <div className="flex items-center gap-3">
        <p className="text-white text-sm font-medium">{job.framework}</p>
        <span className="text-gray-500 text-xs">{job.model}</span>
      </div>
      <div className="flex items-center gap-3">
        <span className="text-gray-400 text-xs">Loss: {job.loss}</span>
        <StatusBadge status={job.status} />
      </div>
    </div>
    {/* Progress Bar */}
    <div className="w-full bg-gray-800 rounded-full h-1.5">
      <div
        className={`h-1.5 rounded-full transition-all duration-500
          ${job.status === 'completed' ? 'bg-green-500' :
            job.status === 'running'   ? 'bg-blue-500'  : 'bg-gray-600'
          }`}
        style={{ width: `${job.progress}%` }}
      />
    </div>
    <p className="text-gray-500 text-xs mt-1">{job.progress}% complete</p>
  </div>
)

// ─── FineTuning Page ──────────────────────────────────────────────────────────
const FineTuning = () => {
  const [selectedFW, setSelectedFW] = useState('lora')

  return (
    <div className="max-w-6xl mx-auto">

      {/* ── Header ── */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">⚙️ Fine-Tuning Studio</h1>
        <p className="text-gray-400 text-sm mt-1">
          Monitor all 8 fine-tuning frameworks running on your models
        </p>
      </div>

      {/* ── Framework Grid ── */}
      <h2 className="text-lg font-semibold text-white mb-3">
        🛠️ Available Frameworks
      </h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-8">
        {FRAMEWORKS.map(fw => (
          <FrameworkCard
            key={fw.id}
            fw={fw}
            isSelected={selectedFW === fw.id}
            onClick={() => setSelectedFW(fw.id)}
          />
        ))}
      </div>

      {/* ── Selected Framework Info ── */}
      {selectedFW && (() => {
        const fw = FRAMEWORKS.find(f => f.id === selectedFW)
        return (
          <div className={`
            bg-gray-900 border border-${fw.color}-500/30
            rounded-xl p-6 mb-8
          `}>
            <div className="flex items-center gap-3 mb-3">
              <span className="text-3xl">{fw.icon}</span>
              <div>
                <h3 className="text-white font-bold text-lg">{fw.label}</h3>
                <p className="text-gray-400 text-sm">{fw.name}</p>
              </div>
            </div>
            <div className="grid grid-cols-3 gap-4 mt-4">
              {[
                { label: 'Base Model',  value: 'Llama-3-8B'  },
                { label: 'Framework',   value: fw.label       },
                { label: 'Status',      value: '✅ Available' },
              ].map(item => (
                <div key={item.label}
                  className="bg-gray-800 rounded-lg p-3">
                  <p className="text-gray-400 text-xs">{item.label}</p>
                  <p className="text-white text-sm font-medium mt-1">
                    {item.value}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )
      })()}

      {/* ── Jobs List ── */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h2 className="text-white font-semibold mb-4">
          📋 Fine-Tuning Jobs
        </h2>
        <div className="flex flex-col gap-4">
          {MOCK_JOBS.map(job => (
            <JobRow key={job.id} job={job} />
          ))}
        </div>
      </div>

    </div>
  )
}

export default FineTuning