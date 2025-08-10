export function ResultsPanel({ message, isLoading }: { message: any, isLoading: boolean }) {
  const movies = message?.info?.movies ?? []
  const people = message?.info?.people ?? []

  return (
    <div className="glass rounded-2xl p-6">
      <h2 className="text-xl font-semibold mb-3">Results</h2>
      {isLoading && <p className="text-zinc-400">Searching…</p>}
      {!isLoading && movies.length === 0 && people.length === 0 && <p className="text-zinc-500">No results yet.</p>}

      {movies.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-medium mb-2">Movies</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {movies.slice(0, 6).map((m: any) => (
              <div key={m.id} className="glass rounded-xl p-3">
                <div className="text-sm font-medium">{m.title}</div>
                <div className="text-xs text-zinc-400">{m.release_date}</div>
                <div className="text-xs line-clamp-3 text-zinc-300 mt-1">{m.overview}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {people.length > 0 && (
        <div>
          <h3 className="text-lg font-medium mb-2">People</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {people.slice(0, 6).map((p: any) => (
              <div key={p.id} className="glass rounded-xl p-3">
                <div className="text-sm font-medium">{p.name}</div>
                <div className="text-xs text-zinc-400">Popularity: {Math.round(p.popularity)}</div>
                {p.known_for && (
                  <div className="text-xs text-zinc-300 mt-1 line-clamp-3">
                    {p.known_for.map((k: any) => k.title || k.name).filter(Boolean).join(', ')}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}