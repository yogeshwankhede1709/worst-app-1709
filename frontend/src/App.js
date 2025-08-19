import React, { useEffect, useState } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, NavLink, Link, useLocation } from "react-router-dom";
import axios from "axios";
import { Landing, Blogs, Tools, Path, Community } from "./pages/Sections";
import { Switch } from "./components/ui/switch";
import { Sun, Moon, ShieldHalf, BookOpen, Wrench, Route as RouteIcon, Users, Menu } from "lucide-react";
import { Sheet, SheetContent, SheetTrigger } from "./components/ui/sheet";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function useHello() {
  useEffect(() => {
    const helloWorldApi = async () => {
      try { const response = await axios.get(`${API}/`); console.log(response.data.message); }
      catch (e) { console.error("API check failed (non-blocking)"); }
    };
    helloWorldApi();
  }, []);
}

function Header({ theme, setTheme }) {
  const location = useLocation();
  const isHome = location.pathname === "/";

  return (
    <header className="dark-header">
      <a href="#main" className="skip-link">Skip to content</a>
      <Link to="/" className="flex items-center gap-3">
        <ShieldHalf color="#00FFD1" />
        <span className="nav-text">DevSecOps</span>
      </Link>

      <nav className="dark-nav" aria-label="Primary">
        <NavLink to="/blogs" className={({ isActive }) => `dark-nav-link ${isActive ? "active" : ""}`}><BookOpen size={18} /> Blogs</NavLink>
        <NavLink to="/tools" className={({ isActive }) => `dark-nav-link ${isActive ? "active" : ""}`}><Wrench size={18} /> Tools</NavLink>
        <NavLink to="/path" className={({ isActive }) => `dark-nav-link ${isActive ? "active" : ""}`}><RouteIcon size={18} /> Path</NavLink>
        <NavLink to="/community" className={({ isActive }) => `dark-nav-link ${isActive ? "active" : ""}`}><Users size={18} /> Community</NavLink>
      </nav>

      <div className="flex items-center gap-3">
        <span className="body-small hidden sm:block">Theme</span>
        <Switch checked={theme === "light"} onCheckedChange={(v) => setTheme(v ? "light" : "dark")} aria-label="Toggle theme" />
        {theme === "light" ? <Sun size={18} /> : <Moon size={18} />}

        {/* Mobile Menu */}
        <div className="lg:hidden">
          <Sheet>
            <SheetTrigger asChild>
              <button className="btn-secondary" aria-label="Open menu"><Menu size={18} /></button>
            </SheetTrigger>
            <SheetContent side="right" className="bg-[#121212] text-white border-l border-white/10 w-80">
              <div className="flex flex-col gap-4 mt-10">
                <NavLink to="/blogs" className={({ isActive }) => `dark-nav-link ${isActive ? "active" : ""}`}>Blogs</NavLink>
                <NavLink to="/tools" className={({ isActive }) => `dark-nav-link ${isActive ? "active" : ""}`}>Tools</NavLink>
                <NavLink to="/path" className={({ isActive }) => `dark-nav-link ${isActive ? "active" : ""}`}>Path</NavLink>
                <NavLink to="/community" className={({ isActive }) => `dark-nav-link ${isActive ? "active" : ""}`}>Community</NavLink>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  );
}

function Footer() {
  return (
    <footer className="dark-full-container" style={{ background: "#000" }}>
      <div className="dark-content-container pad-large">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-t border-white/10 pt-6">
          <p className="body-small">© {new Date().getFullYear()} DevSecOps — Built for developers, security, and ops.</p>
          <div className="flex gap-3">
            <Link to="/blogs" className="btn-secondary">Blogs</Link>
            <Link to="/tools" className="btn-secondary">Tools</Link>
            <Link to="/path" className="btn-secondary">Path</Link>
            <Link to="/community" className="btn-secondary">Community</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}

function ErrorBoundary({ children }) {
  const [error, setError] = useState(null);
  if (error) return <div className="dark-full-container"><div className="dark-content-container pad-large"><div className="glass-card p-6"><h2 className="heading-2 mb-2">Something went wrong</h2><p className="body-small">Please refresh the page.</p></div></div></div>;
  return (
    <React.Suspense fallback={<div className="dark-full-container"><div className="dark-content-container pad-large"><div className="glass-card p-6">Loading…</div></div></div>}>
      <React.ErrorBoundary fallbackRender={({ error }) => { setError(error); return null; }}>
        {children}
      </React.ErrorBoundary>
    </React.Suspense>
  );
}

function AppShell() {
  useHello();
  const [theme, setTheme] = useState(() => localStorage.getItem("theme") || "dark");
  useEffect(() => { localStorage.setItem("theme", theme); document.body.classList.toggle("light-mode", theme === "light"); }, [theme]);

  return (
    <div>
      <Header theme={theme} setTheme={setTheme} />
      <div style={{ paddingTop: 80 }} id="main">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/blogs" element={<Blogs />} />
          <Route path="/tools" element={<Tools />} />
          <Route path="/path" element={<Path />} />
          <Route path="/community" element={<Community />} />
        </Routes>
      </div>
      <Footer />
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <ErrorBoundary>
        <AppShell />
      </ErrorBoundary>
    </BrowserRouter>
  );
}