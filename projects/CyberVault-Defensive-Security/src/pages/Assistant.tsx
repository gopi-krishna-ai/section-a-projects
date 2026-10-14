import { useState } from 'react';
import { MessageSquare, Send, Bot, User, Sparkles, ShieldCheck } from 'lucide-react';

export default function Assistant() {
  const [messages, setMessages] = useState<any[]>([
    {
      sender: 'bot',
      text: 'Hello, Analyst! I am CyberVault AI Security Assistant. I am configured to provide standardized defensive security advice, incident triage, and remediation solutions for all queries.',
      time: '11:00'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async (textToSend?: string) => {
    const text = textToSend || input;
    if (!text.trim()) return;

    const userMsg = { sender: 'user', text, time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) };
    setMessages((prev) => [...prev, userMsg]);
    if (!textToSend) setInput('');
    setLoading(true);

    try {
      const res = await fetch('http://127.0.0.1:8000/api/assistant-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });
      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        {
          sender: 'bot',
          text: data.reply,
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    } catch {
      // Default reply fallback
      setMessages((prev) => [
        ...prev,
        {
          sender: 'bot',
          text: 'CyberVault Default Security Advisory: Follow defensive cybersecurity guidelines. Ensure all exposed perimeter ports are restricted, enforce multi-factor authentication (MFA), and audit suspicious URLs with our threat model.',
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    }
    setLoading(false);
  };

  const quickPrompts = [
    'How do I respond to a phishing email attack?',
    'What should I do if an unencrypted Telnet port 23 is open?',
    'How to block SSH brute force attacks in server logs?',
    'What is the recommended password entropy and hashing policy?',
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      <div>
        <h1 className="text-2xl font-bold text-teal-400 flex items-center gap-2">
          <MessageSquare /> AI Cybersecurity Assistant
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Specialized defensive AI bot configured to deliver immediate security guidance and standardized remediation protocols for all inquiries.
        </p>
      </div>

      <div className="bg-[#0f172a] border border-slate-800 rounded-2xl flex flex-col h-[580px] shadow-2xl overflow-hidden">
        {/* Chat Window */}
        <div className="flex-1 p-5 overflow-y-auto space-y-4 custom-scrollbar">
          {messages.map((m, i) => (
            <div
              key={i}
              className={`flex gap-3 max-w-[85%] ${m.sender === 'user' ? 'ml-auto flex-row-reverse' : ''}`}
            >
              <div
                className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 text-xs font-bold ${
                  m.sender === 'bot'
                    ? 'bg-teal-500/20 text-teal-400 border border-teal-500/30'
                    : 'bg-slate-700 text-slate-200'
                }`}
              >
                {m.sender === 'bot' ? <Bot size={16} /> : <User size={16} />}
              </div>
              <div
                className={`p-4 rounded-xl text-xs leading-relaxed space-y-1 ${
                  m.sender === 'bot'
                    ? 'bg-[#0b1120] border border-slate-800 text-slate-200 shadow-md whitespace-pre-wrap'
                    : 'bg-teal-600 text-slate-950 font-medium'
                }`}
              >
                <p>{m.text}</p>
                <p className={`text-[10px] text-right ${m.sender === 'bot' ? 'text-slate-500' : 'text-slate-900/70'}`}>
                  {m.time}
                </p>
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex gap-3 items-center text-xs text-slate-500">
              <Bot size={16} className="text-teal-400 animate-pulse" />
              <span>CyberVault AI is analyzing defensive guidelines...</span>
            </div>
          )}
        </div>

        {/* Quick Prompts */}
        <div className="p-3 bg-[#0b1120]/80 border-t border-slate-800/80 flex gap-2 overflow-x-auto text-[11px]">
          <span className="text-slate-500 flex items-center gap-1 shrink-0 px-1 font-semibold">
            <Sparkles size={12} className="text-teal-400" /> Quick Inquiries:
          </span>
          {quickPrompts.map((q, idx) => (
            <button
              key={idx}
              onClick={() => sendMessage(q)}
              className="bg-slate-800 hover:bg-slate-700 text-slate-300 px-3 py-1 rounded-full whitespace-nowrap border border-slate-700/60 transition"
            >
              {q}
            </button>
          ))}
        </div>

        {/* Input Bar */}
        <div className="p-4 bg-[#0f172a] border-t border-slate-800 flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Ask about vulnerabilities, phishing triage, port hardening, or log alerts..."
            className="flex-1 bg-[#0b1120] border border-slate-700 rounded-xl px-4 py-3 text-xs text-slate-200 outline-none focus:border-teal-500 font-sans"
          />
          <button
            onClick={() => sendMessage()}
            disabled={!input.trim()}
            className="px-5 bg-teal-500 hover:bg-teal-400 disabled:opacity-50 text-slate-950 font-bold rounded-xl transition flex items-center justify-center gap-1 text-xs shadow-lg"
          >
            <Send size={15} /> Send
          </button>
        </div>
      </div>
    </div>
  );
}
