"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Mic, Camera, MapPin, ArrowRight, X, Image as ImageIcon, 
  Zap, CheckCircle2, ChevronRight, Star, AlertCircle, Wrench, Clock, Navigation
} from "lucide-react";

type FlowState = 
  | 'INPUT' 
  | 'ANALYZING' 
  | 'UNDERSTANDING' 
  | 'SERVICE_CONFIRMATION' 
  | 'DISCOVERY' 
  | 'MATCH_RESULTS' 
  | 'PROVIDER_DETAIL' 
  | 'REQUEST' 
  | 'TRACKING';

export default function CustomerDashboard() {
  const [flowState, setFlowState] = useState<FlowState>('INPUT');
  const [problemText, setProblemText] = useState("");
  const [hasImage, setHasImage] = useState(false);
  const [hasLocation, setHasLocation] = useState(true);
  
  // Navigation
  const Header = () => (
    <header className="w-full px-8 py-6 flex items-center justify-between border-b border-border bg-surface sticky top-0 z-50">
      <div className="font-black text-2xl tracking-tighter flex items-center gap-2 text-ink">
        <div className="w-4 h-4 bg-primary rounded-sm" />
        <span>FixFind</span>
      </div>
      <nav className="hidden md:flex gap-8 text-sm font-bold text-ink-soft">
        <button onClick={() => setFlowState('INPUT')} className="text-primary transition-colors">Solve a Problem</button>
        <button className="hover:text-primary transition-colors">My Fixes</button>
        <button className="hover:text-primary transition-colors">Messages</button>
        <button className="hover:text-primary transition-colors">Saved Providers</button>
        <button className="hover:text-primary transition-colors">Profile</button>
      </nav>
      <div className="w-10 h-10 bg-primary-tint rounded-full border border-primary/20 flex items-center justify-center text-primary font-bold">
        JD
      </div>
    </header>
  );

  // Transition handler for async flows
  const transitionTo = (newState: FlowState, delayMs: number = 0) => {
    if (delayMs > 0) {
      setTimeout(() => setFlowState(newState), delayMs);
    } else {
      setFlowState(newState);
    }
  };

  return (
    <main className="min-h-screen bg-background text-foreground font-sans selection:bg-primary selection:text-white pb-32">
      <Header />
      
      <div className="max-w-4xl mx-auto px-6 pt-16">
        <AnimatePresence mode="wait">
          
          {/* 1. INPUT STATE */}
          {flowState === 'INPUT' && (
            <motion.div 
              key="input"
              initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20, filter: "blur(10px)" }}
              className="space-y-8"
            >
              <div className="text-center space-y-4">
                <h1 className="text-5xl font-black uppercase tracking-tighter text-ink">What needs fixing?</h1>
                <p className="text-xl text-ink-soft font-bold">Describe the problem. Show us a photo. Or just tell us what's happening.</p>
              </div>

              <div className="bg-surface border-2 border-border rounded-3xl shadow-xl overflow-hidden focus-within:border-primary/50 transition-colors duration-500 relative">
                
                {/* Image Attachment Preview */}
                <AnimatePresence>
                  {hasImage && (
                    <motion.div 
                      initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }}
                      className="px-8 pt-8 pb-4"
                    >
                      <div className="relative w-32 h-32 bg-background border border-border rounded-xl overflow-hidden group">
                         <div className="absolute inset-0 bg-ink/10 flex items-center justify-center">
                           <ImageIcon className="w-8 h-8 text-ink-mute" />
                         </div>
                         <button onClick={() => setHasImage(false)} className="absolute top-2 right-2 bg-surface p-1 rounded-full shadow hover:bg-danger/10 hover:text-danger opacity-0 group-hover:opacity-100 transition-all">
                           <X className="w-4 h-4" />
                         </button>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>

                <textarea 
                  value={problemText}
                  onChange={(e) => setProblemText(e.target.value)}
                  placeholder="e.g., My AC is leaking water from the indoor unit..."
                  className="w-full bg-transparent p-8 min-h-[180px] outline-none text-2xl resize-none placeholder:text-ink-mute text-ink font-medium leading-relaxed"
                />
                
                <div className="bg-background border-t border-border p-4 flex items-center justify-between">
                  <div className="flex gap-2">
                    <button onClick={() => setHasImage(true)} className="p-3 hover:bg-surface rounded-xl transition-colors text-ink-mute hover:text-primary border border-transparent hover:border-border font-bold text-sm flex items-center gap-2">
                      <Camera className="w-5 h-5"/> <span className="hidden sm:inline">Add photo</span>
                    </button>
                    <button className="p-3 hover:bg-surface rounded-xl transition-colors text-ink-mute hover:text-primary border border-transparent hover:border-border font-bold text-sm flex items-center gap-2">
                      <Mic className="w-5 h-5"/> <span className="hidden sm:inline">Speak</span>
                    </button>
                    <button className="p-3 hover:bg-surface rounded-xl transition-colors text-primary border border-primary/20 bg-primary-tint font-bold text-sm flex items-center gap-2">
                      <MapPin className="w-5 h-5"/> <span className="hidden sm:inline">Hyderabad</span>
                    </button>
                  </div>
                  <button 
                    onClick={() => {
                      setFlowState('ANALYZING');
                      transitionTo('UNDERSTANDING', 2500);
                    }}
                    disabled={!problemText.trim() && !hasImage}
                    className="bg-primary text-white px-8 py-4 rounded-xl font-black text-sm hover:bg-primary-hover transition-colors flex items-center gap-2 shadow-md disabled:opacity-50"
                  >
                    ANALYZE PROBLEM <ArrowRight className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </motion.div>
          )}

          {/* 2. ANALYZING STATE */}
          {flowState === 'ANALYZING' && (
            <motion.div 
              key="analyzing"
              initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 1.05 }}
              className="flex flex-col items-center justify-center min-h-[400px] space-y-8"
            >
               <div className="relative">
                 <div className="w-24 h-24 border-4 border-border rounded-full" />
                 <div className="w-24 h-24 border-4 border-primary border-t-transparent rounded-full animate-spin absolute inset-0" />
                 <div className="absolute inset-0 flex items-center justify-center">
                   <Zap className="w-8 h-8 text-primary animate-pulse" />
                 </div>
               </div>
               <div className="text-center">
                 <h2 className="text-3xl font-black text-ink mb-2">Analyzing Problem</h2>
                 <p className="text-ink-soft font-bold">FixFind is parsing text and visual evidence...</p>
               </div>
            </motion.div>
          )}

          {/* 3. UNDERSTANDING STATE */}
          {flowState === 'UNDERSTANDING' && (
            <motion.div 
              key="understanding"
              initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}
              className="space-y-8"
            >
              <div className="text-center mb-12">
                <h1 className="text-5xl font-black uppercase tracking-tighter text-ink mb-4">We think we know what's wrong.</h1>
                <p className="text-xl text-ink-soft font-bold">Review the diagnosis below.</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-[1fr_300px] gap-8">
                
                {/* Left: Diagnosis */}
                <div className="bg-surface border border-border p-8 rounded-3xl shadow-sm space-y-8">
                  <div>
                    <h4 className="text-xs font-black text-ink-mute uppercase tracking-widest mb-2">Detected Problem</h4>
                    <p className="text-3xl font-black text-ink">AC water leakage</p>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-y-6 gap-x-4">
                    <div>
                      <span className="text-sm font-bold text-ink-soft block mb-1">Object</span>
                      <span className="text-lg font-black text-ink">Air Conditioner</span>
                    </div>
                    <div>
                      <span className="text-sm font-bold text-ink-soft block mb-1">Issue</span>
                      <span className="text-lg font-black text-ink">Water leakage</span>
                    </div>
                    <div>
                      <span className="text-sm font-bold text-ink-soft block mb-1">Likely service</span>
                      <span className="text-lg font-black text-primary">AC Repair</span>
                    </div>
                    <div>
                      <span className="text-sm font-bold text-ink-soft block mb-1">Specialization</span>
                      <span className="text-lg font-black text-ink">Drainage</span>
                    </div>
                    <div>
                      <span className="text-sm font-bold text-ink-soft block mb-1">Urgency</span>
                      <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-warn/10 text-warn rounded-lg font-bold text-sm">
                        <AlertCircle className="w-4 h-4" /> Moderate
                      </span>
                    </div>
                  </div>
                </div>

                {/* Right: Confidence & Evidence */}
                <div className="space-y-6">
                  {/* Confidence */}
                  <div className="bg-surface border border-border p-6 rounded-3xl shadow-sm text-center">
                    <h4 className="text-xs font-black text-ink-mute uppercase tracking-widest mb-4">Understanding</h4>
                    <div className="text-5xl font-black text-ok mb-2">91%</div>
                    <p className="text-sm font-bold text-ok flex items-center justify-center gap-1.5"><CheckCircle2 className="w-4 h-4"/> High confidence</p>
                    
                    <button className="mt-6 text-sm font-bold text-ink-mute hover:text-ink transition-colors underline decoration-border underline-offset-4">
                      That's not my problem
                    </button>
                  </div>

                  {/* Evidence */}
                  {(hasImage || problemText) && (
                    <div className="bg-primary-tint border border-primary/20 p-6 rounded-3xl shadow-sm">
                      <h4 className="text-xs font-black text-primary uppercase tracking-widest mb-4">What we noticed</h4>
                      <ul className="space-y-3">
                        <li className="flex gap-2 text-sm font-bold text-ink">
                           <CheckCircle2 className="w-5 h-5 text-primary shrink-0" /> Indoor AC unit detected
                        </li>
                        <li className="flex gap-2 text-sm font-bold text-ink">
                           <CheckCircle2 className="w-5 h-5 text-primary shrink-0" /> Leakage appears near lower section
                        </li>
                      </ul>
                    </div>
                  )}
                </div>
              </div>

              <div className="flex justify-end pt-8">
                <button onClick={() => setFlowState('SERVICE_CONFIRMATION')} className="bg-primary text-white px-10 py-5 rounded-2xl font-black text-lg hover:bg-primary-hover transition-colors flex items-center gap-3 shadow-xl shadow-primary/20">
                  CONFIRM DIAGNOSIS <ArrowRight className="w-6 h-6" />
                </button>
              </div>
            </motion.div>
          )}

          {/* 4. SERVICE CONFIRMATION */}
          {flowState === 'SERVICE_CONFIRMATION' && (
            <motion.div 
              key="service_conf"
              initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}
              className="max-w-2xl mx-auto text-center space-y-12"
            >
               <div>
                 <h1 className="text-5xl font-black uppercase tracking-tighter text-ink mb-4">We've identified the service you need.</h1>
               </div>

               <div className="bg-surface border-2 border-border p-10 rounded-[3rem] shadow-xl text-left relative overflow-hidden">
                 <div className="absolute top-0 right-0 p-8 opacity-5">
                   <Wrench className="w-40 h-40" />
                 </div>
                 <div className="relative z-10">
                   <h2 className="text-4xl font-black text-primary mb-8">AC Repair</h2>
                   
                   <div className="space-y-4 text-lg">
                     <div className="flex border-b border-border pb-4">
                       <span className="w-1/3 text-ink-soft font-bold">Issue</span>
                       <span className="w-2/3 font-black text-ink">Water leakage</span>
                     </div>
                     <div className="flex border-b border-border pb-4">
                       <span className="w-1/3 text-ink-soft font-bold">Specialization</span>
                       <span className="w-2/3 font-black text-ink">Drainage / Leakage</span>
                     </div>
                     <div className="flex border-b border-border pb-4">
                       <span className="w-1/3 text-ink-soft font-bold">Location</span>
                       <span className="w-2/3 font-black text-ink flex items-center gap-2"><MapPin className="w-5 h-5 text-primary"/> Hyderabad</span>
                     </div>
                     <div className="flex pt-2">
                       <span className="w-1/3 text-ink-soft font-bold">Preferred time</span>
                       <span className="w-2/3 font-black text-ink flex items-center gap-2"><Clock className="w-5 h-5 text-primary"/> Today</span>
                     </div>
                   </div>
                 </div>
               </div>

               <button 
                 onClick={() => {
                   setFlowState('DISCOVERY');
                   transitionTo('MATCH_RESULTS', 3000);
                 }} 
                 className="w-full bg-ink text-white px-10 py-6 rounded-2xl font-black text-xl hover:bg-black transition-colors flex items-center justify-center gap-3 shadow-xl"
               >
                 FIND AVAILABLE PROFESSIONALS <ArrowRight className="w-6 h-6" />
               </button>
            </motion.div>
          )}

          {/* 5. DISCOVERY (LOADING) */}
          {flowState === 'DISCOVERY' && (
            <motion.div 
              key="discovery"
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="max-w-xl mx-auto space-y-12"
            >
              <div className="text-center">
                 <h1 className="text-4xl font-black uppercase tracking-tighter text-ink mb-4">Finding someone who can actually fix this.</h1>
                 <p className="text-lg text-ink-soft font-bold">Hold tight while FixFind analyzes the local provider network.</p>
              </div>

              <div className="bg-surface border border-border rounded-3xl p-8 shadow-sm space-y-6 font-mono font-bold text-sm">
                 <motion.div initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.2 }} className="flex justify-between items-center text-ink">
                   <span>UNDERSTANDING PROBLEM</span> <CheckCircle2 className="w-5 h-5 text-ok" />
                 </motion.div>
                 <motion.div initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.8 }} className="flex justify-between items-center text-ink">
                   <span>MATCHING SPECIALISTS</span> <CheckCircle2 className="w-5 h-5 text-ok" />
                 </motion.div>
                 <motion.div initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 1.4 }} className="flex justify-between items-center text-ink">
                   <span>CHECKING AVAILABILITY</span> <CheckCircle2 className="w-5 h-5 text-ok" />
                 </motion.div>
                 <motion.div initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 2.0 }} className="flex justify-between items-center text-ink">
                   <span>CHECKING DISTANCE</span> <CheckCircle2 className="w-5 h-5 text-ok" />
                 </motion.div>
                 <motion.div initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 2.6 }} className="flex justify-between items-center text-primary">
                   <span>BUILDING YOUR MATCHES...</span> <Loader2 className="w-5 h-5 animate-spin" />
                 </motion.div>
              </div>
            </motion.div>
          )}

          {/* 6. MATCH RESULTS */}
          {flowState === 'MATCH_RESULTS' && (
            <motion.div 
              key="match_results"
              initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}
              className="space-y-8"
            >
               <div className="flex items-end justify-between border-b border-border pb-6">
                 <div>
                   <h1 className="text-5xl font-black uppercase tracking-tighter text-ink mb-2">4 professionals match your problem</h1>
                   <p className="text-xl text-ink-soft font-bold">Ranked deterministically by Service Fit Score.</p>
                 </div>
               </div>

               {/* Result Card */}
               <motion.div 
                 onClick={() => setFlowState('PROVIDER_DETAIL')}
                 whileHover={{ scale: 1.01 }}
                 className="bg-surface border-2 border-border rounded-3xl p-8 cursor-pointer shadow-sm hover:shadow-xl hover:border-primary/50 transition-all group"
               >
                 <div className="flex flex-col md:flex-row gap-8">
                   
                   {/* Fit Score Badge */}
                   <div className="shrink-0 flex flex-col items-center justify-center w-32 h-32 rounded-full border-8 border-primary bg-background">
                     <span className="text-3xl font-black text-ink">95%</span>
                     <span className="text-[10px] font-black tracking-widest text-primary uppercase mt-1">MATCH</span>
                   </div>

                   <div className="flex-1 space-y-4">
                     <div className="flex justify-between items-start">
                       <div>
                         <h2 className="text-3xl font-black text-ink flex items-center gap-3">
                           CoolCare Services
                           <span className="bg-ok/10 text-ok text-xs px-2 py-1 rounded font-bold flex items-center gap-1 uppercase tracking-widest"><CheckCircle2 className="w-3 h-3"/> Verified</span>
                         </h2>
                         <p className="text-lg font-bold text-primary mt-1">AC Repair · Water Leakage</p>
                       </div>
                       <div className="text-right">
                         <div className="text-xl font-black text-ink">₹400–₹700</div>
                         <div className="text-sm font-bold text-ink-mute">Est. price</div>
                       </div>
                     </div>

                     <div className="flex gap-4">
                       <span className="bg-background px-4 py-2 rounded-xl border border-border font-bold text-sm text-ink-soft flex items-center gap-2">
                         <MapPin className="w-4 h-4 text-ink"/> 2.1 km
                       </span>
                       <span className="bg-background px-4 py-2 rounded-xl border border-border font-bold text-sm text-ink-soft flex items-center gap-2">
                         <Star className="w-4 h-4 text-accent fill-accent"/> 4.7 (120+)
                       </span>
                       <span className="bg-background px-4 py-2 rounded-xl border border-border font-bold text-sm text-ink-soft flex items-center gap-2">
                         <Clock className="w-4 h-4 text-ok"/> Available Today
                       </span>
                     </div>

                     <div className="bg-primary-tint border border-primary/20 p-4 rounded-xl mt-4">
                       <h4 className="text-xs font-black text-primary uppercase tracking-widest mb-1">Why FixFind matched them</h4>
                       <p className="text-sm font-bold text-ink">Strong match for your specific issue (AC Drainage) and available near your location today.</p>
                     </div>
                   </div>

                   <div className="flex items-center shrink-0">
                     <div className="w-12 h-12 rounded-full bg-background border border-border flex items-center justify-center group-hover:bg-primary group-hover:text-white transition-colors text-ink">
                       <ChevronRight className="w-6 h-6" />
                     </div>
                   </div>
                 </div>
               </motion.div>
               
               {/* Faded mockup of second result */}
               <div className="bg-surface/50 border border-border rounded-3xl p-8 opacity-60 grayscale pointer-events-none">
                 <div className="flex gap-8">
                   <div className="shrink-0 flex flex-col items-center justify-center w-24 h-24 rounded-full border-4 border-ink-mute bg-background">
                     <span className="text-xl font-black text-ink">82%</span>
                   </div>
                   <div>
                     <h2 className="text-2xl font-black text-ink">Swift AC Techs</h2>
                     <p className="font-bold text-ink-soft">AC Repair</p>
                   </div>
                 </div>
               </div>

            </motion.div>
          )}

          {/* 7. PROVIDER DETAIL */}
          {flowState === 'PROVIDER_DETAIL' && (
            <motion.div 
              key="provider_detail"
              initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 1.05 }}
              className="max-w-3xl mx-auto"
            >
               <button onClick={() => setFlowState('MATCH_RESULTS')} className="text-sm font-bold text-ink-mute hover:text-ink mb-8 flex items-center gap-2 transition-colors">
                 <ArrowRight className="w-4 h-4 rotate-180" /> Back to matches
               </button>

               <div className="bg-surface border-2 border-border rounded-[2rem] shadow-xl overflow-hidden">
                 
                 {/* Match header */}
                 <div className="bg-primary p-8 text-white flex justify-between items-center">
                   <div>
                     <div className="text-sm font-bold uppercase tracking-widest text-primary-tint mb-1">Your Match</div>
                     <div className="text-4xl font-black">95% fit for this problem</div>
                   </div>
                   <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center text-primary font-black text-2xl shadow-xl">
                     95%
                   </div>
                 </div>

                 <div className="p-10 space-y-12">
                   
                   <div className="flex justify-between items-start">
                     <div>
                       <h1 className="text-4xl font-black text-ink mb-2">CoolCare Services</h1>
                       <p className="text-lg font-bold text-ink-soft">Specialized in AC drainage and water-leakage issues.</p>
                     </div>
                     <div className="text-right">
                       <div className="text-3xl font-black text-ink">₹400–₹700</div>
                       <div className="text-sm font-bold text-ink-mute">Estimated cost</div>
                     </div>
                   </div>

                   <div className="grid grid-cols-2 gap-8">
                     <div>
                       <h3 className="text-sm font-black text-ink-mute uppercase tracking-widest mb-4">Capabilities</h3>
                       <ul className="space-y-2 font-bold text-ink">
                         <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-primary" /> AC Repair</li>
                         <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-primary" /> Water Leakage</li>
                         <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-primary" /> Drainage</li>
                         <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-primary" /> Cooling Issues</li>
                       </ul>
                     </div>
                     
                     <div className="space-y-8">
                       <div>
                         <h3 className="text-sm font-black text-ink-mute uppercase tracking-widest mb-4">Availability</h3>
                         <div className="bg-ok/10 text-ok px-4 py-3 rounded-xl font-bold flex items-center gap-2">
                           <Clock className="w-5 h-5" /> Available Today
                         </div>
                       </div>
                       <div>
                         <h3 className="text-sm font-black text-ink-mute uppercase tracking-widest mb-4">Location</h3>
                         <div className="bg-background border border-border px-4 py-3 rounded-xl font-bold text-ink flex items-center justify-between">
                           <div className="flex items-center gap-2"><MapPin className="w-5 h-5 text-primary" /> 2.1 km away</div>
                           <button className="text-primary hover:underline text-sm">View map</button>
                         </div>
                       </div>
                     </div>
                   </div>

                   <div className="pt-8 border-t border-border">
                     <button onClick={() => setFlowState('REQUEST')} className="w-full bg-ink text-white py-5 rounded-2xl font-black text-xl hover:bg-black transition-colors flex items-center justify-center gap-3 shadow-xl">
                       REQUEST SERVICE <ArrowRight className="w-6 h-6" />
                     </button>
                   </div>

                 </div>
               </div>
            </motion.div>
          )}

          {/* 8. SERVICE REQUEST */}
          {flowState === 'REQUEST' && (
            <motion.div 
              key="request"
              initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}
              className="max-w-xl mx-auto"
            >
               <h1 className="text-5xl font-black uppercase tracking-tighter text-ink mb-10 text-center">Request service</h1>

               <div className="bg-surface border-2 border-border p-10 rounded-[2rem] shadow-xl space-y-8">
                 
                 <div className="space-y-1">
                   <div className="text-sm font-black text-ink-mute uppercase tracking-widest">Problem</div>
                   <div className="text-2xl font-black text-ink">AC water leakage</div>
                 </div>
                 
                 <div className="space-y-1">
                   <div className="text-sm font-black text-ink-mute uppercase tracking-widest">Provider</div>
                   <div className="text-2xl font-black text-primary">CoolCare Services</div>
                 </div>
                 
                 <div className="space-y-1">
                   <div className="text-sm font-black text-ink-mute uppercase tracking-widest">Location</div>
                   <div className="text-2xl font-black text-ink">Home · Hyderabad</div>
                 </div>

                 <div className="space-y-1">
                   <div className="text-sm font-black text-ink-mute uppercase tracking-widest">Preferred slot</div>
                   <div className="text-2xl font-black text-ink bg-primary-tint border border-primary/20 p-4 rounded-xl inline-block mt-2">Today · 4:00 PM</div>
                 </div>

                 <div className="pt-8 mt-8 border-t border-border">
                   <button 
                     onClick={() => {
                       setFlowState('TRACKING');
                     }} 
                     className="w-full bg-primary text-white py-5 rounded-2xl font-black text-xl hover:bg-primary-hover transition-colors flex items-center justify-center gap-3 shadow-xl shadow-primary/20"
                   >
                     SEND SERVICE REQUEST <ArrowRight className="w-6 h-6" />
                   </button>
                 </div>
               </div>
            </motion.div>
          )}

          {/* 9. TRACKING */}
          {flowState === 'TRACKING' && (
            <motion.div 
              key="tracking"
              initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0 }}
              className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-[1fr_350px] gap-12"
            >
               {/* Left: Problem Card context */}
               <div className="space-y-8">
                 <h1 className="text-5xl font-black uppercase tracking-tighter text-ink mb-4">Fix Journey</h1>
                 
                 {/* Reusable Problem Card concept */}
                 <div className="bg-surface border-2 border-border p-8 rounded-3xl shadow-sm">
                   <div className="flex items-center gap-4 mb-6 pb-6 border-b border-border">
                     <div className="w-16 h-16 bg-primary-tint rounded-2xl flex items-center justify-center text-primary">
                       <Wrench className="w-8 h-8" />
                     </div>
                     <div>
                       <h2 className="text-2xl font-black text-ink">AC water leakage</h2>
                       <p className="text-ink-soft font-bold">CoolCare Services</p>
                     </div>
                   </div>
                   
                   <div className="bg-ok/10 border border-ok/20 p-6 rounded-2xl">
                     <h3 className="text-sm font-black text-ok uppercase tracking-widest mb-1">Current Status</h3>
                     <p className="text-xl font-black text-ink">Provider accepted</p>
                     <p className="text-sm font-bold text-ink-soft mt-2">CoolCare Services accepted your request and will arrive at 4:00 PM.</p>
                   </div>
                 </div>

                 <div className="bg-surface border border-border p-6 rounded-3xl shadow-sm flex items-center justify-between">
                   <div className="flex items-center gap-4">
                     <div className="w-12 h-12 bg-background border border-border rounded-full flex items-center justify-center text-ink">
                       <Navigation className="w-5 h-5" />
                     </div>
                     <span className="font-bold text-ink">Provider location tracking unavailable until 3:30 PM.</span>
                   </div>
                 </div>
               </div>

               {/* Right: Job Journey Timeline */}
               <div className="bg-background border border-border p-8 rounded-3xl h-fit">
                 <h3 className="text-sm font-black text-ink-mute uppercase tracking-widest mb-8">Request Timeline</h3>
                 
                 <div className="relative border-l-2 border-border ml-3 space-y-10">
                   
                   <div className="relative">
                     <div className="absolute -left-[11px] top-1 w-5 h-5 bg-ok rounded-full border-4 border-background" />
                     <div className="pl-8">
                       <div className="font-black text-ink">PROBLEM REPORTED</div>
                       <div className="text-xs font-bold text-ink-mute mt-1">10:00 AM</div>
                     </div>
                   </div>
                   
                   <div className="relative">
                     <div className="absolute -left-[11px] top-1 w-5 h-5 bg-ok rounded-full border-4 border-background" />
                     <div className="pl-8">
                       <div className="font-black text-ink">MATCH FOUND</div>
                       <div className="text-xs font-bold text-ink-mute mt-1">10:01 AM</div>
                     </div>
                   </div>

                   <div className="relative">
                     <div className="absolute -left-[11px] top-1 w-5 h-5 bg-ok rounded-full border-4 border-background" />
                     <div className="pl-8">
                       <div className="font-black text-ink">REQUEST SENT</div>
                       <div className="text-xs font-bold text-ink-mute mt-1">10:05 AM</div>
                     </div>
                   </div>

                   <div className="relative">
                     <div className="absolute -left-[11px] top-1 w-5 h-5 bg-primary rounded-full border-4 border-background shadow-[0_0_10px_rgba(15,118,110,0.5)]" />
                     <div className="pl-8">
                       <div className="font-black text-primary">PROVIDER ACCEPTED</div>
                       <div className="text-xs font-bold text-primary mt-1">10:12 AM</div>
                     </div>
                   </div>

                   <div className="relative opacity-50">
                     <div className="absolute -left-[9px] top-1 w-4 h-4 bg-transparent border-2 border-border rounded-full" />
                     <div className="pl-8">
                       <div className="font-black text-ink">ON THE WAY</div>
                     </div>
                   </div>

                   <div className="relative opacity-50">
                     <div className="absolute -left-[9px] top-1 w-4 h-4 bg-transparent border-2 border-border rounded-full" />
                     <div className="pl-8">
                       <div className="font-black text-ink">SERVICE COMPLETED</div>
                     </div>
                   </div>

                 </div>
               </div>
            </motion.div>
          )}

        </AnimatePresence>
      </div>
    </main>
  );
}
// Add Loader2 manually since it was missed in imports above to fix linter
const Loader2 = ({ className }: { className?: string }) => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
);
