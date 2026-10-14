import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./styles/index.css";
import App from "./app/App";

// Augment window so TS knows about our splash helper
declare global {
  interface Window {
    __removeSplash?: () => void;
  }
}

const rootEl = document.getElementById("root");

if (!rootEl) {
  throw new Error("[StudyAI] Root element #root not found in index.html.");
}

createRoot(rootEl).render(
  <StrictMode>
    <App />
  </StrictMode>
);

// Remove the splash screen once React has painted
requestAnimationFrame(() => {
  if (typeof window.__removeSplash === "function") {
    window.__removeSplash();
  }
});
