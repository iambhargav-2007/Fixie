"use client";

import { motion } from "framer-motion";
import { Search, MapPin, Calendar, Wrench, ChevronDown } from "lucide-react";

export default function SearchPill() {
  return (
    <div className="w-full max-w-5xl mx-auto relative z-20">
      {/* Background dashed line simulation */}
      <div className="absolute top-1/2 left-[-100%] right-[-100%] border-t-2 border-dashed border-primary/40 -z-10 opacity-50" />
      
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="bg-[#1a1a1a] rounded-[2rem] p-2 flex flex-col md:flex-row items-center gap-2 shadow-2xl shadow-primary/10 border border-white/10"
      >
        <div className="flex-1 flex items-center px-4 py-3 hover:bg-white/5 rounded-2xl cursor-text transition-colors">
          <div className="flex flex-col w-full">
            <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-1">Problem</span>
            <div className="flex items-center gap-2 text-zinc-300">
              <Wrench className="w-4 h-4 text-primary" />
              <input type="text" placeholder="Describe issue..." className="bg-transparent outline-none w-full text-sm font-medium placeholder-zinc-600" />
            </div>
          </div>
        </div>

        <div className="w-px h-10 bg-white/10 hidden md:block" />

        <div className="flex-1 flex items-center px-4 py-3 hover:bg-white/5 rounded-2xl cursor-text transition-colors">
          <div className="flex flex-col w-full">
            <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-1">Location</span>
            <div className="flex items-center gap-2 text-zinc-300">
              <MapPin className="w-4 h-4 text-primary" />
              <input type="text" placeholder="Area or Zip code" className="bg-transparent outline-none w-full text-sm font-medium placeholder-zinc-600" />
            </div>
          </div>
        </div>

        <div className="w-px h-10 bg-white/10 hidden md:block" />

        <div className="flex-[0.8] flex items-center px-4 py-3 hover:bg-white/5 rounded-2xl cursor-pointer transition-colors">
          <div className="flex flex-col w-full">
            <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-1">When</span>
            <div className="flex items-center gap-2 text-zinc-300">
              <Calendar className="w-4 h-4 text-primary" />
              <span className="text-sm font-medium">Today</span>
            </div>
          </div>
        </div>

        <div className="w-px h-10 bg-white/10 hidden md:block" />

        <div className="flex-[0.8] flex items-center px-4 py-3 hover:bg-white/5 rounded-2xl cursor-pointer transition-colors justify-between">
          <div className="flex flex-col">
            <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-1">Urgency</span>
            <div className="flex items-center gap-2 text-zinc-300">
              <span className="text-sm font-medium">High</span>
            </div>
          </div>
          <ChevronDown className="w-4 h-4 text-zinc-500" />
        </div>

        <button className="bg-primary hover:bg-primary/90 text-black p-4 rounded-[1.5rem] flex items-center justify-center transition-transform hover:scale-105 min-w-[72px]">
          <Search className="w-6 h-6" />
        </button>
      </motion.div>
      
      <div className="flex flex-wrap justify-center gap-4 mt-6">
        {["Plumbing", "Electrical", "AC Repair", "Carpentry", "Appliance"].map((tag) => (
          <span key={tag} className="px-4 py-1.5 rounded-full bg-white/5 text-zinc-400 text-xs font-semibold hover:bg-white/10 cursor-pointer transition-colors">
            {tag}
          </span>
        ))}
      </div>
    </div>
  );
}
