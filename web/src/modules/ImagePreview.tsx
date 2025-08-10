export function ImagePreview({ message }: { message: any }) {
  const imageBase64 = message?.image?.image_base64
  const provider = message?.image?.provider

  if (!imageBase64) return (
    <div className="glass rounded-2xl p-6">
      <h2 className="text-xl font-semibold mb-3">Image</h2>
      <p className="text-zinc-500">No image generated yet.</p>
    </div>
  )

  const src = `data:image/png;base64,${imageBase64}`

  return (
    <div className="glass rounded-2xl p-6">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-xl font-semibold">Image</h2>
        <span className="text-xs text-zinc-400">Provider: {provider}</span>
      </div>
      <img src={src} className="w-full rounded-xl border border-white/10" />
      <div className="mt-3">
        <a download href={src} className="text-sm text-brand-400 hover:underline">Download</a>
      </div>
    </div>
  )
}