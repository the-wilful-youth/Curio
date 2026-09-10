'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';

interface DeadlineItem {
  id: string;
  title: string;
  deadline_datetime: string;
  status: string;
}

interface NoteItem {
  id: string;
  title: string;
  summary?: string;
  category?: string;
  created_at: string;
}

interface TagItem {
  id: string;
  name: string;
}

export default function Dashboard() {
  const [upcoming, setUpcoming] = useState<DeadlineItem[]>([]);
  const [recent, setRecent] = useState<NoteItem[]>([]);
  const [categories, setCategories] = useState<TagItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const [upcomingRes, recentRes, tagsRes] = await Promise.all([
        fetch('/api/deadlines?status=upcoming&limit=5'),
        fetch('/api/notes?limit=6'),
        fetch('/api/tags?limit=12'),
      ]);

      if (upcomingRes.ok) {
        const data = await upcomingRes.json();
        setUpcoming(Array.isArray(data) ? data : []);
      }
      if (recentRes.ok) {
        const data = await recentRes.json();
        setRecent(Array.isArray(data) ? data : []);
      }
      if (tagsRes.ok) {
        const data = await tagsRes.json();
        setCategories(Array.isArray(data) ? data : []);
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Vault Overview</h1>
          <p className="text-sm text-slate-500 mt-1">
            Real-time feed of your captured notes, imminent deadlines, and topics
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Link
            href="/library"
            className="px-4 py-2 text-sm font-semibold text-slate-700 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 shadow-sm transition"
          >
            Browse Library ({recent.length})
          </Link>
          <Link
            href="/"
            className="px-4 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 shadow-sm transition"
          >
            + Add URL
          </Link>
        </div>
      </div>

      {loading ? (
        <div className="flex flex-col items-center justify-center h-64 bg-white rounded-xl border border-slate-100 shadow-sm">
          <div className="animate-spin rounded-full border-3 border-indigo-600 border-t-transparent w-8 h-8"></div>
          <p className="mt-3 text-sm text-slate-500">Loading your vault overview...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Recent Notes (2 columns) */}
          <div className="lg:col-span-2 space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-bold text-slate-900">Recent Content</h2>
              <Link href="/library" className="text-xs font-semibold text-indigo-600 hover:underline">
                View all →
              </Link>
            </div>

            {recent.length === 0 ? (
              <div className="text-center py-12 bg-white rounded-xl border border-dashed border-slate-200">
                <p className="text-sm font-medium text-slate-700">No notes saved yet</p>
                <p className="text-xs text-slate-400 mt-1">Start by saving your first link or article</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {recent.map((note) => (
                  <Link
                    key={note.id}
                    href={`/library/${note.id}`}
                    className="p-5 bg-white rounded-xl border border-slate-200 hover:border-indigo-300 hover:shadow-md transition flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex items-center justify-between gap-2 mb-2">
                        {note.category && (
                          <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">
                            {note.category}
                          </span>
                        )}
                        <span className="text-xs text-slate-400">
                          {new Date(note.created_at).toLocaleDateString()}
                        </span>
                      </div>
                      <h3 className="font-semibold text-slate-900 line-clamp-2">{note.title}</h3>
                      {note.summary && (
                        <p className="text-xs text-slate-500 mt-2 line-clamp-3 leading-relaxed">
                          {note.summary}
                        </p>
                      )}
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </div>

          {/* Sidebar: Upcoming & Topics (1 column) */}
          <div className="space-y-6">
            {/* Upcoming Deadlines */}
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-base font-bold text-slate-900">Upcoming Deadlines</h2>
                <Link href="/calendar" className="text-xs font-semibold text-indigo-600 hover:underline">
                  Calendar →
                </Link>
              </div>

              {upcoming.length === 0 ? (
                <p className="text-xs text-slate-400 text-center py-4">No deadlines recorded</p>
              ) : (
                <ul className="space-y-3">
                  {upcoming.map((item) => (
                    <li key={item.id} className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                      <div className="text-sm font-semibold text-slate-900">{item.title}</div>
                      <div className="text-xs text-indigo-600 font-medium mt-1">
                        📅 {new Date(item.deadline_datetime).toLocaleDateString(undefined, {
                          month: 'short',
                          day: 'numeric',
                          year: 'numeric'
                        })}
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </div>

            {/* Tags / Categories */}
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
              <h2 className="text-base font-bold text-slate-900 mb-3">Topic Tags</h2>
              {categories.length === 0 ? (
                <p className="text-xs text-slate-400 text-center py-4">No tags extracted yet</p>
              ) : (
                <div className="flex flex-wrap gap-2">
                  {categories.map((tag) => (
                    <span
                      key={tag.id}
                      className="px-2.5 py-1 rounded-md bg-slate-100 text-slate-700 text-xs font-medium hover:bg-slate-200 transition cursor-pointer"
                    >
                      #{tag.name}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </main>
  );
}