"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  CheckCircle2, MapPin, Clock, ArrowRight, Zap, Image as ImageIcon, 
  X, Briefcase, Star, AlertCircle, ChevronRight, Navigation, LayoutDashboard, History, Settings, User
} from "lucide-react";
import { api } from "@/lib/api";

export default function ProviderDashboard() {
  const [activeTab, setActiveTab] = useState<'requests' | 'active'>('requests');
  const [allRequests, setAllRequests] = useState<any[]>([]);
  const [selectedRequest, setSelectedRequest] = useState<any | null>(null);
  const [isAvailable, setIsAvailable] = useState(true);

  // Poll for requests
  useEffect(() => {
    let interval = setInterval(async () => {
      try {
        const reqs = await api.listRequests();
        setAllRequests(reqs);
      } catch (e) {
        // ignore
      }
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  const pendingRequests = allRequests.filter(r => r.status === 'pending');
  const activeJobs = allRequests.filter(r => r.status !== 'pending' && r.status !== 'declined');

  // Actions
  const handleAccept = async (req: any) => {
    try {
      await api.updateRequestStatus(req.id, "accepted");
      setSelectedRequest(null);
      setActiveTab('active');
    } catch (e) {
      alert("Failed to accept");
    }
  };

  const handleDecline = async (req: any) => {
    try {
      await api.updateRequestStatus(req.id, "declined");
      setSelectedRequest(null);
    } catch (e) {
      alert("Failed to decline");
    }
  };

  const advanceJobStatus = async (job: any) => {
    const statuses = ['accepted', 'scheduled', 'on the way', 'in progress', 'completed'];
    const currentIndex = statuses.indexOf(job.status.toLowerCase());
    if (currentIndex < statuses.length - 1) {
      const nextStatus = statuses[currentIndex + 1];
      try {
        await api.updateRequestStatus(job.id, nextStatus);
      } catch (e) {
        alert("Failed to update status");
      }
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground font-sans flex flex-col md:flex-row selection:bg-primary selection:text-white overflow-hidden">
      
      {/* 1. Sidebar Navigation */}
      <aside className="hidden md:flex w-64 bg-surface border-r border-border flex-col justify-between sticky top-0 h-screen">
        <div>
          <div className="px-8 py-8">
            <div className="font-black text-2xl tracking-tighter flex items-center gap-2 text-ink">
              <div className="w-5 h-5 bg-primary rounded-sm" />
              <span>FixFind <span className="text-primary">Pro</span></span>
            </div>
          </div>
          <nav className="px-4 space-y-2 font-bold text-sm">
            <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl bg-primary-tint text-primary border border-primary/20">
              <Briefcase className="w-5 h-5" /> Workspace
            </button>
            <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-ink-soft hover:text-ink hover:bg-background transition-colors">
              <LayoutDashboard className="w-5 h-5" /> Overview
            </button>
            <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-ink-soft hover:text-ink hover:bg-background transition-colors">
              <History className="w-5 h-5" /> History
            </button>
            <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-ink-soft hover:text-ink hover:bg-background transition-colors">
              <User className="w-5 h-5" /> Profile
            </button>
          </nav>
        </div>
        <div className="p-4 border-t border-border">
          <div className="bg-background border border-border p-4 rounded-2xl">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-10 h-10 bg-accent/20 rounded-full flex items-center justify-center text-accent font-black">CC</div>
              <div>
                <div className="text-sm font-black text-ink">CoolCare</div>
                <div className="text-xs font-bold text-ink-mute flex items-center gap-1"><Star className="w-3 h-3 text-accent fill-accent"/> 4.7 (128)</div>
              </div>
            </div>
            <button 
              onClick={() => setIsAvailable(!isAvailable)}
              className={`w-full py-2 rounded-lg text-xs font-black uppercase tracking-widest flex items-center justify-center gap-2 transition-colors ${isAvailable ? 'bg-ok/10 text-ok border border-ok/20' : 'bg-ink-mute/10 text-ink-mute border border-border'}`}
            >
              <div className={`w-2 h-2 rounded-full ${isAvailable ? 'bg-ok' : 'bg-ink-mute'}`} />
              {isAvailable ? 'Available' : 'Away'}
            </button>
          </div>
        </div>
      </aside>

      {/* 2. Main Workspace */}
      <main className="flex-1 h-screen overflow-y-auto relative bg-background">
        
        {/* Mobile Header */}
        <header className="md:hidden bg-surface border-b border-border p-4 flex items-center justify-between sticky top-0 z-40">
           <div className="font-black text-xl tracking-tighter flex items-center gap-2 text-ink">
             <div className="w-4 h-4 bg-primary rounded-sm" />
             <span>FixFind Pro</span>
           </div>
           <div className="flex items-center gap-3">
             <div className={`w-2 h-2 rounded-full ${isAvailable ? 'bg-ok' : 'bg-ink-mute'}`} />
             <div className="w-8 h-8 bg-accent/20 rounded-full flex items-center justify-center text-accent font-black text-xs">CC</div>
           </div>
        </header>

        <div className="max-w-5xl mx-auto p-6 md:p-12 space-y-12 pb-32">
          
          <section>
            <h1 className="text-4xl md:text-5xl font-black uppercase tracking-tighter text-ink mb-4">
              Good evening, CoolCare 👋
            </h1>
            <p className="text-xl text-ink-soft font-bold max-w-2xl">
              Review customer problems, understand what FixFind identified, and choose the jobs that fit your expertise.
            </p>
          </section>

          <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-surface border border-border p-5 rounded-2xl shadow-sm">
              <div className="text-3xl font-black text-ink">{pendingRequests.length}</div>
              <div className="text-xs font-black uppercase tracking-widest text-primary mt-1">New Requests</div>
            </div>
            <div className="bg-surface border border-border p-5 rounded-2xl shadow-sm">
              <div className="text-3xl font-black text-ink">{activeJobs.length}</div>
              <div className="text-xs font-black uppercase tracking-widest text-ink-mute mt-1">Active Jobs</div>
            </div>
            <div className="bg-surface border border-border p-5 rounded-2xl shadow-sm">
              <div className="text-3xl font-black text-ink">128</div>
              <div className="text-xs font-black uppercase tracking-widest text-ink-mute mt-1">Completed</div>
            </div>
            <div className="bg-surface border border-border p-5 rounded-2xl shadow-sm">
              <div className="text-3xl font-black text-ink flex items-center gap-1">4.7 <Star className="w-5 h-5 text-accent fill-accent"/></div>
              <div className="text-xs font-black uppercase tracking-widest text-ink-mute mt-1">Rating</div>
            </div>
          </section>

          <div className="flex border-b border-border gap-8">
            <button 
              onClick={() => setActiveTab('requests')}
              className={`pb-4 text-sm font-black uppercase tracking-widest transition-colors relative ${activeTab === 'requests' ? 'text-primary' : 'text-ink-mute hover:text-ink'}`}
            >
              New Requests ({pendingRequests.length})
              {activeTab === 'requests' && <motion.div layoutId="tab-indicator" className="absolute bottom-[-1px] left-0 right-0 h-0.5 bg-primary" />}
            </button>
            <button 
              onClick={() => setActiveTab('active')}
              className={`pb-4 text-sm font-black uppercase tracking-widest transition-colors relative ${activeTab === 'active' ? 'text-primary' : 'text-ink-mute hover:text-ink'}`}
            >
              Active Jobs ({activeJobs.length})
              {activeTab === 'active' && <motion.div layoutId="tab-indicator" className="absolute bottom-[-1px] left-0 right-0 h-0.5 bg-primary" />}
            </button>
          </div>

          <AnimatePresence mode="wait">
            
            {/* NEW REQUESTS TAB */}
            {activeTab === 'requests' && (
              <motion.section 
                key="requests"
                initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}
                className="space-y-6"
              >
                {pendingRequests.length === 0 ? (
                  <div className="text-center py-20 bg-surface border border-border border-dashed rounded-3xl">
                    <CheckCircle2 className="w-12 h-12 text-ink-mute mx-auto mb-4" />
                    <h3 className="text-xl font-black text-ink">You're all caught up!</h3>
                    <p className="text-ink-soft font-bold mt-2">We'll notify you when nearby problems match your expertise.</p>
                  </div>
                ) : (
                  pendingRequests.map(req => (
                    <motion.div 
                      layout
                      initial={{ opacity: 0, scale: 0.98 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.95 }}
                      key={req.id} 
                      className="bg-surface border-2 border-border rounded-3xl p-6 md:p-8 shadow-sm hover:shadow-lg transition-shadow"
                    >
                      
                      <div className="flex flex-col md:flex-row gap-8 mb-8 pb-8 border-b border-border">
                        <div className="flex-1">
                          <div className="text-xs font-black text-ink-mute uppercase tracking-widest mb-3">Customer Problem</div>
                          <h2 className="text-2xl font-black text-ink leading-snug">"{req.problem?.issue_summary || "Unknown Issue"}"</h2>
                          
                          <div className="flex flex-wrap gap-4 mt-6">
                            <span className="flex items-center gap-1.5 text-sm font-bold text-ink-soft bg-background px-3 py-1.5 rounded-lg border border-border">
                              <MapPin className="w-4 h-4 text-primary" /> Hyderabad
                            </span>
                          </div>
                        </div>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-[1fr_250px] gap-8">
                        <div className="bg-primary-tint border border-primary/20 p-6 rounded-2xl space-y-4">
                          <div className="flex items-center gap-2 mb-2">
                            <Zap className="w-4 h-4 text-primary" />
                            <h4 className="text-xs font-black text-primary uppercase tracking-widest">FixFind Understanding</h4>
                          </div>
                          <div className="grid grid-cols-2 gap-y-4 gap-x-2 text-sm">
                            <div><span className="text-ink-soft font-bold block">Asset</span><span className="font-black text-ink">{req.problem?.object}</span></div>
                            <div><span className="text-ink-soft font-bold block">Issue</span><span className="font-black text-ink">{req.problem?.issue_summary}</span></div>
                            <div><span className="text-ink-soft font-bold block">Service</span><span className="font-black text-primary">{req.service?.service}</span></div>
                            <div><span className="text-ink-soft font-bold block">Urgency</span><span className="font-black text-warn">{req.problem?.urgency_level}</span></div>
                          </div>
                        </div>
                      </div>

                      <div className="mt-8 flex flex-col sm:flex-row items-center gap-4">
                        <button 
                          onClick={() => handleAccept(req)}
                          className="w-full sm:w-auto flex-1 bg-primary text-white py-4 px-8 rounded-xl font-black text-lg hover:bg-primary-hover transition-colors shadow-lg shadow-primary/20 flex items-center justify-center gap-2"
                        >
                          ACCEPT JOB <CheckCircle2 className="w-5 h-5" />
                        </button>
                        <button 
                          onClick={() => handleDecline(req)}
                          className="w-full sm:w-auto text-ink-mute hover:text-danger font-bold text-sm py-4 px-6 transition-colors"
                        >
                          Decline
                        </button>
                      </div>

                    </motion.div>
                  ))
                )}
              </motion.section>
            )}

            {/* ACTIVE JOBS TAB */}
            {activeTab === 'active' && (
              <motion.section 
                key="active"
                initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}
                className="space-y-6"
              >
                {activeJobs.length === 0 ? (
                  <div className="text-center py-20 bg-surface border border-border border-dashed rounded-3xl">
                    <Briefcase className="w-12 h-12 text-ink-mute mx-auto mb-4" />
                    <h3 className="text-xl font-black text-ink">No active jobs</h3>
                    <p className="text-ink-soft font-bold mt-2">Accept a new request to start working.</p>
                  </div>
                ) : (
                  activeJobs.map(job => (
                    <motion.div 
                      layout
                      initial={{ opacity: 0, scale: 0.98 }} animate={{ opacity: 1, scale: 1 }}
                      key={job.id} 
                      className="bg-surface border-2 border-border rounded-3xl p-6 md:p-8 shadow-sm"
                    >
                      <div className="flex flex-col md:flex-row gap-8">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-4">
                            <span className="bg-ok/10 text-ok px-3 py-1 rounded-lg text-xs font-black uppercase tracking-widest border border-ok/20">
                              {job.status}
                            </span>
                            <span className="text-sm font-bold text-ink-mute">Hyderabad</span>
                          </div>
                          <h2 className="text-2xl font-black text-ink mb-2">{job.service?.service}</h2>
                          <p className="text-ink-soft font-bold">"{job.problem?.issue_summary}"</p>
                          
                          <div className="mt-8 flex gap-4">
                            <button 
                              onClick={() => advanceJobStatus(job)}
                              disabled={job.status === 'completed'}
                              className="bg-ink text-white px-6 py-3 rounded-xl font-bold text-sm hover:bg-black transition-colors disabled:opacity-50 shadow-md"
                            >
                              {job.status === 'completed' ? 'Finished' : 'Advance Status'}
                            </button>
                          </div>
                        </div>

                        <div className="w-full md:w-64 bg-background border border-border p-6 rounded-2xl">
                          <h4 className="text-xs font-black text-ink-mute uppercase tracking-widest mb-4">Job Journey</h4>
                          <div className="space-y-4 relative border-l-2 border-border/50 ml-2">
                            {['accepted', 'scheduled', 'on the way', 'in progress', 'completed'].map((s, i, arr) => {
                               const isActive = job.status.toLowerCase() === s;
                               const isPast = arr.indexOf(job.status.toLowerCase()) > i;
                               return (
                                 <div key={s} className="relative pl-6">
                                   <div className={`absolute -left-[9px] top-1 w-4 h-4 rounded-full border-2 ${isActive ? 'bg-primary border-primary shadow-[0_0_10px_rgba(15,118,110,0.5)]' : isPast ? 'bg-ok border-ok' : 'bg-background border-border'}`} />
                                   <div className={`text-sm font-bold ${isActive ? 'text-primary font-black' : isPast ? 'text-ink' : 'text-ink-mute'} capitalize`}>
                                     {s}
                                   </div>
                                 </div>
                               );
                            })}
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  ))
                )}
              </motion.section>
            )}

          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}
