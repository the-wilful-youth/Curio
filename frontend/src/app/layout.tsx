import type { Metadata } from "next";
import Link from "next/link";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Curio — Personal AI Content Vault",
  description: "Capture, extract, and understand online articles, videos, events, and tasks with AI.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-slate-50 text-slate-900">
        <header className="sticky top-0 z-40 w-full border-b border-slate-200 bg-white/80 backdrop-blur-md">
          <div className="max-w-7xl mx-auto flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
            <div className="flex items-center gap-8">
              <Link href="/dashboard" className="flex items-center gap-2 font-bold text-lg text-slate-900 tracking-tight">
                <div className="h-8 w-8 rounded-lg bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center text-white font-bold text-sm shadow-sm">
                  C
                </div>
                <span>Curio</span>
              </Link>
              <nav className="hidden md:flex items-center space-x-1 text-sm font-medium">
                <Link
                  href="/dashboard"
                  className="px-3 py-2 rounded-md text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition"
                >
                  Dashboard
                </Link>
                <Link
                  href="/library"
                  className="px-3 py-2 rounded-md text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition"
                >
                  Library
                </Link>
                <Link
                  href="/calendar"
                  className="px-3 py-2 rounded-md text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition"
                >
                  Calendar
                </Link>
                <Link
                  href="/tasks"
                  className="px-3 py-2 rounded-md text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition"
                >
                  Tasks
                </Link>
                <Link
                  href="/search"
                  className="px-3 py-2 rounded-md text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition"
                >
                  Search
                </Link>
                <Link
                  href="/chat"
                  className="px-3 py-2 rounded-md text-indigo-600 hover:text-indigo-700 hover:bg-indigo-50 font-semibold transition"
                >
                  AI Chat
                </Link>
              </nav>
            </div>

            <div className="flex items-center gap-3">
              <Link
                href="/"
                className="inline-flex items-center justify-center rounded-lg bg-indigo-600 px-3.5 py-1.5 text-xs font-semibold text-white shadow-sm hover:bg-indigo-700 transition"
              >
                + Save Content
              </Link>
            </div>
          </div>
        </header>

        <div className="flex-1">{children}</div>

        <footer className="border-t border-slate-200 bg-white py-6 text-center text-xs text-slate-500">
          Curio Personal AI Content Vault • Private & Local First
        </footer>
      </body>
    </html>
  );
}
