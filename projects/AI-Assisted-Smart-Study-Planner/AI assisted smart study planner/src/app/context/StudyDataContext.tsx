import { createContext, useContext, useState } from "react";

export interface Task {
  id: string;
  title: string;
  subject: string;
  subjectColor: string;
  priority: "high" | "medium" | "low";
  deadline: string;
  duration: string;
  completed: boolean;
  category: string;
  createdAt: string;
}

export interface Subject {
  id: string;
  name: string;
  color: string;
  emoji: string;
  totalHours: number;
  completedHours: number;
  difficulty: "Easy" | "Medium" | "Hard";
}

export interface Note {
  id: string;
  title: string;
  content: string;
  subject: string;
  subjectColor: string;
  tags: string[];
  updatedAt: string;
  createdAt: string;
}

export interface CalendarEvent {
  id: string;
  title: string;
  date: string;
  time: string;
  type: "exam" | "assignment" | "study" | "reminder";
  color: string;
  description: string;
}

const today = new Date();
const fmt = (d: Date) => d.toISOString().split("T")[0];
const addDays = (n: number) => fmt(new Date(today.getTime() + n * 86400000));

const INITIAL_TASKS: Task[] = [
  { id: "t1", title: "Complete Chapter 5 – Discrete Mathematics", subject: "Computation Mathematics", subjectColor: "#4F8EF7", priority: "high", deadline: addDays(1), duration: "2h", completed: true, category: "Study", createdAt: addDays(-2) },
  { id: "t2", title: "Solve 20 Circuit Analysis problems from Module 3", subject: "Basic Electronic Engineering", subjectColor: "#7B61FF", priority: "high", deadline: addDays(1), duration: "1.5h", completed: true, category: "Practice", createdAt: addDays(-2) },
  { id: "t3", title: "Review Binary Tree algorithms", subject: "Data Structures", subjectColor: "#10b981", priority: "medium", deadline: addDays(2), duration: "1h", completed: true, category: "Revision", createdAt: addDays(-1) },
  { id: "t4", title: "Study Deep Learning fundamentals – Chapter 4", subject: "Artificial Intelligence", subjectColor: "#f59e0b", priority: "medium", deadline: addDays(2), duration: "45m", completed: false, category: "Reading", createdAt: addDays(-1) },
  { id: "t5", title: "Write Python script for data analysis project", subject: "Python", subjectColor: "#ef4444", priority: "low", deadline: addDays(3), duration: "1h", completed: false, category: "Study", createdAt: addDays(0) },
  { id: "t6", title: "Practice 10 Calculus integration problems", subject: "Computation Mathematics", subjectColor: "#4F8EF7", priority: "high", deadline: addDays(0), duration: "1.5h", completed: false, category: "Practice", createdAt: addDays(0) },
  { id: "t7", title: "Complete Lab Report – DC Circuit Analysis", subject: "Basic Electronic Engineering", subjectColor: "#7B61FF", priority: "high", deadline: addDays(4), duration: "2h", completed: false, category: "Assignment", createdAt: addDays(0) },
  { id: "t8", title: "Revise sorting algorithms flashcards", subject: "Data Structures", subjectColor: "#10b981", priority: "low", deadline: addDays(5), duration: "30m", completed: false, category: "Revision", createdAt: addDays(0) },
];

const INITIAL_SUBJECTS: Subject[] = [
  { id: "s1", name: "Computation Mathematics", color: "#4F8EF7", emoji: "📐", totalHours: 4, completedHours: 2.5, difficulty: "Hard" },
  { id: "s2", name: "Basic Electronic Engineering", color: "#7B61FF", emoji: "⚡", totalHours: 3, completedHours: 3, difficulty: "Hard" },
  { id: "s3", name: "Data Structures", color: "#10b981", emoji: "💻", totalHours: 5, completedHours: 2, difficulty: "Medium" },
  { id: "s4", name: "Artificial Intelligence", color: "#f59e0b", emoji: "🤖", totalHours: 2, completedHours: 1.5, difficulty: "Medium" },
  { id: "s5", name: "Python", color: "#ef4444", emoji: "🐍", totalHours: 3, completedHours: 0.5, difficulty: "Easy" },
];

const INITIAL_NOTES: Note[] = [
  { id: "n1", title: "Discrete Mathematics – Key Concepts", content: "## First-Order Logic\n\nA proposition is a declarative statement that is either true or false.\n\n**Predicate logic:** ∀x P(x) means 'for all x, P(x) is true'\n\n## Proof Techniques\n\nDirect proof, proof by contradiction, proof by induction.\n\n## Set Theory\n\nA set is a collection of distinct objects.\n\nOperations: Union (A ∪ B), Intersection (A ∩ B), Complement (A'), Difference (A − B)\n\n## Graph Theory\n\nA graph G = (V, E) consists of vertices V and edges E.", subject: "Computation Mathematics", subjectColor: "#4F8EF7", tags: ["calculus", "logic", "exam-prep"], updatedAt: addDays(-1), createdAt: addDays(-3) },
  { id: "n2", title: "Basic Electronics – Circuit Analysis", content: "## Ohm's Law\n\nV = IR\n- V = Voltage (Volts)\n- I = Current (Amperes)\n- R = Resistance (Ohms)\n\n## Kirchhoff's Laws\n\n**KVL:** The sum of all voltages around any closed loop equals zero.\n\n**KCL:** The sum of all currents entering a node equals the sum leaving.\n\n## RC Circuits\n\nTime constant τ = RC\nVoltage: V(t) = V₀(1 − e^(−t/τ))", subject: "Basic Electronic Engineering", subjectColor: "#7B61FF", tags: ["circuits", "electronics", "formulas"], updatedAt: addDays(-2), createdAt: addDays(-5) },
  { id: "n3", title: "Binary Trees – Operations & Complexity", content: "## Tree Traversals\n\n- **Inorder** (L-N-R): Gives sorted sequence for BST\n- **Preorder** (N-L-R): Used for copying trees\n- **Postorder** (L-R-N): Used for deletion\n\n## Time Complexities\n\n| Operation | Average | Worst |\n|-----------|---------|-------|\n| Search    | O(log n)| O(n)  |\n| Insert    | O(log n)| O(n)  |\n| Delete    | O(log n)| O(n)  |", subject: "Data Structures", subjectColor: "#10b981", tags: ["trees", "bst", "algorithms"], updatedAt: addDays(-3), createdAt: addDays(-7) },
  { id: "n4", title: "Machine Learning – Core Algorithms", content: "## Supervised Learning\n\n1. **Linear Regression** – predicts continuous values using y = mx + b\n2. **Logistic Regression** – binary classification using sigmoid: σ(z) = 1 / (1 + e^(−z))\n3. **Decision Trees** – splits data on feature thresholds\n\n## Neural Networks\n\n> Layers: Input → Hidden → Output\n\nActivation functions: ReLU, Sigmoid, Tanh\n\nBackpropagation updates weights using gradient descent:\nΔw = −η × ∂L/∂w", subject: "Artificial Intelligence", subjectColor: "#f59e0b", tags: ["ml", "neural-nets", "algorithms"], updatedAt: addDays(-4), createdAt: addDays(-8) },
];

const INITIAL_EVENTS: CalendarEvent[] = [
  { id: "e1", title: "Comp. Math Midterm Exam", date: addDays(3), time: "09:00", type: "exam", color: "#ef4444", description: "Chapters 1–5: Discrete Math and Calculus" },
  { id: "e2", title: "Electronics Lab Report Due", date: addDays(4), time: "23:59", type: "assignment", color: "#7B61FF", description: "DC Circuit analysis experiment report submission" },
  { id: "e3", title: "Data Structures Study Session", date: addDays(1), time: "18:00", type: "study", color: "#10b981", description: "Review binary trees and graph algorithms" },
  { id: "e4", title: "AI Assignment Due", date: addDays(7), time: "17:00", type: "assignment", color: "#f59e0b", description: "Implement a simple neural network from scratch" },
  { id: "e5", title: "Python Quiz", date: addDays(6), time: "14:00", type: "exam", color: "#ef4444", description: "Python OOP and data structures" },
  { id: "e6", title: "Study Group – Electronics", date: addDays(2), time: "16:00", type: "study", color: "#4F8EF7", description: "Group review session for midterm" },
  { id: "e7", title: "Office Hours – Prof. Martinez", date: addDays(0), time: "13:00", type: "reminder", color: "#6366f1", description: "Ask about problem set 4" },
  { id: "e8", title: "Final Exams Begin", date: addDays(14), time: "09:00", type: "exam", color: "#ef4444", description: "Two-week exam period starts" },
];

interface StudyDataContextValue {
  tasks: Task[];
  subjects: Subject[];
  notes: Note[];
  events: CalendarEvent[];
  addTask: (t: Omit<Task, "id" | "createdAt">) => void;
  updateTask: (id: string, updates: Partial<Task>) => void;
  deleteTask: (id: string) => void;
  toggleTask: (id: string) => void;
  addSubject: (s: Omit<Subject, "id">) => void;
  updateSubject: (id: string, updates: Partial<Subject>) => void;
  deleteSubject: (id: string) => void;
  addNote: (n: Omit<Note, "id" | "createdAt" | "updatedAt">) => void;
  updateNote: (id: string, updates: Partial<Note>) => void;
  deleteNote: (id: string) => void;
  addEvent: (e: Omit<CalendarEvent, "id">) => void;
  updateEvent: (id: string, updates: Partial<CalendarEvent>) => void;
  deleteEvent: (id: string) => void;
}

const StudyDataContext = createContext<StudyDataContextValue | null>(null);

export function StudyDataProvider({ children }: { children: React.ReactNode }) {
  const [tasks, setTasks] = useState<Task[]>(INITIAL_TASKS);
  const [subjects, setSubjects] = useState<Subject[]>(INITIAL_SUBJECTS);
  const [notes, setNotes] = useState<Note[]>(INITIAL_NOTES);
  const [events, setEvents] = useState<CalendarEvent[]>(INITIAL_EVENTS);

  const uid = () => `${Date.now()}-${Math.random().toString(36).slice(2)}`;
  const now = () => new Date().toISOString().split("T")[0];

  const addTask = (t: Omit<Task, "id" | "createdAt">) => setTasks(p => [{ ...t, id: uid(), createdAt: now() }, ...p]);
  const updateTask = (id: string, u: Partial<Task>) => setTasks(p => p.map(t => t.id === id ? { ...t, ...u } : t));
  const deleteTask = (id: string) => setTasks(p => p.filter(t => t.id !== id));
  const toggleTask = (id: string) => setTasks(p => p.map(t => t.id === id ? { ...t, completed: !t.completed } : t));

  const addSubject = (s: Omit<Subject, "id">) => setSubjects(p => [...p, { ...s, id: uid() }]);
  const updateSubject = (id: string, u: Partial<Subject>) => {
    setSubjects(prev => {
      const old = prev.find(s => s.id === id);
      if (old && u.name && u.name !== old.name) {
        const newColor = u.color ?? old.color;
        setTasks(t => t.map(task => task.subject === old.name ? { ...task, subject: u.name!, subjectColor: newColor } : task));
        setNotes(n => n.map(note => note.subject === old.name ? { ...note, subject: u.name!, subjectColor: newColor } : note));
      }
      return prev.map(s => s.id === id ? { ...s, ...u } : s);
    });
  };
  const deleteSubject = (id: string) => setSubjects(p => p.filter(s => s.id !== id));

  const addNote = (n: Omit<Note, "id" | "createdAt" | "updatedAt">) => {
    const ts = now();
    setNotes(p => [{ ...n, id: uid(), createdAt: ts, updatedAt: ts }, ...p]);
  };
  const updateNote = (id: string, u: Partial<Note>) => setNotes(p => p.map(n => n.id === id ? { ...n, ...u, updatedAt: now() } : n));
  const deleteNote = (id: string) => setNotes(p => p.filter(n => n.id !== id));

  const addEvent = (e: Omit<CalendarEvent, "id">) => setEvents(p => [...p, { ...e, id: uid() }]);
  const updateEvent = (id: string, u: Partial<CalendarEvent>) => setEvents(p => p.map(e => e.id === id ? { ...e, ...u } : e));
  const deleteEvent = (id: string) => setEvents(p => p.filter(e => e.id !== id));

  return (
    <StudyDataContext.Provider value={{ tasks, subjects, notes, events, addTask, updateTask, deleteTask, toggleTask, addSubject, updateSubject, deleteSubject, addNote, updateNote, deleteNote, addEvent, updateEvent, deleteEvent }}>
      {children}
    </StudyDataContext.Provider>
  );
}

export function useStudyData() {
  const ctx = useContext(StudyDataContext);
  if (!ctx) throw new Error("useStudyData must be used inside StudyDataProvider");
  return ctx;
}
