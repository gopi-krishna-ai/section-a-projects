import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../api/client';
import { UserAccount } from '../types';

interface AuthContextType {
  currentUser: UserAccount | null;
  token: string | null;
  isLoading: boolean;
  demoUsers: UserAccount[];
  login: (username: string, password: string) => Promise<void>;
  register: (params: { username: string; password: string; email?: string; full_name?: string; target_company?: string }) => Promise<void>;
  logout: () => void;
  switchDemoUser: (username: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentUser, setCurrentUser] = useState<UserAccount | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [demoUsers, setDemoUsers] = useState<UserAccount[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    initAuth();
  }, []);

  const initAuth = async () => {
    try {
      // 1. Fetch demo users list
      const demos = await api.getDemoUsers();
      setDemoUsers(demos);

      // 2. Check stored session
      const storedToken = localStorage.getItem('aptitude_auth_token');
      const storedUser = localStorage.getItem('aptitude_user');

      if (storedToken && storedUser) {
        setToken(storedToken);
        setCurrentUser(JSON.parse(storedUser));
      } else if (demos.length > 0) {
        // Default to first demo user (Rohan Mistry) for seamless zero-barrier experience
        const defaultDemo = demos[0];
        const res = await api.switchDemo(defaultDemo.username);
        setToken(res.token);
        setCurrentUser(res.user);
      }
    } catch (err) {
      console.error('Failed to initialize auth', err);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (username: string, password: string) => {
    const res = await api.login(username, password);
    setToken(res.token);
    setCurrentUser(res.user);
  };

  const register = async (params: { username: string; password: string; email?: string; full_name?: string; target_company?: string }) => {
    const res = await api.register(params);
    setToken(res.token);
    setCurrentUser(res.user);
  };

  const logout = () => {
    api.logout();
    setToken(null);
    setCurrentUser(null);
  };

  const switchDemoUser = async (username: string) => {
    const res = await api.switchDemo(username);
    setToken(res.token);
    setCurrentUser(res.user);
  };

  return (
    <AuthContext.Provider
      value={{
        currentUser,
        token,
        isLoading,
        demoUsers,
        login,
        register,
        logout,
        switchDemoUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
