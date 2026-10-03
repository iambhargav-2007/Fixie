"use client";

import { useRef, useState } from "react";
import { motion, useScroll, useTransform, AnimatePresence } from "framer-motion";
import { Search, MapPin, Mic, Camera, ShieldCheck, ArrowRight, Zap, CheckCircle2, Wrench, Briefcase, X } from "lucide-react";
import { useRouter } from "next/navigation";

// Mock Data
const mockScenarios = [
  "AC starts leaking before guests arrive.",
  "Washing machine suddenly stops spinning.",
  "Kitchen sink drainage completely blocked.",
  "Ceiling fan making a loud grinding noise."
];

const mockProviders = [
  { id: "P1", name: "CoolCare Experts", specialty: "AC Leakage & Drainage", distance: 2.1, score: 95, price: 400, time: "Today, 14:00" },
  { id: "P2", name: "Swift Plumbers", specialty: "Pipe Blockages", distance: 1.2, score: 92, price: 350, time: "Today, 15:30" }
];

export default function Home() {
  const router = useRouter();
  const containerRef = useRef(null);
  const { scrollYProgress } = useScroll({ target: containerRef, offset: ["start start", "end start"] });
  const yHero = useTransform(scrollYProgress, [0, 1], [0, 200]);
  const opacityHero = useTransform(scrollYProgress, [0, 0.5], [1, 0]);

  const [activeStep, setActiveStep] = useState(0);

  // Staggered text animation variants
  const sentence = { hidden: { opacity: 1 }, visible: { opacity: 1, transition: { delay: 0.1, staggerChildren: 0.04 } } };
  const letter = { hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0, transition: { type: "spring", damping: 12, stiffness: 200 } } };

  return (
    <main ref={containerRef} className="min-h-screen bg-background text-foreground font-sans overflow-x-hidden selection:bg-primary selection:text-white">
      
      {/* 1. Navigation */}
      <header className="fixed top-0 w-full z-50 px-8 py-6 flex items-center justify-between backdrop-blur-md bg-background/80 border-b border-border">
        <div className="font-bold text-2xl tracking-tighter flex items-center gap-2 text-ink">
          <div className="w-4 h-4 bg-primary rounded-sm" />
          <span>FixFind</span>
        </div>
        <nav className="hidden md:flex gap-8 text-sm font-bold text-ink-soft">
          <a href="#" className="hover:text-primary transition-colors">Product</a>
          <a href="#" className="hover:text-primary transition-colors">How it Works</a>
          <button onClick={() => router.push('/login')} className="hover:text-primary transition-colors cursor-pointer">For Providers</button>
        </nav>
        <button onClick={() => router.push('/login')} className="bg-primary text-white px-6 py-2 rounded-full font-bold text-sm hover:bg-primary-hover transition-colors shadow-sm">
          Login
        </button>
      </header>

      {/* 2. Hero Section */}
      <section className="relative pt-40 pb-32 px-8 max-w-7xl mx-auto min-h-screen flex flex-col justify-center">
        <motion.div style={{ y: yHero, opacity: opacityHero }} className="grid grid-cols-1 lg:grid-cols-[1fr_0.8fr] gap-12 items-center">
          
          <div className="z-10">
            <motion.h1 variants={sentence} initial="hidden" animate="visible" className="text-[5rem] lg:text-[6.5rem] font-black uppercase tracking-tighter leading-[0.85] mb-8 text-ink">
              {"DON'T SEARCH FOR A SERVICE.".split(" ").map((word, i) => (
                <span key={i} className="inline-block mr-4">
                  {word.split("").map((char, j) => (
                    <motion.span key={j} variants={letter} className="inline-block">{char}</motion.span>
                  ))}
                </span>
              ))}
              <br/>
              <span className="text-primary block mt-4">DESCRIBE THE PROBLEM.</span>
            </motion.h1>

            <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.8 }} className="text-xl text-ink-soft max-w-lg mb-10 leading-relaxed font-medium">
              Describe what's wrong using text, a photo, your voice, or your location. FixFind understands the problem and connects you with suitable nearby professionals.
            </motion.p>
            
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 1 }} className="flex gap-4">
              <button onClick={() => router.push('/login')} className="bg-primary text-white px-8 py-4 rounded-xl font-bold text-sm hover:bg-primary-hover transition-colors shadow-lg shadow-primary/20">DESCRIBE A PROBLEM</button>
              <button className="border-2 border-border text-ink px-8 py-4 rounded-xl font-bold text-sm hover:border-ink transition-colors">SEE HOW IT WORKS</button>
            </motion.div>
          </div>

          {/* Hero Visual - Product Interface Mockup */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.6, duration: 1 }}
            className="relative h-[600px] w-full bg-surface border-2 border-border shadow-2xl overflow-hidden flex flex-col rounded-[2rem]"
          >
            {/* Top Bar */}
            <div className="h-12 border-b border-border flex items-center px-4 gap-2 bg-background/50">
              <div className="w-3 h-3 rounded-full bg-red-400" />
              <div className="w-3 h-3 rounded-full bg-amber-400" />
              <div className="w-3 h-3 rounded-full bg-green-400" />
              <div className="mx-auto text-[10px] font-mono text-ink-mute tracking-widest">FIXFIND_AI_AGENT</div>
            </div>
            
            <div className="p-8 flex-1 flex flex-col gap-6">
               <div className="flex justify-end">
                 <div className="bg-primary-tint border border-primary/20 text-primary px-5 py-4 rounded-l-[2rem] rounded-tr-[2rem] max-w-[80%] text-sm font-bold shadow-sm">
                    "My AC started leaking water from the indoor unit just now."
                 </div>
               </div>

               {/* AI Detection Badge */}
               <motion.div 
                 initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 1.5 }}
                 className="flex items-center gap-2 bg-accent/10 border border-accent/20 w-fit px-4 py-2 rounded-full text-xs font-mono text-accent font-bold"
               >
                 <Zap className="w-3 h-3" />
                 <span>AI DETECTION: WATER_LEAKAGE → AC_REPAIR</span>
               </motion.div>

               {/* Mock Card */}
               <motion.div 
                 initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 2 }}
                 className="bg-surface border border-border p-6 rounded-2xl mt-auto shadow-lg shadow-black/5"
               >
                 <div className="flex justify-between items-start mb-4">
                   <div>
                     <h4 className="font-black text-lg text-ink">CoolCare Services</h4>
                     <p className="text-ink-soft text-xs font-medium mt-1">Specialization: Leakage & Drainage</p>
                   </div>
                   <div className="bg-accent text-ink text-xs font-black px-3 py-1.5 rounded-full shadow-sm">
                     95% FIT
                   </div>
                 </div>
                 <div className="flex gap-4 text-xs font-bold text-ink-soft">
                    <span className="flex items-center gap-1.5 bg-background px-3 py-1.5 rounded-lg border border-border"><MapPin className="w-3 h-3 text-primary"/> 2.1 km</span>
                    <span className="flex items-center gap-1.5 bg-background px-3 py-1.5 rounded-lg border border-border"><CheckCircle2 className="w-3 h-3 text-ok"/> Available Today</span>
                 </div>
               </motion.div>
            </div>

            {/* Floating Badges */}
            <motion.div animate={{ y: [0, -10, 0] }} transition={{ repeat: Infinity, duration: 4, ease: "easeInOut" }} className="absolute -left-6 top-32 bg-surface border border-border shadow-xl px-5 py-3 rounded-xl font-bold text-sm flex items-center gap-2 text-ink">
              <ShieldCheck className="w-5 h-5 text-ok" /> Verified Network
            </motion.div>
            <motion.div animate={{ y: [0, 10, 0] }} transition={{ repeat: Infinity, duration: 5, ease: "easeInOut" }} className="absolute -right-8 bottom-32 bg-primary text-white shadow-primary/20 shadow-2xl px-5 py-3 rounded-xl font-bold text-sm">
              Deterministic Ranking
            </motion.div>
          </motion.div>

        </motion.div>
      </section>

      {/* 3. Product Experience - Multimodal Input */}
      <section className="py-32 bg-surface border-y border-border">
        <div className="max-w-4xl mx-auto px-8 text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-black uppercase tracking-tighter mb-6 text-ink">FIND THE RIGHT SERVICE<br/>FOR YOUR PROBLEM.</h2>
          <p className="text-xl text-ink-soft font-medium">Describe what is wrong and let FixFind identify the service and discover suitable nearby providers.</p>
        </div>

        <div className="max-w-3xl mx-auto px-8">
          <div className="bg-surface border-2 border-border rounded-3xl shadow-xl overflow-hidden focus-within:border-primary/50 transition-colors duration-500">
            <textarea 
              placeholder="What's wrong? e.g., My AC is leaking water from the indoor unit..."
              className="w-full bg-transparent p-8 min-h-[150px] outline-none text-xl resize-none placeholder:text-ink-mute text-ink font-medium"
            />
            <div className="bg-background border-t border-border p-4 flex items-center justify-between">
              <div className="flex gap-2">
                <button className="p-3 hover:bg-surface rounded-xl transition-colors text-ink-mute hover:text-primary border border-transparent hover:border-border"><Mic className="w-6 h-6"/></button>
                <button className="p-3 hover:bg-surface rounded-xl transition-colors text-ink-mute hover:text-primary border border-transparent hover:border-border"><Camera className="w-6 h-6"/></button>
                <button className="p-3 hover:bg-surface rounded-xl transition-colors text-ink-mute hover:text-primary border border-transparent hover:border-border"><MapPin className="w-6 h-6"/></button>
              </div>
              <button onClick={() => router.push('/login')} className="bg-primary text-white px-8 py-4 rounded-xl font-bold text-sm hover:bg-primary-hover transition-colors flex items-center gap-2 shadow-md">
                ANALYZE PROBLEM <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* 4. Scroll Experience: How It Works */}
      <section className="py-32 bg-background">
        <div className="max-w-7xl mx-auto px-8">
          <div className="mb-24">
            <h4 className="text-primary font-bold tracking-widest text-sm uppercase mb-4">Simple & Smart</h4>
            <h2 className="text-5xl font-black uppercase tracking-tighter text-ink">HOW IT WORKS</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-16 relative">
             {/* Sticky Left Column */}
             <div className="relative">
                <div className="sticky top-32 space-y-16">
                  {[
                    { num: "01", title: "DESCRIBE THE PROBLEM", desc: "Text, image, voice, or location." },
                    { num: "02", title: "FIXFIND UNDERSTANDS", desc: "AI identifies the problem and required service." },
                    { num: "03", title: "DISCOVER PROVIDERS", desc: "Nearby providers evaluated using Service Fit Score." },
                    { num: "04", title: "REQUEST SERVICE", desc: "Select a provider and submit your request." }
                  ].map((step, idx) => (
                    <motion.div 
                      key={idx}
                      whileInView={{ opacity: 1, x: 0 }}
                      initial={{ opacity: 0.4, x: -20 }}
                      viewport={{ margin: "-40% 0px -40% 0px", amount: "all" }}
                      onViewportEnter={() => setActiveStep(idx)}
                      className={`transition-opacity duration-500 ${activeStep === idx ? 'opacity-100' : 'opacity-40'}`}
                    >
                      <h1 className="text-7xl font-black text-ink/10 mb-2">{step.num}</h1>
                      <h3 className="text-2xl font-black uppercase mb-3 text-ink">{step.title}</h3>
                      <p className="text-ink-soft font-bold text-lg">{step.desc}</p>
                    </motion.div>
                  ))}
                </div>
             </div>

             {/* Dynamic Right Column Visual */}
             <div className="h-[600px] sticky top-32 bg-surface border-2 border-border rounded-[2rem] flex items-center justify-center overflow-hidden p-8 shadow-xl">
                <AnimatePresence mode="wait">
                  <motion.div 
                    key={activeStep}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 1.1 }}
                    transition={{ duration: 0.5 }}
                    className="text-center font-mono font-bold text-2xl w-full"
                  >
                    {activeStep === 0 && <span className="text-ink-soft text-3xl">"My sink is blocked."</span>}
                    {activeStep === 1 && (
                      <div className="bg-primary-tint border-2 border-primary/20 p-8 rounded-2xl mx-auto max-w-sm text-left">
                        <span className="text-primary block mb-2 text-sm uppercase tracking-widest">Detected Intent</span>
                        <span className="text-ink text-xl">{"{ intent: 'plumbing_blockage' }"}</span>
                      </div>
                    )}
                    {activeStep === 2 && (
                       <div className="bg-background border border-border p-8 rounded-2xl mx-auto max-w-sm flex items-center gap-4">
                         <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin" />
                         <span className="text-ink text-lg font-sans">Searching Radius: 5km...</span>
                       </div>
                    )}
                    {activeStep === 3 && (
                      <div className="bg-ok/10 border-2 border-ok/30 text-ok px-8 py-6 rounded-2xl inline-flex items-center gap-3 font-sans text-xl shadow-sm">
                        <CheckCircle2 className="w-8 h-8" /> Booking Confirmed
                      </div>
                    )}
                  </motion.div>
                </AnimatePresence>
             </div>
          </div>
        </div>
      </section>

      {/* 5. Trust / Service Fit Score */}
      <section className="py-32 bg-surface border-y border-border">
         <div className="max-w-7xl mx-auto px-8 grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className="text-5xl font-black uppercase tracking-tighter mb-6 text-ink">FIND WITH CONFIDENCE.</h2>
              <p className="text-xl text-ink-soft mb-10 font-medium leading-relaxed">FixFind combines AI reasoning with deterministic provider data and ranking. Providers are ranked by a transparent Service Fit Score.</p>
              
              <div className="space-y-4">
                {[
                  { label: "Problem Compatibility", val: "35%" },
                  { label: "Specialization", val: "20%" },
                  { label: "Availability", val: "15%" },
                  { label: "Distance", val: "15%" },
                  { label: "Rating", val: "10%" },
                  { label: "Price", val: "5%" },
                ].map((stat, i) => (
                  <div key={i} className="flex justify-between items-center border-b border-border pb-3">
                    <span className="font-bold text-ink">{stat.label}</span>
                    <span className="font-mono text-primary font-bold">{stat.val}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-background rounded-[3rem] p-12 flex flex-col items-center justify-center relative overflow-hidden border border-border shadow-xl h-[500px]">
               <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,var(--color-primary-tint)_0%,transparent_70%)]" />
               <motion.div initial={{ scale: 0 }} whileInView={{ scale: 1 }} viewport={{ once: true }} transition={{ type: "spring", bounce: 0.5 }} className="w-56 h-56 rounded-full border-[12px] border-primary flex flex-col items-center justify-center relative z-10 bg-surface shadow-2xl">
                  <span className="text-6xl font-black text-ink">95%</span>
                  <span className="text-sm font-bold text-ink-soft uppercase tracking-widest mt-2">Service Fit</span>
               </motion.div>
            </div>
         </div>
      </section>

      {/* 6. Testimonials / Scenarios Marquee */}
      <section className="py-24 bg-primary overflow-hidden">
        <h4 className="text-center font-bold tracking-widest text-sm uppercase mb-16 text-primary-tint">REAL PROBLEMS. REAL SCENARIOS.</h4>
        <div className="flex gap-8 whitespace-nowrap px-8">
           <motion.div 
             animate={{ x: ["0%", "-50%"] }} 
             transition={{ ease: "linear", duration: 30, repeat: Infinity }}
             className="flex gap-8"
           >
             {[...mockScenarios, ...mockScenarios].map((scen, i) => (
               <div key={i} className="bg-white/10 backdrop-blur-md px-10 py-8 text-2xl font-bold rounded-2xl border border-white/20 shrink-0 text-white shadow-xl">
                 "{scen}"
               </div>
             ))}
           </motion.div>
        </div>
      </section>

      {/* 7. Final CTA */}
      <section className="py-40 bg-surface text-center px-8">
         <motion.div initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="max-w-3xl mx-auto">
           <h2 className="text-6xl md:text-[5rem] font-black uppercase tracking-tighter mb-8 leading-[0.9] text-ink">GOT A PROBLEM?<br/>DESCRIBE IT.</h2>
           <p className="text-xl text-ink-soft mb-12 font-bold">Tell FixFind what's wrong and let it figure out the right service and suitable nearby provider.</p>
           <button onClick={() => router.push('/login')} className="bg-primary text-white px-12 py-6 rounded-2xl font-black text-lg hover:scale-105 transition-transform flex items-center gap-3 mx-auto shadow-2xl shadow-primary/30">
             DESCRIBE A PROBLEM <ArrowRight className="w-6 h-6" />
           </button>
         </motion.div>
      </section>

      {/* 8. Footer */}
      <footer className="bg-background py-16 px-8 border-t border-border">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8">
          <div>
            <div className="font-black text-3xl tracking-tighter flex items-center gap-2 mb-3 text-ink">
              <div className="w-5 h-5 bg-primary rounded-sm" />
              <span>FixFind <span className="text-primary">AI</span></span>
            </div>
            <p className="text-ink-soft text-base font-bold">Don't search for a service. Describe the problem.</p>
          </div>
          <div className="flex gap-8 text-sm font-bold text-ink-mute">
            <a href="#" className="hover:text-primary transition-colors">Product</a>
            <a href="#" className="hover:text-primary transition-colors">Providers</a>
            <a href="#" className="hover:text-white transition-colors">Privacy</a>
            <a href="#" className="hover:text-white transition-colors">Terms</a>
          </div>
        </div>
      </footer>

    </main>
  );
}
