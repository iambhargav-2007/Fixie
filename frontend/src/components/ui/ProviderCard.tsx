"use client";

import { motion } from "framer-motion";
import { Star, Clock, ArrowRight, ShieldCheck } from "lucide-react";

export interface ProviderData {
  id: string;
  name: string;
  specialization: string;
  distance_km: number;
  rating: number;
  price_min: number;
  price_max: number;
  availability: string;
  fit_score: number;
  colorTheme: string;
}

export default function ProviderCard({ provider }: { provider: ProviderData }) {
  const getInitials = (name: string) => name.split(' ').map(n => n[0]).join('').substring(0, 2);

  return (
    <motion.div
      whileHover={{ y: -5 }}
      className="bg-white rounded-3xl p-6 shadow-sm border border-zinc-100 flex flex-col relative overflow-hidden group"
    >
      {/* Top Border Color Line */}
      <div className={`absolute top-0 left-0 right-0 h-1.5 ${provider.colorTheme}`} />

      {/* Header */}
      <div className="flex justify-between items-start mb-6 pt-2">
        <div className="flex items-center gap-3">
          <div className={`w-12 h-12 rounded-full text-white font-bold flex items-center justify-center relative ${provider.colorTheme}`}>
            {getInitials(provider.name)}
            <div className="absolute -bottom-1 -right-1 bg-white rounded-full p-0.5">
              <ShieldCheck className="w-4 h-4 text-orange-500" fill="currentColor" />
            </div>
          </div>
          <div>
            <h3 className="text-black font-black text-lg leading-none mb-1">{provider.name}</h3>
            <span className="text-zinc-500 text-sm font-medium">{provider.specialization}</span>
          </div>
        </div>
        <div className="text-right">
          <h3 className="text-black font-black text-2xl leading-none tracking-tight">
            <span className={`text-xl ${provider.colorTheme.replace('bg-', 'text-')}`}>₹</span>{provider.price_min}
          </h3>
          <span className="text-zinc-400 text-xs font-medium">base fare / visit</span>
        </div>
      </div>

      {/* Route / Service Details (Vertical Line) */}
      <div className="bg-zinc-50 rounded-2xl p-4 mb-6 relative">
        <div className="absolute left-6 top-6 bottom-6 w-px bg-zinc-200 border-l border-dashed border-zinc-300" />
        
        <div className="flex items-center gap-4 mb-4 relative z-10">
          <div className={`w-3 h-3 rounded-full ${provider.colorTheme}`} />
          <div>
            <h4 className="text-black font-bold text-sm">Issue Diagnosis</h4>
            <span className="text-zinc-500 text-xs font-medium">{provider.distance_km} km away from your location</span>
          </div>
        </div>
        
        <div className="flex items-center gap-4 relative z-10">
          <div className={`w-3 h-3 rounded-full ${provider.colorTheme}`} />
          <div>
            <h4 className="text-black font-bold text-sm">Service Location</h4>
            <span className="text-zinc-500 text-xs font-medium">Home Visit</span>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between mt-auto">
        <div className="flex items-center gap-2 text-primary font-bold text-sm bg-primary/10 px-3 py-1.5 rounded-full">
          <Clock className="w-4 h-4" />
          <span>{provider.availability.replace('_', ' ')}</span>
        </div>
        
        <div className="flex items-center gap-1 text-zinc-500 text-sm font-bold bg-zinc-100 px-3 py-1.5 rounded-full">
          <Star className="w-4 h-4 text-yellow-500" fill="currentColor" />
          <span>{provider.rating} Rating</span>
        </div>
      </div>

      <button className={`mt-6 w-fit text-white px-6 py-2.5 rounded-full font-bold text-sm flex items-center gap-2 hover:opacity-90 transition-opacity ${provider.colorTheme}`}>
        Request Service <ArrowRight className="w-4 h-4" />
      </button>
    </motion.div>
  );
}
