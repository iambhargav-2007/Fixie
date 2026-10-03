"use client";

import { motion } from "framer-motion";
import { Search, Cpu, CheckCircle } from "lucide-react";
import { useEffect, useState } from "react";

const steps = [
  { icon: Search, text: "Extracting object identifiers..." },
  { icon: Cpu, text: "Diagnosing fault and severity..." },
  { icon: CheckCircle, text: "Mapping to service requirements..." },
];

export default function AnalyzingState({ onComplete }: { onComplete: () => void }) {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    if (currentStep < steps.length) {
      const timer = setTimeout(() => {
        setCurrentStep(prev => prev + 1);
      }, 800); // 800ms per step
      return () => clearTimeout(timer);
    } else {
      const timer = setTimeout(() => {
        onComplete();
      }, 500);
      return () => clearTimeout(timer);
    }
  }, [currentStep, onComplete]);

  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className="w-full max-w-3xl mx-auto glass-card rounded-2xl p-8 relative overflow-hidden"
    >
      {/* Scanning Line overlay */}
      <motion.div
        animate={{ y: ["-10%", "110%", "-10%"] }}
        transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
        className="absolute left-0 right-0 h-8 bg-gradient-to-b from-transparent via-primary/10 to-transparent pointer-events-none border-b border-primary/20"
      />
      
      <div className="flex flex-col gap-4">
        {steps.map((step, index) => {
          const Icon = step.icon;
          const isActive = index === currentStep;
          const isPast = index < currentStep;
          
          return (
            <motion.div 
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: isPast || isActive ? 1 : 0.3, x: isPast || isActive ? 0 : -20 }}
              className="flex items-center gap-4 text-sm md:text-base font-mono"
            >
              <div className={`p-2 rounded flex items-center justify-center transition-colors ${isPast ? 'bg-primary/20 text-primary' : isActive ? 'bg-accent/20 text-accent animate-pulse' : 'bg-surface text-muted'}`}>
                <Icon className="w-5 h-5" />
              </div>
              <span className={isPast ? 'text-foreground' : isActive ? 'text-accent' : 'text-muted'}>
                {step.text}
              </span>
            </motion.div>
          );
        })}
      </div>
    </motion.div>
  );
}
