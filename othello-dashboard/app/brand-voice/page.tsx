// app/brand-voice/page.tsx
"use client"

import { useState } from "react"
import { Loader2, Sparkles, Instagram, Copy, Check } from "lucide-react"

type GeneratedContent = {
  title?: string
  hook?: string
  caption?: string
  hashtags?: string[]
  cta?: string
}

type BrandVoiceProfile = {
  tone?: {
    sicaklik?: number
    mizah?: number
    enerji?: number
    resmiyet?: number
  }
  style?: {
    cumle_uzunlugu?: "kısa" | "orta" | "uzun" | string
    emoji_kullanimi?: "düşük" | "orta" | "yüksek" | string
  }
  lexicon?: string[]
  dos?: string[]
  donts?: string[]
  cta_patterns?: string[]
  few_shots?: Array<{ caption?: string; notes?: string }>
  // Eski/alternatif alan adları için tolerans:
  language_style?: string
  emoji_usage?: string
  personality?: string[]
}

type ApiResult = {
  success?: boolean
  username?: string
  posts_synced?: number
  brand_voice?: BrandVoiceProfile
  generated_content?: GeneratedContent
  rag_used?: boolean
  rag_passages_count?: number
  error?: string
}

export default function BrandVoicePage() {
  const [instagramUrl, setInstagramUrl] = useState("")
  const [topic, setTopic] = useState("")
  const [platform, setPlatform] = useState("instagram")
  const [goal, setGoal] = useState("engagement")
  const [result, setResult] = useState<ApiResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [copied, setCopied] = useState(false)

  const API_URL =
    process.env.NEXT_PUBLIC_API_URL ||
    "https://othello-backend-production-2ff4.up.railway.app"

  const generateContent = async () => {
    setLoading(true)
    setResult(null)

    try {
      const res = await fetch(`${API_URL}/api/brand-voice/generate-from-url`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          client_id: `user_${Date.now()}`,
          instagram_url: instagramUrl,
          topic,
          platform,
          goal,
          max_posts: 12,
        }),
      })

      if (!res.ok) {
        const txt = await res.text().catch(() => "")
        throw new Error(`Failed to generate (${res.status}) ${txt}`)
      }

      const data: ApiResult = await res.json()
      setResult(data)
    } catch (error) {
      console.error("Error:", error)
      alert("Hata oluştu. Lütfen tekrar deneyin.")
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = (text: string) => {
    if (!text) return
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const toneEntries = (result?.brand_voice?.tone
    ? Object.entries(result.brand_voice.tone)
    : []) as Array<[string, number | undefined]>

  const style = result?.brand_voice?.style

  const fullCopy = [
    result?.generated_content?.caption || "",
    (result?.generated_content?.hashtags || []).join(" "),
    result?.generated_content?.cta || "",
  ]
    .filter(Boolean)
    .join("\n\n")

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-8">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Sparkles className="w-10 h-10 text-purple-600" />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              AI Brand Voice
            </h1>
          </div>
          <p className="text-gray-600 text-lg">
            Instagram hesabından otomatik içerik üret
          </p>
        </div>

        {/* Form */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <div className="space-y-6">
            {/* Instagram URL */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Instagram className="inline w-4 h-4 mr-2" />
                Instagram Profil URL
              </label>
              <input
                type="url"
                value={instagramUrl}
                onChange={(e) => setInstagramUrl(e.target.value)}
                placeholder="https://www.instagram.com/username/"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>

            {/* Topic */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                İçerik Konusu
              </label>
              <input
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="örn: yeni yıl kampanyası, hafta sonu özel menü"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>

            {/* Platform & Goal */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Platform
                </label>
                <select
                  value={platform}
                  onChange={(e) => setPlatform(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                >
                  <option value="instagram">Instagram</option>
                  <option value="linkedin">LinkedIn</option>
                  <option value="twitter">Twitter / X</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Hedef
                </label>
                <select
                  value={goal}
                  onChange={(e) => setGoal(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                >
                  <option value="engagement">Etkileşim</option>
                  <option value="sales">Satış</option>
                  <option value="awareness">Farkındalık</option>
                </select>
              </div>
            </div>

            {/* Generate Button */}
            <button
              onClick={generateContent}
              disabled={loading || !instagramUrl || !topic}
              className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-4 rounded-lg font-semibold text-lg hover:from-purple-700 hover:to-blue-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  İçerik Üretiliyor...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5" />
                  İçerik Üret
                </>
              )}
            </button>
          </div>
        </div>

        {/* Results */}
        {result && (
          <div className="space-y-6">
            {/* Stats */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="bg-white rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-purple-600">
                  {result.posts_synced ?? "-"}
                </div>
                <div className="text-sm text-gray-600">Post Analiz Edildi</div>
              </div>
              <div className="bg-white rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-blue-600">
                  {result.username ? `@${result.username}` : "-"}
                </div>
                <div className="text-sm text-gray-600">Hesap</div>
              </div>
              <div className="bg-white rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-green-600">
                  {result.rag_passages_count ?? 0}
                </div>
                <div className="text-sm text-gray-600">RAG Passages</div>
              </div>
            </div>

            {/* Generated Content */}
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-6">
                <h2 className="text-2xl font-bold text-gray-800">
                  {result.generated_content?.title || "Üretilen İçerik"}
                </h2>
                <button
                  onClick={() => copyToClipboard(fullCopy)}
                  className="flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition"
                >
                  {copied ? (
                    <Check className="w-4 h-4 text-green-600" />
                  ) : (
                    <Copy className="w-4 h-4" />
                  )}
                  {copied ? "Kopyalandı!" : "Kopyala"}
                </button>
              </div>

              <div className="space-y-6">
                {/* Hook */}
                {result.generated_content?.hook && (
                  <div className="bg-purple-50 p-4 rounded-lg">
                    <p className="font-semibold text-purple-900 mb-2">Hook:</p>
                    <p className="text-gray-800">
                      {result.generated_content.hook}
                    </p>
                  </div>
                )}

                {/* Caption */}
                {result.generated_content?.caption && (
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <p className="font-semibold text-blue-900 mb-2">Caption:</p>
                    <p className="text-gray-800 whitespace-pre-wrap">
                      {result.generated_content.caption}
                    </p>
                  </div>
                )}

                {/* Hashtags */}
                {result.generated_content?.hashtags?.length ? (
                  <div className="bg-green-50 p-4 rounded-lg">
                    <p className="font-semibold text-green-900 mb-2">
                      Hashtags:
                    </p>
                    <p className="text-blue-600">
                      {result.generated_content.hashtags.join(" ")}
                    </p>
                  </div>
                ) : null}

                {/* CTA */}
                {result.generated_content?.cta && (
                  <div className="bg-orange-50 p-4 rounded-lg">
                    <p className="font-semibold text-orange-900 mb-2">CTA:</p>
                    <p className="text-gray-800">
                      {result.generated_content.cta}
                    </p>
                  </div>
                )}
              </div>
            </div>

            {/* Brand Voice Details */}
            <div className="bg-white rounded-lg p-6">
              <h3 className="font-semibold text-gray-800 mb-4">
                Marka Sesi Analizi
              </h3>

              {/* Tone grid */}
              {toneEntries.length ? (
                <div className="space-y-3 mb-6">
                  {toneEntries.map(([key, val]) => {
                    const pct = Math.round(((val ?? 0) as number) * 100)
                    const label =
                      key === "sicaklik"
                        ? "Sıcaklık"
                        : key === "mizah"
                        ? "Mizah"
                        : key === "enerji"
                        ? "Enerji"
                        : key === "resmiyet"
                        ? "Resmiyet"
                        : key
                    return (
                      <div key={key}>
                        <div className="flex justify-between text-sm text-gray-700 mb-1">
                          <span>{label}</span>
                          <span>{isFinite(pct) ? `${pct}%` : "-"}</span>
                        </div>
                        <div className="h-2 bg-gray-200 rounded">
                          <div
                            className="h-2 bg-gradient-to-r from-purple-500 to-blue-500 rounded"
                            style={{ width: `${Math.min(Math.max(pct, 0), 100)}%` }}
                          />
                        </div>
                      </div>
                    )
                  })}
                </div>
              ) : (
                <p className="text-sm text-gray-500 mb-6">
                  Ton verisi bulunamadı.
                </p>
              )}

              {/* Style */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-600">Cümle Uzunluğu:</span>
                  <span className="ml-2 font-medium">
                    {style?.cumle_uzunlugu ??
                      result?.brand_voice?.language_style ??
                      "-"}
                  </span>
                </div>
                <div>
                  <span className="text-gray-600">Emoji Kullanımı:</span>
                  <span className="ml-2 font-medium">
                    {style?.emoji_kullanimi ??
                      result?.brand_voice?.emoji_usage ??
                      "-"}
                  </span>
                </div>
                {result?.brand_voice?.personality?.length ? (
                  <div className="sm:col-span-2">
                    <span className="text-gray-600">Kişilik:</span>
                    <span className="ml-2 font-medium">
                      {result.brand_voice.personality.join(", ")}
                    </span>
                  </div>
                ) : null}
              </div>

              {/* Lexicon tags */}
              {result?.brand_voice?.lexicon?.length ? (
                <div className="mt-6">
                  <p className="text-sm text-gray-600 mb-2">Sıklıkla Kullanılan Kelimeler:</p>
                  <div className="flex flex-wrap gap-2">
                    {result.brand_voice.lexicon.map((w, i) => (
                      <span
                        key={`${w}-${i}`}
                        className="px-3 py-1 rounded-full text-xs bg-purple-50 text-purple-700 border border-purple-200"
                      >
                        {w}
                      </span>
                    ))}
                  </div>
                </div>
              ) : null}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

