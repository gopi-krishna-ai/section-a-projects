import { createContext, useContext, useEffect, useState } from "react";

export type ThemeId = "blue" | "green" | "purple" | "orange" | "rose" | "teal";

export interface ThemeOption {
  id: ThemeId;
  label: string;
  primary: string;
  secondary: string;
}

export const THEMES: ThemeOption[] = [
  { id: "blue",   label: "Ocean Blue",     primary: "#4F8EF7", secondary: "#7B61FF" },
  { id: "purple", label: "Royal Purple",   primary: "#8b5cf6", secondary: "#7c3aed" },
  { id: "green",  label: "Forest Green",   primary: "#10b981", secondary: "#059669" },
  { id: "orange", label: "Sunset Orange",  primary: "#f97316", secondary: "#ea580c" },
  { id: "rose",   label: "Cherry Rose",    primary: "#f43f5e", secondary: "#e11d48" },
  { id: "teal",   label: "Deep Teal",      primary: "#06b6d4", secondary: "#0891b2" },
];

interface ThemeColors {
  primary: string;
  secondary: string;
  gradient: string;
  pageBg: string;
  cardBg: string;
  cardBorder: string;
  textPrimary: string;
  textSecondary: string;
  navBg: string;
  topNavBg: string;
  inputBg: string;
  inputBorder: string;
  mutedBg: string;
}

interface ThemeContextValue {
  isDark: boolean;
  themeId: ThemeId;
  colors: ThemeColors;
  toggleDark: () => void;
  setThemeId: (id: ThemeId) => void;
  currentTheme: ThemeOption;
}

function buildColors(theme: ThemeOption, isDark: boolean): ThemeColors {
  if (isDark) {
    return {
      primary: theme.primary,
      secondary: theme.secondary,
      gradient: `linear-gradient(135deg, ${theme.primary}, ${theme.secondary})`,
      pageBg: "#0d1117",
      cardBg: "#161b27",
      cardBorder: "rgba(255,255,255,0.07)",
      textPrimary: "#e2e8f0",
      textSecondary: "#94a3b8",
      navBg: "linear-gradient(180deg, #0d1117 0%, #090d18 100%)",
      topNavBg: "rgba(13,17,23,0.96)",
      inputBg: "#1e2433",
      inputBorder: "rgba(255,255,255,0.1)",
      mutedBg: "#1a2035",
    };
  }
  return {
    primary: theme.primary,
    secondary: theme.secondary,
    gradient: `linear-gradient(135deg, ${theme.primary}, ${theme.secondary})`,
    pageBg: "#f0f4ff",
    cardBg: "#ffffff",
    cardBorder: "rgba(0,0,0,0.06)",
    textPrimary: "#1a1f3e",
    textSecondary: "#718096",
    navBg: "linear-gradient(180deg, #1a1f3e 0%, #0f1228 100%)",
    topNavBg: "rgba(248,250,255,0.95)",
    inputBg: "#f8faff",
    inputBorder: "#e2e8f0",
    mutedBg: "#f0f4ff",
  };
}

const ThemeContext = createContext<ThemeContextValue | null>(null);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [isDark, setIsDark] = useState<boolean>(() => {
    try { return localStorage.getItem("studyai-dark") === "true"; } catch { return false; }
  });
  const [themeId, setThemeIdState] = useState<ThemeId>(() => {
    try { return (localStorage.getItem("studyai-theme") as ThemeId) || "blue"; } catch { return "blue"; }
  });

  const currentTheme = THEMES.find((t) => t.id === themeId) ?? THEMES[0];
  const colors = buildColors(currentTheme, isDark);

  useEffect(() => {
    const root = document.documentElement;
    if (isDark) {
      root.classList.add("dark");
    } else {
      root.classList.remove("dark");
    }
    root.style.setProperty("--accent-primary", currentTheme.primary);
    root.style.setProperty("--accent-secondary", currentTheme.secondary);
    localStorage.setItem("studyai-dark", String(isDark));
  }, [isDark, currentTheme]);

  useEffect(() => {
    localStorage.setItem("studyai-theme", themeId);
  }, [themeId]);

  const toggleDark = () => setIsDark((d) => !d);
  const setThemeId = (id: ThemeId) => setThemeIdState(id);

  return (
    <ThemeContext.Provider value={{ isDark, themeId, colors, toggleDark, setThemeId, currentTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error("useTheme must be used inside ThemeProvider");
  return ctx;
}
