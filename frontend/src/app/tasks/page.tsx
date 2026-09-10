'use client';

import { useEffect, useState } from 'react';

interface ActionItem {
  id: string;
  title: string;
  description?: string;
  due_datetime?: string;
  priority?: number;
  completed: boolean;
  calendar_status: string;
}

export default function Tasks() {
  const [actionItems, setActionItems] = useState<ActionItem[]>([]);
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchActionItems();
  }, []);

  const fetchActionItems = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/action-items?limit=100');
      if (!response.ok) throw new Error(`Status ${response.status}`);
      const data = await response.json();
      if (Array.isArray(data)) {
        setActionItems(data);
      } else {
        setActionItems([]);
      }
    } catch (error) {
      console.error('Error fetching action items:', error);
      setActionItems([]);
    } finally {
      setLoading(false);
    }
  };

  const markComplete = async (id: string) => {
    try {
      // Optimistic update
      setActionItems(prev =>
        prev.map(item => item.id === id ? { ...item, completed: true } : item)
      );
      await fetch(`/api/action-items/${id}/complete`, {
        method: 'PATCH',
      });
    } catch (error) {
      console.error('Error marking action item as complete:', error);
      fetchActionItems();
    }
  };

  const incompleteItems = actionItems.filter(item => !item.completed);
  const completeItems = actionItems.filter(item => item.completed);

  const displayedItems =
    filter === 'pending'
      ? incompleteItems
      : filter === 'completed'
      ? completeItems
      : actionItems;

  return (
    <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Tasks & Action Items</h1>
          <p className="text-sm text-gray-500 mt-1">Track actions extracted from your saved content</p>
        </div>
        <div className="flex space-x-2 bg-gray-100 p-1 rounded-lg">
          <button
            onClick={() => setFilter('all')}
            className={`px-3 py-1.5 rounded-md text-xs font-medium transition ${
              filter === 'all'
                ? 'bg-white text-gray-900 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            All ({actionItems.length})
          </button>
          <button
            onClick={() => setFilter('pending')}
            className={`px-3 py-1.5 rounded-md text-xs font-medium transition ${
              filter === 'pending'
                ? 'bg-white text-gray-900 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Pending ({incompleteItems.length})
          </button>
          <button
            onClick={() => setFilter('completed')}
            className={`px-3 py-1.5 rounded-md text-xs font-medium transition ${
              filter === 'completed'
                ? 'bg-white text-gray-900 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Completed ({completeItems.length})
          </button>
        </div>
      </div>

      {loading ? (
        <div className="flex flex-col items-center justify-center h-64 bg-white rounded-xl border border-gray-100 shadow-sm">
          <div className="animate-spin rounded-full border-3 border-indigo-600 border-t-transparent w-8 h-8"></div>
          <p className="mt-3 text-sm text-gray-500">Loading tasks...</p>
        </div>
      ) : displayedItems.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-xl border border-dashed border-gray-200">
          <p className="text-base font-medium text-gray-800">No action items found</p>
          <p className="text-sm text-gray-500 mt-1">Save articles or videos to auto-extract tasks</p>
        </div>
      ) : (
        <div className="space-y-3">
          {displayedItems.map(item => (
            <div
              key={item.id}
              className={`flex items-center justify-between p-4 bg-white rounded-xl border transition hover:shadow-sm ${
                item.completed ? 'border-gray-200 bg-gray-50/50' : 'border-gray-200'
              }`}
            >
              <div className="flex items-start gap-3">
                <input
                  type="checkbox"
                  checked={item.completed}
                  onChange={() => !item.completed && markComplete(item.id)}
                  disabled={item.completed}
                  className="mt-1 h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                />
                <div>
                  <h3
                    className={`text-sm font-medium ${
                      item.completed ? 'line-through text-gray-400' : 'text-gray-900'
                    }`}
                  >
                    {item.title}
                  </h3>
                  {item.description && (
                    <p className="text-xs text-gray-500 mt-0.5">{item.description}</p>
                  )}
                  {item.due_datetime && (
                    <p className="text-xs text-indigo-600 mt-1">
                      Due: {new Date(item.due_datetime).toLocaleDateString()}
                    </p>
                  )}
                </div>
              </div>

              <div className="flex items-center gap-2">
                {item.priority && item.priority > 1 && (
                  <span
                    className={`text-xs px-2 py-0.5 rounded font-medium ${
                      item.priority === 3
                        ? 'bg-red-50 text-red-700'
                        : 'bg-amber-50 text-amber-700'
                    }`}
                  >
                    {item.priority === 3 ? 'High' : 'Medium'}
                  </span>
                )}
                {item.completed ? (
                  <span className="text-xs bg-emerald-50 text-emerald-700 px-2 py-0.5 rounded font-medium">
                    Done
                  </span>
                ) : (
                  <button
                    onClick={() => markComplete(item.id)}
                    className="text-xs font-medium text-indigo-600 hover:text-indigo-800 px-2.5 py-1 rounded bg-indigo-50 hover:bg-indigo-100 transition"
                  >
                    Complete
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}