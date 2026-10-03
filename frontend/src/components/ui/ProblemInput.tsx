"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Mic, Image as ImageIcon, MapPin, ArrowRight, Loader2 } from "lucide-react";

export default function ProblemInput({ onSubmit }: { onSubmit: (text: string) => void }) {
  const [isFocused, setIsFocused] = useState(false);
  const [text, setText] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleSubmit = () => {
    if (!text.trim()) return;
    setIsAnalyzing(true);
    setTimeout(() => {
      onSubmit(text);
      setIsAnalyzing(false);
    }, 1500); // Simulate network latency
  };

  return (
    <motion.div 
      layout
      className={`w-full max-w-3xl mx-auto glass-card rounded-2xl overflow-hidden transition-colors duration-300 ${isFocused ? 'border-primary/50 shadow-[0_0_15px_rgba(16,185,129,0.15)]' : 'border-border'}`}
    >
      <div className="p-4 flex flex-col gap-3">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          placeholder="Describe your issue or upload a photo (e.g. 'My AC is leaking water from the indoor unit...')"
          className="w-full bg-transparent border-none outline-none text-foreground placeholder-muted resize-none min-h-[80px]"
          rows={3}
          disabled={isAnalyzing}
        />
        
        <div className="flex items-center justify-between pt-2 border-t border-border/50">
          <div className="flex items-center gap-1 text-muted">
            <button className="p-2 rounded-lg hover:bg-surface hover:text-foreground transition-colors group relative">
              <Mic className="w-5 h-5 group-hover:text-primary transition-colors" />
            </button>
            <button className="p-2 rounded-lg hover:bg-surface hover:text-foreground transition-colors group relative">
              <ImageIcon className="w-5 h-5 group-hover:text-accent transition-colors" />
            </button>
            <button className="p-2 rounded-lg hover:bg-surface hover:text-foreground transition-colors group relative">
              <MapPin className="w-5 h-5 group-hover:text-primary transition-colors" />
            </button>
          </div>
          
          <button 
            onClick={handleSubmit}
            disabled={!text.trim() || isAnalyzing}
            className="flex items-center gap-2 bg-primary text-background px-5 py-2 rounded-lg font-medium hover:bg-highlight transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isAnalyzing ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Analyzing</span>
              </>
            ) : (
              <>
                <span>Diagnose</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </div>
    </motion.div>
  );
}
