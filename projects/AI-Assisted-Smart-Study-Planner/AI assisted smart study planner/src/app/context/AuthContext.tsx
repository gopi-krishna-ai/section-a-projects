import { createContext, useContext, useState, useEffect } from "react";

export interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  university: string;
  emailVerified: boolean;
  createdAt: string;
  role: "student";
}

interface AuthContextValue {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string, remember?: boolean) => Promise<void>;
  signup: (name: string, email: string, password: string) => Promise<User>;
  logout: () => void;
  forgotPassword: (email: string) => Promise<void>;
  updateUser: (updates: Partial<User>) => void;
}

const STORAGE_KEY = "studyai-auth";

const DEFAULT_USER: User = {
  id: "user-1",
  name: "Alex Johnson",
  email: "alex.johnson@university.edu",
  university: "State University of Technology",
  emailVerified: true,
  createdAt: "2025-09-01",
  role: "student",
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) setUser(JSON.parse(raw));
    } catch { /* ignore */ }
    setIsLoading(false);
  }, []);

  const persist = (u: User | null) => {
    setUser(u);
    if (u) localStorage.setItem(STORAGE_KEY, JSON.stringify(u));
    else localStorage.removeItem(STORAGE_KEY);
  };

  const login = async (email: string, _password: string, remember = true) => {
    setIsLoading(true);
    await new Promise((r) => setTimeout(r, 1200));
    const u: User = { ...DEFAULT_USER, email, name: email.split("@")[0].replace(/[._]/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()) };
    if (remember) persist(u);
    else setUser(u);
    setIsLoading(false);
  };

  const signup = async (name: string, email: string, _password: string): Promise<User> => {
    setIsLoading(true);
    await new Promise((r) => setTimeout(r, 1400));
    const u: User = { id: `user-${Date.now()}`, name, email, university: "", emailVerified: false, createdAt: new Date().toISOString().split("T")[0], role: "student" };
    persist(u);
    setIsLoading(false);
    return u;
  };

  const logout = () => {
    persist(null);
  };

  const forgotPassword = async (_email: string) => {
    await new Promise((r) => setTimeout(r, 1000));
  };

  const updateUser = (updates: Partial<User>) => {
    if (!user) return;
    const updated = { ...user, ...updates };
    persist(updated);
  };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated: !!user, isLoading, login, signup, logout, forgotPassword, updateUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}
