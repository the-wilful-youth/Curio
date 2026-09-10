'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';

interface SearchResult {
  id: string;
  title: string;
  summary?: string;
  category?: string;
  created_at: string;
}

export default function Search() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  useEffect(() => {
    const trimmed = query.trim();
    if (!trimmed) {
      setResults([]);
      setSearched(false);
      return;
    }

    const timer = setTimeout(() => {
      searchContent(trimmed);
    }, 300);

    return () => clearTimeout(timer);
  }, [query]);

  const searchContent = async (searchQuery: string) => {
    setLoading(true);
    try {
      const response = await fetch(`/api/search?q=${encodeURIComponent(searchQuery)}`);
      if (!response.ok) throw new Error(`Status ${response.status}`);
      const data = await response.json();
      setResults(Array.isArray(data) ? data : []);
      setSearched(true);
    } catch (error) {
      console.error('Error searching content:', error);
      setResults([]);
      setSearched(true);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      searchContent(query.trim());
    }
  };

  return (
    <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Search Vault</h1>
        <p className="text-sm text-gray-500 mt-1">
          Fast keyword & semantic search across your saved notes, titles, and summaries
        </p>
      </div>

      <form onSubmit={handleSubmit} className="mb-8">
        <div className="relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Type keywords (e.g. machine learning, deadlines, conference)..."
            className="w-full rounded-xl border border-gray-200 bg-white py-3.5 pl-4 pr-24 text-sm text-gray-900 shadow-sm placeholder:text-gray-400 focus:border-indigo-600 focus:outline-none focus:ring-1 focus:ring-indigo-600 transition"
          />
          <button
            type="submit"
            className="absolute right-2 top-2 bottom-2 px-4 rounded-lg bg-indigo-600 text-white text-xs font-semibold hover:bg-indigo-700 transition"
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </form>

      {loading ? (
        <div className="flex flex-col items-center justify-center h-48 bg-white rounded-xl border border-gray-100 shadow-sm">
          <div className="animate-spin rounded-full border-3 border-indigo-600 border-t-transparent w-7 h-7"></div>
          <p className="mt-3 text-xs text-gray-400">Searching your vault...</p>
        </div>
      ) : searched && results.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-xl border border-dashed border-gray-200">
          <p className="text-base font-medium text-gray-800">No results found for &ldquo;{query}&rdquo;</p>
          <p className="text-sm text-gray-500 mt-1">Try another keyword or broader search term</p>
        </div>
      ) : (
        <div className="space-y-3">
          {results.map(item => (
            <Link
              key={item.id}
              href={`/library/${item.id}`}
              className="block p-5 bg-white rounded-xl border border-gray-200 shadow-sm hover:border-indigo-200 hover:shadow-md transition"
            >
              <div className="flex items-center justify-between gap-4">
                <h3 className="text-base font-semibold text-gray-900 hover:text-indigo-600 transition">
                  {item.title}
                </h3>
                {item.category && (
                  <span className="text-xs px-2.5 py-0.5 rounded-full bg-gray-100 text-gray-600 font-medium shrink-0">
                    {item.category}
                  </span>
                )}
              </div>
              {item.summary && (
                <p className="text-sm text-gray-600 mt-2 line-clamp-2">{item.summary}</p>
              )}
            </Link>
          ))}
        </div>
      )}
    </main>
  );
}