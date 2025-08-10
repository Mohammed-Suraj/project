import { useState } from 'react'
import axios from 'axios'
import clsx from 'clsx'

const API_BASE = (typeof window !== 'undefined' ? window.location.origin : '') || import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export function ChatPanel({ sessionId, onUpdate, onLoading }: {
  sessionId: string
  onUpdate: (message: any, history: any[]) => void
  onLoading: (loading: boolean) => void
}) {
  const [message, setMessage] = useState('')
  const [generateImage, setGenerateImage] = useState(true)
  const [size, setSize] = useState('1024x1024')

  const canSend = message.trim().length > 0

  async function send() {
    if (!canSend) return
    onLoading(true)
    try {
      const res = await axios.post(`${API_BASE}/chat`, {
        session_id: sessionId,
        message,
        generate_image: generateImage,
        image_size: size,
      })
      onUpdate(res.data.message, res.data.history)
    } catch (e) {
      // noop: could add toast
    } finally {
      onLoading(false)
    }
  }

  return (
    <div className="space-y-4">
      <div className={clsx('glass rounded-xl p-4 grid gap-3')}>        
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => { if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) send() }}
          placeholder="e.g., Find movies with Shah Rukh Khan in 2010s"
          className="w-full bg-transparent outline-none text-lg placeholder:text-zinc-500"
        />
        <div className="flex items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <label className="flex items-center gap-2 text-sm text-zinc-400">
              <input type="checkbox" checked={generateImage} onChange={(e) => setGenerateImage(e.target.checked)} />
              Generate image
            </label>
            <select value={size} onChange={(e) => setSize(e.target.value)} className="bg-black/40 border border-white/10 rounded-md text-sm px-2 py-1">
              <option>512x512</option>
              <option>768x768</option>
              <option>1024x1024</option>
            </select>
          </div>
          <button
            onClick={send}
            disabled={!canSend}
            className={clsx('px-4 py-2 rounded-lg font-medium transition', canSend ? 'bg-brand-600 hover:bg-brand-500 shadow-glow' : 'bg-zinc-800 text-zinc-500 cursor-not-allowed')}
          >Send</button>
        </div>
      </div>
      <div className="flex flex-wrap gap-2">
        {['Top Bollywood films', 'Best of Alia Bhatt', 'AR Rahman classics', 'Create a poster of a dance scene'].map(q => (
          <button key={q} onClick={() => setMessage(q)} className="glass rounded-full px-3 py-1 text-sm hover:bg-white/10">{q}</button>
        ))}
      </div>
    </div>
  )
}