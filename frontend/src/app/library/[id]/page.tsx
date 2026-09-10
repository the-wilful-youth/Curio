'use client';

import Link from 'next/link';
import { useEffect, useState, use } from 'react';

interface NoteItem {
  id: string;
  title: string;
  summary?: string;
  full_note?: string;
  category?: string;
  created_at: string;
  tags?: Array<{ id: string; name: string }>;
}

export default function LibraryDetail({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  const [note, setNote] = useState<NoteItem | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchNote();
  }, [resolvedParams.id]);

  const fetchNote = async () => {
    setLoading(true);
    try {
      const response = await fetch(`/api/notes/${resolvedParams.id}`);
      if (!response.ok) {
        throw new Error('Note not found');
      }
      const data = await response.json();
      setNote(data);
    } catch (error) {
      console.error('Error fetching note:', error);
      setNote(null);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <main className="max-w-4xl mx-auto px-4 py-12">
        <div className="flex flex-col items-center justify-center h-64 bg-white rounded-xl border border-gray-100 shadow-sm">
          <div className="animate-spin rounded-full border-3 border-indigo-600 border-t-transparent w-8 h-8"></div>
          <p className="mt-3 text-sm text-gray-500">Loading content...</p>
        </div>
      </main>
    );
  }

  if (!note) {
    return (
      <main className="max-w-4xl mx-auto px-4 py-12">
        <div className="text-center py-16 bg-white rounded-xl border border-dashed border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900 mb-2">Content not found</h2>
          <p className="text-sm text-gray-500 mb-6">
            The requested note could not be retrieved.
          </p>
          <Link
            href="/library"
            className="inline-flex items-center px-4 py-2 rounded-lg bg-indigo-600 text-white text-sm font-medium hover:bg-indigo-700 transition"
          >
            Back to Library
          </Link>
        </div>
      </main>
    );
  }

  return (
    <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <Link
          href="/library"
          className="inline-flex items-center text-sm font-medium text-indigo-600 hover:text-indigo-800 transition mb-4"
        >
          ← Back to Library
        </Link>
        <h1 className="text-3xl font-bold text-gray-900 tracking-tight">{note.title}</h1>
        <div className="flex items-center gap-3 mt-2 text-xs text-gray-400">
          <span>{new Date(note.created_at).toLocaleDateString(undefined, { dateStyle: 'long' })}</span>
          {note.category && (
            <span className="px-2 py-0.5 rounded-full bg-gray-100 text-gray-600 font-medium">
              {note.category}
            </span>
          )}
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6 sm:p-8 space-y-8">
        {note.summary && (
          <div className="p-4 bg-indigo-50/60 rounded-lg border border-indigo-100/80">
            <h2 className="text-xs font-semibold text-indigo-800 uppercase tracking-wider mb-2">
              Summary
            </h2>
            <p className="text-sm text-indigo-950 leading-relaxed">{note.summary}</p>
          </div>
        )}

        {note.full_note && (
          <div>
            <h2 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-3">
              Full Content
            </h2>
            <div className="text-sm text-gray-700 leading-relaxed whitespace-pre-line bg-gray-50/50 p-4 rounded-lg border border-gray-100">
              {note.full_note}
            </div>
          </div>
        )}

        {note.tags && note.tags.length > 0 && (
          <div>
            <h2 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">
              Tags
            </h2>
            <div className="flex flex-wrap gap-2">
              {note.tags.map(tag => (
                <span
                  key={tag.id}
                  className="bg-gray-100 text-gray-700 px-2.5 py-1 rounded-md text-xs font-medium"
                >
                  #{tag.name}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}