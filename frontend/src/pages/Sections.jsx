import React, { useEffect, useMemo, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { mock } from "../mock";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "../components/ui/accordion";
import { Badge } from "../components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { ScrollArea } from "../components/ui/scroll-area";
import { Input } from "../components/ui/input";
import { Textarea } from "../components/ui/textarea";
import { Progress } from "../components/ui/progress";
import { Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { Button as ShadButton } from "../components/ui/button";
import { Heart, Bookmark, Search, Send, Layers, Shield, Route, Users } from "lucide-react";

// Utility helpers
const ls = {
  get(key, fallback) { try { const v = localStorage.getItem(key); return v ? JSON.parse(v) : fallback; } catch { return fallback; } },
  set(key, value) { try { localStorage.setItem(key, JSON.stringify(value)); } catch {} },
};

function SectionHeader({ title, subtitle }) {
  return (
    <div className="mb-6">
      <h2 className="display-large mb-2">{title}</h2>
      {subtitle && <p className="body-small text-white/70">{subtitle}</p>}
    </div>
  );
}

// Landing Page
export function Landing() {
  const features = [
    { icon: <Shield size={20} />, title: "Shift Left, Ship Faster", text: "Bake security into code reviews and pipelines to reduce rework and MTTR." },
    { icon: <Layers size={20} />, title: "Secure Supply Chain", text: "SBOMs, signing, and provenance deliver trust from source to runtime." },
    { icon: <Route size={20} />, title: "Automated Guardrails", text: "Policy-as-code enforces standards without blocking dev velocity." },
    { icon: <Users size={20} />, title: "Culture + Tools", text: "Security becomes a team sport when tooling aligns with workflows." },
  ];

  return (
    <main>
      {/* Hero */}
      <section className="dark-full-container" style={{ background: "#000" }}>
        <div className="dark-content-container" style={{ paddingTop: 120, paddingBottom: 80 }}>
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
            <div className="lg:col-span-7">
              <h1 className="display-huge mb-6">Why DevSecOps is the Future</h1>
              <p className="body-medium mb-8 max-w-2xl text-white/80">Security cannot be a gate at the end. It must be integrated into every stage of delivery — from code to cloud — without slowing teams. This is how modern software wins.</p>
              <div className="flex flex-wrap items-center gap-4">
                <Link to="/blogs" className="btn-primary" aria-label="Go to Blogs">Blogs</Link>
                <Link to="/tools" className="btn-primary" aria-label="Go to Tools">Tools</Link>
                <Link to="/path" className="btn-primary" aria-label="Go to Path">Path</Link>
                <Link to="/community" className="btn-primary" aria-label="Go to Community">Community</Link>
                <a href="#why" className="btn-secondary">Learn why</a>
              </div>
            </div>
            <div className="lg:col-span-5">
              {/* Decorative shapes - static, subtle */}
              <div className="glass-card relative overflow-hidden" style={{ height: 360 }}>
                <div className="absolute inset-0 pointer-events-none" aria-hidden>
                  <svg width="100%" height="100%">
                    <defs>
                      <linearGradient id="grad" x1="0" y1="0" x2="1" y2="1">
                        <stop offset="0%" stopColor="rgba(111,210,192,0.15)" />
                        <stop offset="100%" stopColor="rgba(0,255,209,0.05)" />
                      </linearGradient>
                    </defs>
                    <rect x="0" y="0" width="100%" height="100%" fill="url(#grad)" />
                    {[...Array(12)].map((_, i) => (
                      <circle key={i} cx={(i * 70) % 600} cy={(i * 45) % 360} r={(i % 4 + 1) * 8} fill="#00FFD133" />
                    ))}
                  </svg>
                </div>
                <div className="p-6 relative z-10">
                  <h3 className="heading-2 mb-2">Secure by Design</h3>
                  <p className="body-small text-white/70">A resilient pipeline verifies integrity, automates checks, and gives developers instant feedback.</p>
                  <ul className="mt-6 grid grid-cols-2 gap-2 text-sm text-white/70">
                    <li>• SAST &amp; IaC checks</li>
                    <li>• SBOM + signing</li>
                    <li>• Policy-as-code</li>
                    <li>• Runtime signals</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Why Section */}
      <section id="why" className="dark-full-container" style={{ background: "#000" }}>
        <div className="dark-content-container pad-large">
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
            {features.map((f, idx) => (
              <div key={idx} className="glass-card p-6 dark-hover">
                <div className="flex items-center gap-3 mb-3 text-[#00FFD1]">{f.icon}<span className="heading-3">{f.title}</span></div>
                <p className="body-small text-white/70">{f.text}</p>
              </div>
            ))}
          </div>

          <div className="mt-16">
            <Accordion type="single" collapsible className="w-full">
              <AccordionItem value="item-1">
                <AccordionTrigger>Is this site using mock data now?</AccordionTrigger>
                <AccordionContent>
                  Yes. All content is mocked on the frontend for now to deliver the experience quickly. We will wire real backends and microservices next.
                </AccordionContent>
              </AccordionItem>
              <AccordionItem value="item-2">
                <AccordionTrigger>Will there be light and dark themes?</AccordionTrigger>
                <AccordionContent>
                  Yes. Sub-pages support theme toggling on surface elements while the main background remains black for optimal contrast.
                </AccordionContent>
              </AccordionItem>
            </Accordion>
          </div>
        </div>
      </section>
    </main>
  );
}

// Blogs Page (Masonry-style without large bright images)
export function Blogs() {
  const [raw, setRaw] = useState("");
  const [query, setQuery] = useState("");
  const [saved, setSaved] = useState(() => ls.get("savedBlogs", {}));

  useEffect(() => { const t = setTimeout(() => setQuery(raw), 200); return () => clearTimeout(t); }, [raw]);
  useEffect(() => { ls.set("savedBlogs", saved); }, [saved]);

  const filtered = useMemo(() => {
    const q = query.toLowerCase();
    return mock.blogs.filter(b => b.title.toLowerCase().includes(q) || b.excerpt.toLowerCase().includes(q) || b.tags.some(t => t.toLowerCase().includes(q)));
  }, [query]);

  return (
    <div className="dark-full-container" style={{ background: "var(--bg-primary)" }}>
      <div className="dark-content-container pad-large">
        <div className="flex items-center justify-between gap-4 mb-6">
          <SectionHeader title="Blogs" />
          <div className="flex items-center gap-2 w-full max-w-md">
            <Search size={18} className="text-white/60" />
            <Input placeholder="Search posts, tags, authors..." value={raw} onChange={e => setRaw(e.target.value)} className="bg-[#121212] text-white border-border" aria-label="Search blogs" />
          </div>
        </div>

        <div className="columns-1 sm:columns-2 lg:columns-3 gap-6 [column-fill:_balance]">
          {filtered.map(post => (
            <article key={post.id} className="mb-6 break-inside-avoid">
              <Card className="bg-[#121212] border-border">
                <CardHeader>
                  <CardTitle className="heading-2">{post.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="body-small text-white/70 mb-3">{post.excerpt}</p>
                  <div className="flex flex-wrap gap-2 mb-4">
                    {post.tags.map((t, i) => (<Badge key={i} className="bg-white/10 text-white border-0">{t}</Badge>))}
                  </div>
                  <div className="flex items-center justify-between text-sm text-white/60">
                    <span>{post.author} • {new Date(post.date).toLocaleDateString()}</span>
                    <div className="flex items-center gap-2">
                      <ShadButton variant="ghost" className="text-white/70 hover:text-[#00FFD1]" aria-label="Save" onClick={() => setSaved(s => ({ ...s, [post.id]: !s[post.id] }))}>
                        <Bookmark size={18} fill={saved[post.id] ? "#00FFD1" : "none"} color={saved[post.id] ? "#00FFD1" : "currentColor"} />
                      </ShadButton>
                      <ShadButton variant="ghost" className="text-white/70 hover:text-[#00FFD1]" aria-label="Like"><Heart size={18} /></ShadButton>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </article>
          ))}
        </div>
      </div>
    </div>
  );
}

// Tools Page
export function Tools() {
  const [category, setCategory] = useState("all");
  const [sort, setSort] = useState("name");
  const cats = useMemo(() => ["all", ...Array.from(new Set(mock.tools.map(t => t.category)))], []);
  const data = useMemo(() => {
    const filtered = mock.tools.filter(t => category === "all" || t.category === category);
    const sorted = [...filtered].sort((a, b) => sort === "name" ? a.name.localeCompare(b.name) : a.category.localeCompare(b.category));
    return sorted;
  }, [category, sort]);

  return (
    <div className="dark-full-container" style={{ background: "var(--bg-primary)" }}>
      <div className="dark-content-container pad-large">
        <div className="flex items-center justify-between gap-4 mb-6">
          <SectionHeader title="Tools" />
          <div className="flex items-center gap-2">
            <Select value={category} onValueChange={setCategory}>
              <SelectTrigger className="w-40 bg-[#121212] text-white border-border" aria-label="Filter category"><SelectValue placeholder="Filter" /></SelectTrigger>
              <SelectContent className="bg-[#121212] text-white"><SelectGroup>{cats.map(c => (<SelectItem key={c} value={c}>{c}</SelectItem>))}</SelectGroup></SelectContent>
            </Select>
            <Select value={sort} onValueChange={setSort}>
              <SelectTrigger className="w-36 bg-[#121212] text-white border-border" aria-label="Sort by"><SelectValue placeholder="Sort" /></SelectTrigger>
              <SelectContent className="bg-[#121212] text-white"><SelectGroup>
                <SelectItem value="name">Name</SelectItem>
                <SelectItem value="category">Category</SelectItem>
              </SelectGroup></SelectContent>
            </Select>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {data.map(tool => (
            <Card key={tool.id} className="bg-[#121212] border-border dark-hover">
              <CardHeader>
                <CardTitle className="heading-2">{tool.name}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="body-small text-white/70 mb-3">{tool.description}</p>
                <div className="flex flex-wrap gap-2 mb-4">
                  {tool.tags.map((t, i) => (<Badge key={i} className="bg-white/10 text-white border-0">{t}</Badge>))}
                </div>
                <a href={tool.url} target="_blank" rel="noreferrer" className="btn-primary" aria-label={`Visit ${tool.name}`}>Visit</a>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}

// Path Page
export function Path() {
  const key = "pathProgress";
  const [done, setDone] = useState(() => new Set(ls.get(key, [])));
  useEffect(() => { ls.set(key, Array.from(done)); }, [done]);

  const total = mock.path.length;
  const completed = done.size;
  const pct = Math.round((completed / total) * 100);

  return (
    <div className="dark-full-container" style={{ background: "var(--bg-primary)" }}>
      <div className="dark-content-container pad-large max-w-5xl">
        <SectionHeader title="Learning Path" subtitle="Modeled after structured platforms like KodeKloud — track your progress and build real skills." />
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2"><span className="body-small">Progress: {completed}/{total}</span><span className="body-small">{pct}%</span></div>
          <Progress value={pct} className="h-2" />
        </div>

        <ol className="relative border-l border-white/10 pl-6">
          {mock.path.map(step => (
            <li key={step.id} className="mb-8">
              <div className="absolute -left-2 mt-1.5 h-3 w-3 rounded-full" style={{ background: done.has(step.id) ? "#00FFD1" : "#2a2a2a" }} />
              <div className="glass-card p-4">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <h3 className="heading-2">{step.label}</h3>
                    <p className="body-muted">~{Math.round(step.durationMin / 60)}h</p>
                  </div>
                  <label className="flex items-center gap-2 cursor-pointer select-none">
                    <input type="checkbox" checked={done.has(step.id)} onChange={(e) => { setDone(prev => { const n = new Set(prev); if (e.target.checked) n.add(step.id); else n.delete(step.id); return n; }); }} />
                    <span className="body-small">Mark done</span>
                  </label>
                </div>
              </div>
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
}

// Community Page - simple chat with local storage
export function Community() {
  const [channel, setChannel] = useState(mock.channels[0].name);
  const storageKey = (c) => `chat:${c}`;
  const [messages, setMessages] = useState(() => { const init = mock.initialMessages[channel] || []; return ls.get(storageKey(channel), init); });
  const [text, setText] = useState("");
  const listRef = useRef(null);

  useEffect(() => { const init = mock.initialMessages[channel] || []; setMessages(ls.get(storageKey(channel), init)); }, [channel]);
  useEffect(() => { ls.set(storageKey(channel), messages); }, [messages, channel]);
  useEffect(() => { listRef.current?.scrollTo({ top: 999999, behavior: "smooth" }); }, [messages]);

  const send = () => { const val = text.trim(); if (!val) return; setMessages((m) => [...m, { id: crypto.randomUUID(), author: "You", text: val, ts: Date.now() }]); setText(""); };

  return (
    <div className="dark-full-container" style={{ background: "var(--bg-primary)" }}>
      <div className="dark-content-container pad-large">
        <div className="grid grid-cols-12 gap-6" style={{ minHeight: 520 }}>
          <aside className="col-span-12 md:col-span-3">
            <div className="glass-card p-4">
              <h3 className="heading-2 mb-3">Channels</h3>
              <ul className="space-y-2">
                {mock.channels.map((c) => (
                  <li key={c.id}>
                    <button className={`w-full text-left px-3 py-2 dark-transition ${channel === c.name ? "bg-white/10 text-white" : "text-white/70 hover:bg-white/5"}`} onClick={() => setChannel(c.name)} aria-pressed={channel === c.name}>{c.name}</button>
                  </li>
                ))}
              </ul>
            </div>
          </aside>

          <section className="col-span-12 md:col-span-9">
            <div className="glass-card flex flex-col h-full">
              <div className="border-b border-white/10 p-4">
                <h2 className="heading-2">{channel}</h2>
                <p className="body-muted">Public chat (mocked)</p>
              </div>
              <ScrollArea className="flex-1 p-4" ref={listRef}>
                <div className="space-y-3 pr-2">
                  {messages.map(m => (
                    <div key={m.id}>
                      <div className="text-sm text-white/60">{new Date(m.ts).toLocaleTimeString()} • {m.author}</div>
                      <div className="mt-1 bg-white/5 px-3 py-2 inline-block rounded">{m.text}</div>
                    </div>
                  ))}
                </div>
              </ScrollArea>
              <div className="p-4 border-t border-white/10 flex items-center gap-2">
                <Textarea value={text} onChange={(e) => setText(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); } }} placeholder="Write a message" className="bg-[#121212] text-white border-border h-24" />
                <button className="btn-primary" onClick={send} aria-label="Send"><Send size={18} /></button>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}