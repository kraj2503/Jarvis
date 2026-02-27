"use client";

import { useState } from "react";
import { invokeAgent } from "@/lib/api";
import { v4 as uuidv4 } from "uuid";

export default function Home() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const userId = "user-001";
  const sessionId = "session-001"; // later move to URL or cookie

  async function sendQuery() {
    if (!query.trim()) return;

    setLoading(true);
    setMessages((prev) => [...prev, `You: ${query}`]);

    try {
      const res = await invokeAgent({
        user_id: userId,
        session_id: sessionId,
        query,
      });

      setMessages((prev) => [...prev, `Jarvis: ${res}`]);
    } catch (err) {
      setMessages((prev) => [...prev, "Jarvis: Error occurred"]);
    }

    setQuery("");
    setLoading(false);
  }

  return (
    <main className="min-h-screen bg-black text-white p-6">
      <h1 className="text-3xl font-bold mb-6">Jarvis AI</h1>

      <div className="border border-gray-700 rounded-lg p-4 h-[60vh] overflow-y-auto mb-4">
        {messages.map((m, i) => (
          <div key={i} className="mb-2">
            {m}
          </div>
        ))}
        {loading && <div>Jarvis is thinking...</div>}
      </div>

      <div className="flex gap-2">
        <input
          className="flex-1 bg-gray-900 border border-gray-700 rounded px-3 py-2"
          placeholder="Ask Jarvis..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendQuery()}
        />
        <button onClick={sendQuery} className="bg-blue-600 px-4 py-2 rounded">
          Send
        </button>
      </div>
    </main>
  );
}
