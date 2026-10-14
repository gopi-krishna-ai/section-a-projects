import React, { useState, useEffect, useRef } from "react";
import { Brain, Sparkles, Target, Zap, Send, User as UserIcon, Calendar } from "lucide-react";
import { useStudyData } from "../context/StudyDataContext";
import { useTheme } from "../context/ThemeContext";

type Message = {
  id: string;
  sender: "ai" | "user";
  text: string;
};

export function AIAssistantPage() {
  const { colors } = useTheme();
  const { tasks, subjects, addTask, addEvent } = useStudyData();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "init",
      sender: "ai",
      text: "Hello! I am your AI Study Assistant. I have full context of your tasks, subjects, and deadlines. How can I help you today? (Try asking me to 'create a schedule for today')",
    },
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const generateAIResponse = (prompt: string) => {
    const lower = prompt.toLowerCase();
    let responseText = "";

    const isAddingTask = (lower.includes("add ") && lower.includes("task")) || lower.includes("add a task") || lower.includes("remind me") || lower.includes("add event");
    const wantsSchedule = lower.includes("schedule") || lower.includes("shedule") || lower.includes("plan") || lower.includes("urgency") || lower.includes("routine");
    const isAskingTasks = lower.includes("what") && lower.includes("task") || lower.includes("show") && lower.includes("task") || lower.includes("my tasks");
    const wantsOverview = lower.includes("subject") || lower.includes("overview") || lower.includes("how am i doing") || lower.includes("status");

    const mentionedSubject = subjects.find(s => {
      const nameLower = s.name.toLowerCase();
      if (lower.includes(nameLower)) return true;
      if (nameLower.includes("artificial") && (lower.includes("artificial") || lower.includes("intel") || lower.includes("ai") || lower.includes("machine"))) return true;
      if (nameLower.includes("mathematics") && (lower.includes("math") || lower.includes("comp") || lower.includes("calc"))) return true;
      if (nameLower.includes("electronic") && (lower.includes("electronic") || lower.includes("circuit") || lower.includes("electrical"))) return true;
      if (nameLower.includes("data") && (lower.includes("data") || lower.includes("structure") || lower.includes("dsa") || lower.includes("algorithm"))) return true;
      if (nameLower.includes("python") && lower.includes("python")) return true;
      return false;
    });

    if (isAddingTask) {
      let title = prompt.replace(/(add a task|add task|remind me to|remind me|add event|add) (for |to )?/i, "").trim();
      let deadline = new Date().toISOString().split("T")[0];
      
      if (lower.includes("tomorrow") || lower.includes("tommarow") || lower.includes("tmrw")) {
        const d = new Date();
        d.setDate(d.getDate() + 1);
        deadline = d.toISOString().split("T")[0];
        title = title.replace(/(for )?(tomorrow|tommarow|tmrw)/i, "").trim();
      }

      let subjName = "General";
      let subjColor = "#64748b";
      if (mentionedSubject) {
        subjName = mentionedSubject.name;
        subjColor = mentionedSubject.color;
      }

      addTask({
        title: title || "New Task",
        subject: subjName,
        subjectColor: subjColor,
        priority: "medium",
        deadline: deadline,
        duration: "30m",
        completed: false,
        category: "Study"
      });

      responseText = `✅ **Task Added!**\n\nI have added "**${title || "New Task"}**" to your planner.`;

    } else if (isAskingTasks && !wantsSchedule) {
      const pendingTasks = tasks.filter(t => !t.completed);
      
      if (lower.includes("today")) {
        const todayStr = new Date().toISOString().split("T")[0];
        const todayTasks = pendingTasks.filter(t => t.deadline === todayStr);
        if (todayTasks.length === 0) {
          responseText = "You don't have any pending tasks scheduled for today! Enjoy your free time or get ahead on future work.";
        } else {
          responseText = "**Here are your tasks for today:**\n\n";
          todayTasks.forEach(t => {
            responseText += `- **${t.title}** (${t.subject}) - Priority: ${t.priority}\n`;
          });
        }
      } else {
        if (pendingTasks.length === 0) {
          responseText = "You are all caught up! You have no pending tasks right now.";
        } else {
          responseText = `**You have ${pendingTasks.length} pending tasks:**\n\n`;
          pendingTasks.slice(0, 5).forEach(t => {
            responseText += `- **${t.title}** (Due: ${t.deadline})\n`;
          });
          if (pendingTasks.length > 5) {
            responseText += `\n*...and ${pendingTasks.length - 5} more. Check your Tasks tab for the full list!*`;
          }
        }
      }

    } else if (wantsSchedule || (lower.includes("what") && lower.includes("do"))) {
      let relevantTasks = tasks.filter(t => !t.completed);
      let scheduleTitle = "**Here is a personalized study schedule based on urgency and availability:**\n\n";

      if (mentionedSubject) {
        relevantTasks = relevantTasks.filter(t => t.subject === mentionedSubject.name);
        scheduleTitle = `**Here is your focused study schedule for ${mentionedSubject.name}:**\n\n`;
      }

      if (relevantTasks.length === 0) {
        return `You have no pending tasks${mentionedSubject ? ` for **${mentionedSubject.name}**` : ''}! Great job! 🎉`;
      }

      const urgentTasks = relevantTasks.filter(t => new Date(t.deadline).getTime() <= new Date().getTime() + 2 * 86400000);
      const highPriority = relevantTasks.filter(t => t.priority === "high" && !urgentTasks.find(u => u.id === t.id));

      responseText = scheduleTitle;
      
      if (urgentTasks.length > 0) {
        responseText += "🔥 **Urgent Tasks (Do these first):**\n";
        urgentTasks.forEach(t => {
          responseText += `- **${t.title}** (${t.subject}) - Due: ${t.deadline}\n`;
        });
        responseText += "\n";
      }

      if (highPriority.length > 0) {
        responseText += "⭐ **High Priority (Next up):**\n";
        highPriority.forEach(t => {
          responseText += `- **${t.title}** (${t.subject})\n`;
        });
        responseText += "\n";
      }

      const others = relevantTasks.filter(t => !urgentTasks.find(u => u.id === t.id) && !highPriority.find(u => u.id === t.id));
      if (others.length > 0) {
        responseText += "📅 **Later this week:**\n";
        others.slice(0, 3).forEach(t => {
          responseText += `- ${t.title} (${t.subject})\n`;
        });
      }

    } else if (mentionedSubject) {
       const subjTasks = tasks.filter(t => t.subject === mentionedSubject.name);
       const pending = subjTasks.filter(t => !t.completed).length;
       
       responseText = `**Subject Overview: ${mentionedSubject.name}** ${mentionedSubject.emoji}\n\n`;
       responseText += `- **Progress:** ${mentionedSubject.completedHours}/${mentionedSubject.totalHours} hours completed.\n`;
       responseText += `- **Difficulty:** ${mentionedSubject.difficulty}\n`;
       responseText += `- **Tasks:** You have ${pending} pending task(s) for this subject.\n\n`;
       
    } else if (wantsOverview) {
      responseText = "**Overall Subject Overview:**\n\n";
      subjects.forEach(s => {
        responseText += `- **${s.name}** (${s.emoji}): ${s.completedHours}/${s.totalHours} hours completed.\n`;
      });
    } else {
      responseText = "I'm not sure I understood that perfectly. However, **you can ask me to:**\n- *'what are my tasks today?'*\n- *'plan my day'*\n- *'add a task to read chapter 5'*";
    }

    return responseText;
  };

  const handleSend = () => {
    if (!input.trim()) return;

    const newMsg: Message = { id: Date.now().toString(), sender: "user", text: input.trim() };
    setMessages(prev => [...prev, newMsg]);
    setInput("");
    setIsTyping(true);

    setTimeout(() => {
      const responseText = generateAIResponse(newMsg.text);
      setMessages(prev => [...prev, { id: Date.now().toString(), sender: "ai", text: responseText }]);
      setIsTyping(false);
    }, 1500);
  };

  const formatMarkdown = (text: string) => {
    const lines = text.split('\n');
    return lines.map((line, i) => {
      let formattedLine = line;
      const boldRegex = /\*\*(.*?)\*\*/g;
      const parts = [];
      let lastIndex = 0;
      let match;
      
      while ((match = boldRegex.exec(line)) !== null) {
        parts.push(line.slice(lastIndex, match.index));
        parts.push(<strong key={lastIndex} style={{ color: colors.text }}>{match[1]}</strong>);
        lastIndex = match.index + match[0].length;
      }
      parts.push(line.slice(lastIndex));
      
      if (line.startsWith('- ')) {
        return <li key={i} className="ml-4 list-disc mt-1">{parts.length > 1 ? parts : line.slice(2)}</li>;
      }
      
      return (
        <React.Fragment key={i}>
          {parts.length > 1 ? parts : line}
          {i < lines.length - 1 && <br />}
        </React.Fragment>
      );
    });
  };

  const features = [
    {
      icon: Calendar,
      title: "Smart Scheduling",
      desc: "Auto-generates study plans based on deadlines and task urgency.",
      color: "#10b981"
    },
    {
      icon: Target,
      title: "Task Prioritization",
      desc: "Identifies what needs your immediate attention.",
      color: "#ef4444"
    },
    {
      icon: Zap,
      title: "Context Aware",
      desc: "Knows your past performance and active subjects.",
      color: "#f59e0b"
    }
  ];

  return (
    <div className="space-y-6 max-w-5xl mx-auto pb-10">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-12 h-12 rounded-xl flex items-center justify-center shadow-lg" style={{ background: colors.gradient }}>
          <Brain className="w-6 h-6 text-white" />
        </div>
        <div>
          <h1 className="text-2xl font-bold" style={{ color: colors.text }}>AI Assistant</h1>
          <p style={{ color: colors.textLight }}>Your personal, context-aware study companion</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        {features.map((f, i) => (
          <div key={i} className="p-4 rounded-2xl flex items-start gap-4 transition-transform hover:scale-[1.02]" style={{ background: colors.cardBg, border: `1px solid ${colors.border}` }}>
            <div className="w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0" style={{ background: `${f.color}15` }}>
              <f.icon className="w-5 h-5" style={{ color: f.color }} />
            </div>
            <div>
              <h3 className="font-semibold mb-1" style={{ color: colors.text }}>{f.title}</h3>
              <p className="text-sm leading-relaxed" style={{ color: colors.textLight }}>{f.desc}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="rounded-2xl flex flex-col overflow-hidden" style={{ background: colors.cardBg, border: `1px solid ${colors.border}`, height: "500px" }}>
        
        {/* Chat Header */}
        <div className="px-5 py-4 border-b flex items-center gap-2" style={{ borderColor: colors.border, background: `${colors.primary}05` }}>
          <Sparkles className="w-5 h-5" style={{ color: colors.primary }} />
          <span className="font-semibold" style={{ color: colors.text }}>StudyAI Chat</span>
        </div>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-5 space-y-6">
          {messages.map((m) => (
            <div key={m.id} className={`flex gap-3 ${m.sender === "user" ? "flex-row-reverse" : "flex-row"}`}>
              <div className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 mt-1" style={{ background: m.sender === "ai" ? colors.gradient : colors.border }}>
                {m.sender === "ai" ? <Brain className="w-4 h-4 text-white" /> : <UserIcon className="w-4 h-4" style={{ color: colors.textLight }} />}
              </div>
              <div 
                className={`px-4 py-3 rounded-2xl max-w-[80%] text-sm leading-relaxed ${m.sender === "user" ? "rounded-tr-none" : "rounded-tl-none"}`}
                style={{ 
                  background: m.sender === "ai" ? `${colors.primary}10` : colors.border,
                  color: m.sender === "ai" ? colors.text : colors.text
                }}
              >
                {m.sender === "ai" ? formatMarkdown(m.text) : m.text}
              </div>
            </div>
          ))}
          {isTyping && (
            <div className="flex gap-3 flex-row">
              <div className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 mt-1" style={{ background: colors.gradient }}>
                <Brain className="w-4 h-4 text-white" />
              </div>
              <div className="px-4 py-4 rounded-2xl rounded-tl-none flex items-center gap-1" style={{ background: `${colors.primary}10` }}>
                <div className="w-1.5 h-1.5 rounded-full animate-bounce" style={{ background: colors.primary, animationDelay: "0ms" }}></div>
                <div className="w-1.5 h-1.5 rounded-full animate-bounce" style={{ background: colors.primary, animationDelay: "150ms" }}></div>
                <div className="w-1.5 h-1.5 rounded-full animate-bounce" style={{ background: colors.primary, animationDelay: "300ms" }}></div>
              </div>
            </div>
          )}
          <div ref={endOfMessagesRef} />
        </div>

        {/* Chat Input */}
        <div className="p-4 border-t" style={{ borderColor: colors.border, background: colors.bodyBg }}>
          <div className="relative flex items-center">
            <input 
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              placeholder="Ask me to plan your week or prioritize tasks..."
              className="w-full pl-4 pr-12 py-3 rounded-xl outline-none transition-shadow"
              style={{ 
                background: colors.cardBg, 
                border: `1px solid ${colors.border}`,
                color: colors.text
              }}
            />
            <button 
              onClick={handleSend}
              disabled={!input.trim() || isTyping}
              className="absolute right-2 w-8 h-8 rounded-lg flex items-center justify-center transition-opacity"
              style={{ 
                background: input.trim() && !isTyping ? colors.primary : colors.border,
                opacity: input.trim() && !isTyping ? 1 : 0.5,
                cursor: input.trim() && !isTyping ? "pointer" : "default"
              }}
            >
              <Send className="w-4 h-4 text-white" style={{ marginLeft: "-2px" }} />
            </button>
          </div>
          <div className="mt-3 flex flex-wrap gap-2">
             <button onClick={() => setInput("Create a schedule based on urgency")} className="text-xs px-3 py-1.5 rounded-full transition-colors" style={{ background: `${colors.primary}15`, color: colors.primary }}>
               Create schedule
             </button>
             <button onClick={() => setInput("What subjects do I have?")} className="text-xs px-3 py-1.5 rounded-full transition-colors" style={{ background: `${colors.primary}15`, color: colors.primary }}>
               Subject overview
             </button>
          </div>
        </div>

      </div>
    </div>
  );
}
