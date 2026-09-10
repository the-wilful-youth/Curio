'use client';

import Link from 'next/link';
import { useState } from 'react';

export default function Home() {
  const [url, setUrl] = useState('');
  const [status, setStatus] = useState<'idle' | 'submitting' | 'success' | 'error'>('idle');
  const [statusMessage, setStatusMessage] = useState('');
  const [result, setResult] = useState<any>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) return;

    setStatus('submitting');
    setStatusMessage('Capturing and extracting content...');

    try {
      const lowerUrl = url.toLowerCase();
      let platform = 'web';
      let contentType = 'article';
      if (lowerUrl.includes('youtube.com') || lowerUrl.includes('youtu.be')) {
        platform = 'youtube';
        contentType = 'video';
      }

      const response = await fetch('/api/sources/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: url.trim(),
          platform,
          content_type: contentType,
        }),
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || `Server returned error ${response.status}`);
      }

      const data = await response.json();
      setStatus('success');
      setStatusMessage('Content saved and added to your knowledge vault!');
      setResult(data);
      setUrl('');
    } catch (error) {
      setStatus('error');
      setStatusMessage(error instanceof Error ? error.message : String(error));
    }
  };

  return (
    <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="text-center mb-10">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-50 border border-indigo-100 text-xs font-semibold text-indigo-700 mb-4">
          ✨ Private & Single-User Knowledge Vault
        </div>
        <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight sm:text-5xl">
          Save anything. Understand everything.
        </h1>
        <p className="mt-4 text-lg text-slate-600 max-w-xl mx-auto">
          Share articles, videos, and links to automatically extract summaries, key dates, deadlines, and actionable tasks.
        </p>
      </div>

      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 sm:p-8">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="url" className="block text-sm font-semibold text-slate-700 mb-2">
              Source URL
            </label>
            <div className="relative">
              <input
                id="url"
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                required
                placeholder="https://example.com/article or https://youtube.com/watch?v=..."
                className="w-full rounded-xl border border-slate-300 py-3.5 pl-4 pr-32 text-sm text-slate-900 shadow-sm placeholder:text-slate-400 focus:border-indigo-600 focus:outline-none focus:ring-1 focus:ring-indigo-600 transition"
              />
              <button
                type="submit"
                disabled={status === 'submitting'}
                className="absolute right-2 top-2 bottom-2 px-5 rounded-lg bg-indigo-600 text-white text-xs font-semibold hover:bg-indigo-700 disabled:opacity-60 transition"
              >
                {status === 'submitting' ? 'Processing...' : 'Save URL'}
              </button>
            </div>
          </div>

          {status !== 'idle' && (
            <div
              className={`p-4 rounded-xl text-sm font-medium flex items-center justify-between ${
                status === 'error'
                  ? 'bg-rose-50 text-rose-800 border border-rose-200'
                  : status === 'success'
                  ? 'bg-emerald-50 text-emerald-800 border border-emerald-200'
                  : 'bg-indigo-50 text-indigo-800 border border-indigo-200'
              }`}
            >
              <span>{statusMessage}</span>
              {status === 'success' && (
                <Link
                  href="/library"
                  className="underline font-semibold hover:text-emerald-950 text-xs ml-4"
                >
                  View Library →
                </Link>
              )}
            </div>
          )}
        </form>

        {result && (
          <div className="mt-8 pt-6 border-t border-slate-100">
            <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">
              Ingested Source Summary
            </h3>
            <div className="bg-slate-50 p-4 rounded-xl text-xs space-y-1.5 border border-slate-200">
              <div><span className="font-semibold text-slate-700">Source ID:</span> {result.id}</div>
              <div><span className="font-semibold text-slate-700">Platform:</span> {result.platform}</div>
              <div><span className="font-semibold text-slate-700">Status:</span> <span className="text-emerald-600 font-semibold">{result.status}</span></div>
              <div className="truncate"><span className="font-semibold text-slate-700">URL:</span> {result.url}</div>
            </div>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-8">
        <Link
          href="/dashboard"
          className="p-4 rounded-xl bg-white border border-slate-200 hover:border-indigo-300 hover:shadow-sm transition text-center"
        >
          <div className="text-2xl mb-1">📊</div>
          <div className="text-sm font-semibold text-slate-800">Dashboard</div>
          <div className="text-xs text-slate-500 mt-0.5">Upcoming events & recent notes</div>
        </Link>
        <Link
          href="/chat"
          className="p-4 rounded-xl bg-white border border-slate-200 hover:border-indigo-300 hover:shadow-sm transition text-center"
        >
          <div className="text-2xl mb-1">🤖</div>
          <div className="text-sm font-semibold text-slate-800">Ask My Vault</div>
          <div className="text-xs text-slate-500 mt-0.5">Chat over your saved items</div>
        </Link>
        <Link
          href="/tasks"
          className="p-4 rounded-xl bg-white border border-slate-200 hover:border-indigo-300 hover:shadow-sm transition text-center"
        >
          <div className="text-2xl mb-1">✅</div>
          <div className="text-sm font-semibold text-slate-800">Action Items</div>
          <div className="text-xs text-slate-500 mt-0.5">Extracted tasks & deadlines</div>
        </Link>
      </div>
    </main>
  );
}