import { RouterProvider } from "react-router";
import { router } from "./routes";
import { ThemeProvider } from "./context/ThemeContext";
import { ProfileProvider } from "./context/ProfileContext";
import { AuthProvider } from "./context/AuthContext";
import { StudyDataProvider } from "./context/StudyDataContext";

export default function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <ProfileProvider>
          <StudyDataProvider>
            <RouterProvider router={router} />
          </StudyDataProvider>
        </ProfileProvider>
      </AuthProvider>
    </ThemeProvider>
  );
}
