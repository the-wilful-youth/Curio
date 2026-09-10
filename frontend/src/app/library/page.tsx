'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';

interface NoteItem {
  id: string;
  title: string;
  summary?: string;
  category?: string;
  created_at: string;
  tags?: Array<{ id: string; name: string }>;
}

export default function Library() {
  const [notes, setNotes] = useState<NoteItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterCategory, setFilterCategory] = useState<string>('all');

  useEffect(() => {
    fetchNotes();
  }, []);

  const fetchNotes = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/notes?limit=100');
      if (!response.ok) throw new Error(`Status ${response.status}`);
      const data = await response.json();
      setNotes(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching notes:', error);
      setNotes([]);
    } finally {
      setLoading(false);
    }
  };

  const categories = ['all', ...Array.from(new Set(notes.map(n => n.category).filter(Boolean)))];
  const filteredNotes =
    filterCategory === 'all'
      ? notes
      : notes.filter(n => n.category === filterCategory);

  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Content Library</h1>
          <p className="text-sm text-slate-500 mt-1">
            Browse all saved web articles, videos, and extracted notes
          </p>
        </div>
        <Link
          href="/"
          className="inline-flex items-center justify-center px-4 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 shadow-sm transition"
        >
          + Save New Content
        </Link>
      </div>

      {/* Category Pills */}
      {categories.length > 2 && (
        <div className="flex items-center gap-2 overflow-x-auto pb-4 mb-6">
          {categories.map((cat) => (
            <button
              key={cat as string}
              onClick={() => setFilterCategory(cat as string)}
              className={`px-3 py-1.5 rounded-full text-xs font-semibold capitalize transition ${
                filterCategory === cat
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-50'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      )}

      {loading ? (
        <div className="flex flex-col items-center justify-center h-64 bg-white rounded-xl border border-slate-100 shadow-sm">
          <div className="animate-spin rounded-full border-3 border-indigo-600 border-t-transparent w-8 h-8"></div>
          <p className="mt-3 text-sm text-slate-500">Loading library contents...</p>
        </div>
      ) : filteredNotes.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-xl border border-dashed border-slate-200">
          <h2 className="text-lg font-semibold text-slate-800 mb-2">No notes in library</h2>
          <p className="text-sm text-slate-500 mb-6">
            Start by saving a web article or YouTube link to populate your vault.
          </p>
          <Link
            href="/"
            className="inline-flex items-center px-4 py-2 rounded-lg bg-indigo-600 text-white text-sm font-medium hover:bg-indigo-700 transition"
          >
            Save Your First URL
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredNotes.map((note) => (
            <Link
              key={note.id}
              href={`/library/${note.id}`}
              className="p-6 bg-white rounded-xl border border-slate-200 shadow-sm hover:border-indigo-300 hover:shadow-md transition flex flex-col justify-between group"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-3">
                  <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-indigo-50 text-indigo-700 capitalize">
                    {note.category || 'General'}
                  </span>
                  <span className="text-xs text-slate-400">
                    {new Date(note.created_at).toLocaleDateString()}
                  </span>
                </div>
                <h3 className="text-base font-bold text-slate-900 group-hover:text-indigo-600 transition line-clamp-2">
                  {note.title}
                </h3>
                {note.summary && (
                  <p className="text-sm text-slate-600 mt-2 line-clamp-3 leading-relaxed">
                    {note.summary}
                  </p>
                )}
              </div>

              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs font-semibold text-indigo-600">
                <span>View Full Note</span>
                <span>→</span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </main>
  );
}