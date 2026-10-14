import { Outlet } from "react-router";

export function AuthLayout() {
  return (
    <div className="min-h-screen" style={{ background: "linear-gradient(135deg, #f0f4ff 0%, #f8f0ff 100%)", fontFamily: "Inter, sans-serif" }}>
      <Outlet />
    </div>
  );
}
