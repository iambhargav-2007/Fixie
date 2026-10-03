"use client";

import { motion } from "framer-motion";
import { Mic, Image as ImageIcon, MapPin, Sparkles } from "lucide-react";
import React from "react";

export default function AnimatedHero() {
  return (
    <div className="relative overflow-hidden w-full min-h-[80vh] flex flex-col items-center justify-center pt-20 pb-32">
      {/* Subtle grid background instead of AI glow */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px] pointer-events-none" />

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="z-10 flex flex-col items-center text-center max-w-4xl px-6"
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="flex items-center gap-2 px-4 py-2 rounded-full bg-surface border border-border text-sm text-primary font-medium mb-8 shadow-sm shadow-primary/10"
        >
          <Sparkles className="w-4 h-4" />
          <span>The problem-first service network</span>
        </motion.div>

        <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-foreground mb-6 leading-tight">
          Don't search for a service. <br />
          <span className="text-primary">
            Describe the problem.
          </span>
        </h1>

        <p className="text-lg md:text-xl text-zinc-400 max-w-2xl mb-12 leading-relaxed">
          Upload a photo or describe what's broken. Our AI analyzes the issue, identifies the required expertise, and matches you with the best available local professionals instantly.
        </p>

        {/* Mock Interactive Input Area (Hero visual) */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.8, ease: "easeOut" }}
          className="w-full max-w-2xl glass-card rounded-2xl p-4 flex flex-col md:flex-row items-center gap-4 relative overflow-hidden group hover:border-primary/30 transition-colors"
        >
          <div className="absolute inset-0 bg-primary/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />
          
          <input 
            type="text"
            placeholder="e.g. My AC is leaking water from the indoor unit..."
            className="flex-1 bg-transparent border-none outline-none text-white placeholder-zinc-500 px-4 py-2 w-full"
            disabled
          />
          
          <div className="flex items-center gap-2 text-zinc-400 shrink-0 pr-2">
            <button className="p-2 rounded-full hover:bg-white/10 hover:text-white transition-colors">
              <Mic className="w-5 h-5" />
            </button>
            <button className="p-2 rounded-full hover:bg-white/10 hover:text-white transition-colors">
              <ImageIcon className="w-5 h-5" />
            </button>
            <button className="p-2 rounded-full hover:bg-white/10 hover:text-white transition-colors">
              <MapPin className="w-5 h-5" />
            </button>
            <button className="bg-primary text-black px-6 py-2 rounded-full font-semibold ml-2 hover:bg-highlight hover:scale-105 transition-all">
              Analyze
            </button>
          </div>
        </motion.div>
      </motion.div>
    </div>
  );
}
