'use client';

import { useEffect, useState } from 'react';

interface CalendarEvent {
  id: string;
  title: string;
  description?: string;
  start_datetime: string;
  end_datetime?: string;
  location?: string;
  calendar_status: string;
}

interface CalendarDeadline {
  id: string;
  title: string;
  deadline_datetime: string;
  status: string;
  confidence?: number;
  calendar_status: string;
}

interface MergedItem {
  id: string;
  type: 'event' | 'deadline';
  date: string;
  title: string;
  description?: string;
  location?: string;
}

export default function Calendar() {
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [deadlines, setDeadlines] = useState<CalendarDeadline[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCalendarData();
  }, []);

  const fetchCalendarData = async () => {
    setLoading(true);
    try {
      const [eventsRes, deadlinesRes] = await Promise.all([
        fetch('/api/events?limit=50'),
        fetch('/api/deadlines?limit=50'),
      ]);

      if (eventsRes.ok) {
        const data = await eventsRes.json();
        setEvents(Array.isArray(data) ? data : []);
      }
      if (deadlinesRes.ok) {
        const data = await deadlinesRes.json();
        setDeadlines(Array.isArray(data) ? data : []);
      }
    } catch (error) {
      console.error('Error fetching calendar data:', error);
    } finally {
      setLoading(false);
    }
  };

  const allItems: MergedItem[] = [
    ...events.map(
      (e): MergedItem => ({
        id: e.id,
        type: 'event',
        date: e.start_datetime,
        title: e.title,
        description: e.description,
        location: e.location,
      })
    ),
    ...deadlines.map(
      (d): MergedItem => ({
        id: d.id,
        type: 'deadline',
        date: d.deadline_datetime,
        title: d.title,
        description: `Deadline with confidence ${Math.round((d.confidence || 1) * 100)}%`,
      })
    ),
  ].sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

  return (
    <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Schedule & Calendar</h1>
          <p className="text-sm text-gray-500 mt-1">
            Chronological view of detected events, conferences, and deadlines
          </p>
        </div>
      </div>

      {loading ? (
        <div className="flex flex-col items-center justify-center h-64 bg-white rounded-xl border border-gray-100 shadow-sm">
          <div className="animate-spin rounded-full border-3 border-indigo-600 border-t-transparent w-8 h-8"></div>
          <p className="mt-3 text-sm text-gray-500">Loading schedule...</p>
        </div>
      ) : allItems.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-xl border border-dashed border-gray-200">
          <p className="text-base font-medium text-gray-800">No scheduled events or deadlines</p>
          <p className="text-sm text-gray-500 mt-1">
            Save content with dates or deadlines to see them appear here
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {allItems.map(item => (
            <div
              key={`${item.type}-${item.id}`}
              className="p-5 bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition"
            >
              <div className="flex items-start justify-between gap-4">
                <div>
                  <div className="flex items-center gap-2">
                    <span
                      className={`text-xs px-2.5 py-0.5 rounded-full font-semibold ${
                        item.type === 'event'
                          ? 'bg-blue-50 text-blue-700'
                          : 'bg-amber-50 text-amber-700'
                      }`}
                    >
                      {item.type === 'event' ? 'Event' : 'Deadline'}
                    </span>
                    {item.location && (
                      <span className="text-xs text-gray-500">📍 {item.location}</span>
                    )}
                  </div>
                  <h3 className="text-base font-semibold text-gray-900 mt-2">{item.title}</h3>
                  {item.description && (
                    <p className="text-sm text-gray-600 mt-1">{item.description}</p>
                  )}
                </div>

                <div className="text-right shrink-0">
                  <div className="text-sm font-semibold text-indigo-600">
                    {new Date(item.date).toLocaleDateString(undefined, {
                      month: 'short',
                      day: 'numeric',
                      year: 'numeric',
                    })}
                  </div>
                  <div className="text-xs text-gray-400 mt-0.5">
                    {new Date(item.date).toLocaleTimeString(undefined, {
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}