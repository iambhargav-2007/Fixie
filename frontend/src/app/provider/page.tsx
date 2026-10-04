"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  CheckCircle2, MapPin, Briefcase, AlertCircle, X, Wrench, Image as ImageIcon, LayoutGrid, History, User, Check, Star, Clock, Zap
} from "lucide-react";
import { api } from "@/lib/api";
import { useRouter } from "next/navigation";

export default function ProviderDashboard() {
  const router = useRouter();
  const [requests, setRequests] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  // Poll for requests
  useEffect(() => {
    const fetchRequests = async () => {
      try {
        const reqs = await api.listRequests();
        setRequests(reqs.filter((r: any) => r.status === 'pending'));
        setLoading(false);
      } catch (e) {
        console.error("Failed to fetch requests", e);
      }
    };
    fetchRequests();
    const interval = setInterval(fetchRequests, 2000);
    return () => clearInterval(interval);
  }, []);

  const handleAccept = async (reqId: string) => {
    try {
      await api.updateRequestStatus(reqId, "accepted");
      setRequests(prev => prev.filter(r => r.id !== reqId));
    } catch (e) {
      alert("Failed to accept");
    }
  };

  const handleReject = async (reqId: string) => {
    try {
      await api.updateRequestStatus(reqId, "declined");
      setRequests(prev => prev.filter(r => r.id !== reqId));
    } catch (e) {
      alert("Failed to reject");
    }
  };

  return (
    <div className="flex h-screen bg-[#1e1e1e] text-[#e0e0e0] font-sans selection:bg-[#3d3d3d] overflow-hidden">
      
      {/* Sidebar */}
      <div className="w-64 bg-[#252526] border-r border-[#333] flex flex-col justify-between flex-shrink-0 h-full">
        <div>
          <div className="p-6 pb-8 flex items-center gap-3 font-black text-xl text-white tracking-tight cursor-pointer" onClick={() => router.push('/')}>
            <div className="w-6 h-6 bg-emerald-500 rounded-md flex items-center justify-center text-white">
               <Wrench className="w-4 h-4" />
            </div>
            <span>FixFind AI</span>
          </div>
          
          <nav className="px-4 space-y-1">
            <div className="flex items-center gap-3 bg-emerald-500/10 text-emerald-500 border border-emerald-500/20 font-bold px-4 py-3 rounded-xl cursor-pointer">
              <Briefcase className="w-5 h-5" />
              Workspace
            </div>
          </nav>
        </div>
        
        <div className="p-4 m-4 bg-[#1e1e1e] rounded-2xl border border-[#404040] shadow-sm relative">
          <div className="absolute -left-3 -bottom-3 w-10 h-10 bg-[#1e1e1e] border border-[#404040] rounded-full flex items-center justify-center text-white font-black shadow-lg z-10">
            N
          </div>
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 bg-orange-500/10 text-orange-500 rounded-full flex items-center justify-center font-bold text-sm">
              CC
            </div>
            <div>
              <div className="font-bold text-sm text-white">CoolCare Services</div>
              <div className="flex items-center text-xs text-gray-400 font-medium mt-0.5">
                <Star className="w-3 h-3 text-yellow-500 fill-current mr-1" /> 4.7 (128)
              </div>
            </div>
          </div>
          <div className="bg-emerald-500/10 text-emerald-500 text-xs font-bold px-3 py-1.5 rounded-lg flex items-center justify-center gap-2 border border-emerald-500/20">
            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
            AVAILABLE
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto p-8 md:p-12">
        <div className="max-w-5xl mx-auto">
          
          <div className="mb-10">
            <h1 className="text-3xl font-bold text-white mb-2 tracking-tight">Good evening, CoolCare Services</h1>
            <p className="text-gray-400 font-medium">You have {requests.length} new requests waiting for a response.</p>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-10">
            <div className="bg-[#252526] border border-[#333] rounded-2xl p-5 shadow-sm">
              <div className="text-3xl font-bold text-white mb-1">{requests.length}</div>
              <div className="text-sm font-bold text-gray-300">New requests</div>
              <div className="text-xs text-gray-500 font-medium mt-2">{requests.length} awaiting reply</div>
            </div>
            <div className="bg-[#1e1e1e] border border-[#333] rounded-2xl p-5 opacity-70">
              <div className="text-3xl font-bold text-gray-500 mb-1">0</div>
              <div className="text-sm font-bold text-gray-400">Active jobs</div>
              <div className="text-xs text-gray-500 font-medium mt-2">0 in progress</div>
            </div>
            <div className="bg-[#252526] border border-[#333] rounded-2xl p-5 shadow-sm">
              <div className="text-3xl font-bold text-white mb-1">128</div>
              <div className="text-sm font-bold text-gray-300">Completed this month</div>
              <div className="text-xs text-gray-500 font-medium mt-2">128 all time</div>
            </div>
            <div className="bg-[#252526] border border-[#333] rounded-2xl p-5 shadow-sm">
              <div className="text-3xl font-bold text-white mb-1 flex items-center gap-2">
                4.7 <Star className="w-6 h-6 text-yellow-500 fill-current" />
              </div>
              <div className="text-sm font-bold text-gray-300">Rating</div>
              <div className="text-xs text-gray-500 font-medium mt-2">4.7 from 128 reviews</div>
            </div>
          </div>

          {/* Tabs */}
          <div className="flex border-b border-[#333] mb-8 gap-8">
            <div className="pb-3 border-b-2 border-emerald-500 text-sm font-bold text-emerald-500 cursor-pointer">
              NEW REQUESTS ({requests.length})
            </div>
            <div className="pb-3 text-sm font-bold text-gray-500 cursor-pointer">
              ACTIVE JOBS (0)
            </div>
          </div>

          {/* Request List */}
          {loading ? (
             <div className="text-center py-20 text-gray-500 font-bold animate-pulse">Loading requests...</div>
          ) : requests.length === 0 ? (
            <div className="bg-[#252526] border border-[#333] rounded-3xl p-16 text-center shadow-sm">
              <div className="w-16 h-16 bg-[#1e1e1e] rounded-full flex items-center justify-center mx-auto mb-4 border border-[#404040]">
                <AlertCircle className="w-8 h-8 text-gray-500" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">No new requests</h3>
              <p className="text-gray-400 max-w-sm mx-auto">You're all caught up! New service requests will appear here.</p>
            </div>
          ) : (
            <div className="space-y-6">
              <AnimatePresence>
                {requests.map((req, idx) => {
                  const isHighPriority = req.problem?.urgency === 'High' || idx === 1; // dummy logic for visual
                  return (
                  <motion.div 
                    key={req.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, x: -50 }}
                    className="bg-[#252526] border border-[#404040] rounded-3xl p-6 shadow-xl relative overflow-hidden"
                  >
                    <div className="flex items-center gap-4 mb-4 text-xs font-bold text-gray-400">
                      <div className={`px-3 py-1 rounded-full ${isHighPriority ? 'bg-red-500/10 text-red-500 border border-red-500/20' : 'bg-orange-500/10 text-orange-500 border border-orange-500/20'}`}>
                        {isHighPriority ? 'HIGH PRIORITY' : 'MEDIUM PRIORITY'}
                      </div>
                      <div>Received just now</div>
                      <div>•</div>
                      <div className="flex items-center gap-1">
                        Rahul <MapPin className="w-3 h-3" /> (2.1 km away)
                      </div>
                    </div>

                    <h2 className="text-xl font-medium text-white mb-6">
                      "{req.problem?.issue_summary || 'No specific details provided.'}"
                    </h2>

                    <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-2xl p-5 mb-6">
                      <div className="flex items-center gap-2 text-xs font-bold text-emerald-500 uppercase tracking-wider mb-4">
                        <Zap className="w-4 h-4 fill-current" /> FixFind Understood
                      </div>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-sm">
                        <div>
                          <div className="text-gray-400 mb-1">Problem</div>
                          <div className="font-bold text-white">{req.problem?.object || 'Unknown object'}</div>
                        </div>
                        <div>
                          <div className="text-gray-400 mb-1">Service</div>
                          <div className="font-bold text-white">{req.service?.service?.replace(/_/g, ' ') || 'General Repair'}</div>
                        </div>
                        <div>
                          <div className="text-gray-400 mb-1">Specialization</div>
                          <div className="font-bold text-white">{req.service?.category?.replace(/_/g, ' ') || 'General'}</div>
                        </div>
                        <div>
                          <div className="text-gray-400 mb-1">Likely Area</div>
                          <div className="font-bold text-white">Indoor unit</div>
                        </div>
                      </div>
                    </div>

                    <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-6">
                      <div className="space-y-4">
                        <div className="flex flex-wrap gap-3 text-sm font-medium">
                          <div className="flex items-center gap-2 bg-[#1e1e1e] border border-[#333] px-3 py-1.5 rounded-lg text-gray-300">
                            <MapPin className="w-4 h-4 text-gray-500" /> Banjara Hills - 2.1 km
                          </div>
                          <div className="flex items-center gap-2 bg-[#1e1e1e] border border-[#333] px-3 py-1.5 rounded-lg text-gray-300">
                            <Clock className="w-4 h-4 text-gray-500" /> Today, 4:00 PM – 6:00 PM
                          </div>
                          <div className="flex items-center gap-2 bg-[#1e1e1e] border border-[#333] px-3 py-1.5 rounded-lg text-gray-300">
                            ₹ 400 - ₹ 700
                          </div>
                        </div>
                        <div className="flex items-center gap-2 text-sm text-emerald-500 font-medium">
                          <CheckCircle2 className="w-4 h-4" /> Matches your specialization: AC leakage & drainage
                        </div>
                      </div>
                      
                      <div className="w-24 h-24 bg-[#1e1e1e] border border-[#333] rounded-xl flex flex-col items-center justify-center text-gray-500 flex-shrink-0">
                        <ImageIcon className="w-6 h-6 mb-1" />
                        <span className="text-xs font-bold">1 photo</span>
                      </div>
                    </div>

                    <div className="flex items-center justify-between border-t border-[#333] pt-6">
                      <div className="flex gap-3">
                        <button 
                          onClick={() => handleAccept(req.id)}
                          className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-2.5 px-8 rounded-xl transition-colors shadow-lg shadow-emerald-900/20"
                        >
                          Accept
                        </button>
                        <button 
                          onClick={() => handleReject(req.id)}
                          className="bg-transparent hover:bg-red-500/10 text-red-500 border border-red-500/30 hover:border-red-500/50 font-bold py-2.5 px-8 rounded-xl transition-colors"
                        >
                          Decline
                        </button>
                      </div>
                      <button className="text-sm font-bold text-gray-400 hover:text-white transition-colors">
                        View details
                      </button>
                    </div>

                  </motion.div>
                )})}
              </AnimatePresence>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
