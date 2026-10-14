import { createBrowserRouter } from "react-router";
import { LandingPage } from "./pages/LandingPage";
import { LoginPage } from "./pages/LoginPage";
import { SignUpPage } from "./pages/SignUpPage";
import { ForgotPasswordPage } from "./pages/ForgotPasswordPage";
import { EmailVerificationPage } from "./pages/EmailVerificationPage";
import { DashboardPage } from "./pages/DashboardPage";
import { AddSubjectPage } from "./pages/AddSubjectPage";
import { TasksPage } from "./pages/TasksPage";
import { AnalyticsPage } from "./pages/AnalyticsPage";
import { SettingsPage } from "./pages/SettingsPage";
import { CalendarPage } from "./pages/CalendarPage";
import { NotesPage } from "./pages/NotesPage";
import { PomodoroPage } from "./pages/PomodoroPage";
import { PricingPage } from "./pages/PricingPage";
import { FeaturesPage } from "./pages/FeaturesPage";
import { AboutPage } from "./pages/AboutPage";
import { ContactPage } from "./pages/ContactPage";
import { FAQPage } from "./pages/FAQPage";
import { PrivacyPage } from "./pages/PrivacyPage";
import { TermsPage } from "./pages/TermsPage";
import { NotFoundPage } from "./pages/NotFoundPage";
import { AIAssistantPage } from "./pages/AIAssistantPage";
import { QuizPage } from "./pages/QuizPage";
import { Layout } from "./components/Layout";
import { PublicLayout } from "./components/PublicLayout";
import { AuthLayout } from "./components/AuthLayout";

export const router = createBrowserRouter([
  {
    Component: PublicLayout,
    children: [
      { path: "/", Component: LandingPage },
      { path: "/features", Component: FeaturesPage },
      { path: "/pricing", Component: PricingPage },
      { path: "/about", Component: AboutPage },
      { path: "/contact", Component: ContactPage },
      { path: "/faq", Component: FAQPage },
      { path: "/privacy", Component: PrivacyPage },
      { path: "/terms", Component: TermsPage },
    ],
  },
  {
    Component: AuthLayout,
    children: [
      { path: "/login", Component: LoginPage },
      { path: "/signup", Component: SignUpPage },
      { path: "/forgot-password", Component: ForgotPasswordPage },
      { path: "/verify-email", Component: EmailVerificationPage },
    ],
  },
  {
    path: "/app",
    Component: Layout,
    children: [
      { index: true, Component: DashboardPage },
      { path: "dashboard", Component: DashboardPage },
      { path: "planner", Component: AddSubjectPage },
      { path: "tasks", Component: TasksPage },
      { path: "calendar", Component: CalendarPage },
      { path: "notes", Component: NotesPage },
      { path: "pomodoro", Component: PomodoroPage },
      { path: "quiz", Component: QuizPage },
      { path: "analytics", Component: AnalyticsPage },
      { path: "settings", Component: SettingsPage },
      { path: "ai-assistant", Component: AIAssistantPage },
    ],
  },
  { path: "*", Component: NotFoundPage },
]);
