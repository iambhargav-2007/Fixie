"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Eye, EyeOff, Wrench, Briefcase, Loader2, ArrowRight } from "lucide-react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [role, setRole] = useState<'customer' | 'provider'>('customer');
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    
    if (!username.trim()) {
      setError("Please enter your username.");
      return;
    }
    if (!password.trim()) {
      setError("Please enter your password.");
      return;
    }

    setLoading(true);

    // Mock Authentication Delay to demonstrate the polished loading state
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Proceed to respective dashboards
    if (role === 'customer') {
      router.push("/customer");
    } else {
      router.push("/provider");
    }
    
    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-background text-foreground font-sans flex flex-col md:flex-row selection:bg-primary selection:text-white">
      
      {/* Left side: Branding / Product Visual */}
      <div className="hidden md:flex flex-1 bg-surface border-r border-border flex-col justify-between p-12 relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,var(--color-primary-tint)_0%,transparent_50%)]" />
        
        <div className="relative z-10 flex items-center gap-2 text-ink">
          <div className="w-5 h-5 bg-primary rounded-sm" />
          <span className="font-black text-2xl tracking-tighter">FixFind <span className="text-primary">AI</span></span>
        </div>

        <div className="relative z-10 max-w-md">
          <motion.h1 
            key={role}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-5xl font-black uppercase tracking-tighter leading-[0.9] text-ink mb-6"
          >
            {role === 'customer' ? "DON'T SEARCH FOR A SERVICE." : "SOLVE PROBLEMS. GROW BUSINESS."}
          </motion.h1>
          <motion.p 
            key={role + "-desc"}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="text-lg text-ink-soft font-medium"
          >
            {role === 'customer' 
              ? "Describe what's wrong and let FixFind understand the problem and connect you with suitable nearby professionals." 
              : "Receive AI-briefed jobs, accept local requests, and manage your schedule without the friction."}
          </motion.p>
        </div>

        <div className="relative z-10 text-ink-mute text-sm font-bold">
          © 2026 FixFind AI Inc.
        </div>
      </div>

      {/* Right side: Login Form */}
      <div className="flex-1 flex items-center justify-center p-8 bg-background relative">
        <div className="w-full max-w-md">
          
          <div className="mb-10 md:hidden flex items-center gap-2 text-ink">
            <div className="w-5 h-5 bg-primary rounded-sm" />
            <span className="font-black text-2xl tracking-tighter">FixFind</span>
          </div>

          <div className="mb-8">
            <h2 className="text-3xl font-black text-ink mb-2">Welcome back</h2>
            <p className="text-ink-soft font-bold">Please enter your details to sign in.</p>
          </div>

          <form onSubmit={handleLogin} className="space-y-6">
            
            {/* Role Selector Segmented Control */}
            <div className="bg-surface p-1.5 rounded-xl border border-border flex relative shadow-sm">
               {['customer', 'provider'].map((r) => {
                 const isActive = role === r;
                 return (
                   <button
                     key={r}
                     type="button"
                     onClick={() => {
                        setRole(r as 'customer' | 'provider');
                        setError("");
                     }}
                     className={`flex-1 flex items-center justify-center gap-2 py-3 rounded-lg text-sm font-bold transition-colors relative z-10 ${isActive ? 'text-white' : 'text-ink-soft hover:text-ink'}`}
                   >
                     {isActive && (
                       <motion.div 
                         layoutId="role-indicator"
                         className="absolute inset-0 bg-primary rounded-lg -z-10 shadow-md"
                         transition={{ type: "spring", bounce: 0.2, duration: 0.5 }}
                       />
                     )}
                     {r === 'customer' ? <Wrench className="w-4 h-4" /> : <Briefcase className="w-4 h-4" />}
                     {r === 'customer' ? 'Customer' : 'Provider'}
                   </button>
                 );
               })}
            </div>

            {/* Error Message */}
            <AnimatePresence mode="wait">
              {error && (
                <motion.div 
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="bg-danger/10 text-danger px-4 py-3 rounded-xl border border-danger/20 text-sm font-bold flex items-center gap-2"
                >
                  <span className="flex-shrink-0 w-1 h-4 bg-danger rounded-full" />
                  {error}
                </motion.div>
              )}
            </AnimatePresence>

            <div className="space-y-4">
              {/* Username Input */}
              <div className="space-y-2">
                <label className="text-sm font-bold text-ink" htmlFor="username">Username</label>
                <input
                  id="username"
                  type="text"
                  placeholder="Enter your username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full bg-surface border-2 border-border focus:border-primary px-4 py-3.5 rounded-xl outline-none transition-colors text-ink font-medium placeholder:text-ink-mute"
                />
              </div>

              {/* Password Input */}
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <label className="text-sm font-bold text-ink" htmlFor="password">Password</label>
                  <button type="button" className="text-xs font-bold text-primary hover:text-primary-hover">Forgot password?</button>
                </div>
                <div className="relative">
                  <input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    placeholder="Enter your password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full bg-surface border-2 border-border focus:border-primary pl-4 pr-12 py-3.5 rounded-xl outline-none transition-colors text-ink font-medium placeholder:text-ink-mute"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-4 top-1/2 -translate-y-1/2 text-ink-mute hover:text-ink transition-colors p-1"
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <button 
              type="submit" 
              disabled={loading}
              className="w-full bg-primary text-white py-4 rounded-xl font-black text-lg hover:bg-primary-hover transition-colors shadow-lg shadow-primary/20 flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed group relative overflow-hidden"
            >
              <AnimatePresence mode="wait">
                {loading ? (
                  <motion.div key="loading" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="flex items-center gap-2">
                    <Loader2 className="w-5 h-5 animate-spin" /> Signing in...
                  </motion.div>
                ) : (
                  <motion.div key="text" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="flex items-center gap-2">
                    Sign in as {role === 'customer' ? 'Customer' : 'Provider'} 
                    <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                  </motion.div>
                )}
              </AnimatePresence>
            </button>
          </form>

          <div className="mt-8 text-center text-sm font-bold text-ink-soft">
            Don't have an account? <button className="text-primary hover:text-primary-hover">Sign up</button>
          </div>

        </div>
      </div>
    </main>
  );
}
