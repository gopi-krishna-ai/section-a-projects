import { createContext, useContext, useState } from "react";

export interface Profile {
  name: string;
  email: string;
  university: string;
  dailyGoal: number;
}

const STORAGE_KEY = "studyai-profile";

const DEFAULTS: Profile = {
  name: "Alex Johnson",
  email: "alex.johnson@university.edu",
  university: "State University of Technology",
  dailyGoal: 6,
};

function load(): Profile {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return DEFAULTS;
    return { ...DEFAULTS, ...JSON.parse(raw) };
  } catch {
    return DEFAULTS;
  }
}

interface ProfileContextValue {
  profile: Profile;
  saveProfile: (p: Profile) => void;
}

const ProfileContext = createContext<ProfileContextValue | null>(null);

export function ProfileProvider({ children }: { children: React.ReactNode }) {
  const [profile, setProfile] = useState<Profile>(load);

  const saveProfile = (p: Profile) => {
    setProfile(p);
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(p));
    } catch {
      // ignore quota errors
    }
  };

  return (
    <ProfileContext.Provider value={{ profile, saveProfile }}>
      {children}
    </ProfileContext.Provider>
  );
}

export function useProfile() {
  const ctx = useContext(ProfileContext);
  if (!ctx) throw new Error("useProfile must be used inside ProfileProvider");
  return ctx;
}
