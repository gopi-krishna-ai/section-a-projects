import { Outlet } from "react-router";
import { PublicNav } from "./PublicNav";
import { PublicFooter } from "./PublicFooter";

export function PublicLayout() {
  return (
    <div className="min-h-screen flex flex-col">
      <PublicNav />
      <main className="flex-1 pt-16">
        <Outlet />
      </main>
      <PublicFooter />
    </div>
  );
}
