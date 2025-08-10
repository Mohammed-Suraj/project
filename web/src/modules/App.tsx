import { useMemo, useRef, useState } from 'react'
import { ChatPanel } from './ChatPanel'
import { ResultsPanel } from './ResultsPanel'
import { ImagePreview } from './ImagePreview'

export default function App() {
  const [history, setHistory] = useState<any[]>([])
  const [latest, setLatest] = useState<any | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const sessionIdRef = useRef<string>(() => crypto.randomUUID() as unknown as string)

  const sessionId = useMemo(() => crypto.randomUUID(), [])

  return (
    <div className="min-h-screen grid grid-cols-1 lg:grid-cols-2 gap-6 p-6">
      <div className="glass rounded-2xl p-6">
        <div className="mb-4">
          <h1 className="text-3xl font-bold gradient-text">Bollywood Chatbot</h1>
          <p className="text-zinc-400">Ask about Indian movies, actors, and actresses. Generate images from your ideas.</p>
        </div>
        <ChatPanel
          sessionId={sessionId}
          onUpdate={(msg, hist) => { setLatest(msg); setHistory(hist) }}
          onLoading={setIsLoading}
        />
      </div>
      <div className="space-y-6">
        <ResultsPanel message={latest} isLoading={isLoading} />
        <ImagePreview message={latest} />
      </div>
    </div>
  )
}