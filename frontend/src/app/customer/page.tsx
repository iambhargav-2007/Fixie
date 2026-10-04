"use client";

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Send, Image as ImageIcon, MapPin, X, Wrench, CheckCircle2, Star, Clock, User, MessageSquarePlus, History, Map as MapIcon, Navigation, Check, Mic, Briefcase, Bookmark
} from "lucide-react";
import { api, ChatResponse, ProviderResponse } from "@/lib/api";
import dynamic from 'next/dynamic';

// Dynamically import the map to avoid SSR issues with Leaflet
const ProviderMap = dynamic(() => import('@/components/ProviderMap'), { ssr: false });

type Message = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  imageUrl?: string | null;
  thoughts?: string[];
  providers?: ProviderResponse[];
  problem?: any;
  service?: any;
  isThinking?: boolean;
};

type ChatSession = {
  id: string;
  title: string;
  messages: Message[];
  updatedAt: number;
};

export default function CustomerDashboard() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      role: 'assistant',
      content: 'Hello! What needs fixing today? Describe the problem or upload a photo.',
    }
  ]);
  const [inputText, setInputText] = useState("");
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const recognitionRef = useRef<any>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [currentView, setCurrentView] = useState<'chat' | 'my-fixes' | 'saved-providers'>('chat');
  const [myRequests, setMyRequests] = useState<any[]>([]);

  // Poll for requests when in my-fixes view
  useEffect(() => {
    if (currentView !== 'my-fixes') return;
    const fetchRequests = async () => {
      try {
        const reqs = await api.listRequests();
        // Since we don't have customer auth, we show all requests, sorted by newest
        setMyRequests(reqs.reverse());
      } catch (e) {
        console.error("Failed to fetch requests", e);
      }
    };
    fetchRequests();
    const interval = setInterval(fetchRequests, 2000);
    return () => clearInterval(interval);
  }, [currentView]);
  
  // Map State
  const [showMap, setShowMap] = useState(false);
  const [latestProviders, setLatestProviders] = useState<ProviderResponse[]>([]);
  const [latestProblem, setLatestProblem] = useState<any>(null);
  const [latestService, setLatestService] = useState<any>(null);
  
  const [sessionId, setSessionId] = useState("");
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const saved = localStorage.getItem('fixfind_sessions');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        setSessions(parsed);
      } catch (e) {
        console.error("Failed to parse sessions", e);
      }
    }
    
    // Initialize Web Speech API
    if (typeof window !== 'undefined') {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = false;
        
        recognition.onresult = (event: any) => {
          let currentTranscript = "";
          for (let i = event.resultIndex; i < event.results.length; i++) {
            if (event.results[i].isFinal) {
              currentTranscript += event.results[i][0].transcript;
            }
          }
          if (currentTranscript.trim()) {
            setInputText((prev) => {
              const baseText = prev.trim();
              return baseText ? `${baseText} ${currentTranscript.trim()}` : currentTranscript.trim();
            });
          }
        };

        recognition.onerror = (event: any) => {
          console.error("Speech recognition error", event.error);
          setIsRecording(false);
        };

        recognition.onend = () => {
          setIsRecording(false);
        };

        recognitionRef.current = recognition;
      }
    }
  }, []);

  // Save history on messages change
  useEffect(() => {
    if (messages.length > 1 && sessionId) {
      setSessions(prev => {
        const existingIdx = prev.findIndex(s => s.id === sessionId);
        const firstUserMsg = messages.find(m => m.role === 'user');
        const title = firstUserMsg 
          ? (firstUserMsg.content.length > 25 ? firstUserMsg.content.substring(0, 25) + "..." : firstUserMsg.content) 
          : "New Request";
        
        const newSession = {
          id: sessionId,
          title,
          messages,
          updatedAt: Date.now()
        };
        
        let newSessions;
        if (existingIdx >= 0) {
          newSessions = [...prev];
          newSessions[existingIdx] = newSession;
        } else {
          newSessions = [newSession, ...prev];
        }
        
        // Sort by most recent
        newSessions.sort((a, b) => b.updatedAt - a.updatedAt);
        
        localStorage.setItem('fixfind_sessions', JSON.stringify(newSessions));
        return newSessions;
      });
    }
  }, [messages, sessionId]);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImageUrl(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const loadSession = (sid: string) => {
    const session = sessions.find(s => s.id === sid);
    if (session) {
      setSessionId(session.id);
      setMessages(session.messages);
      
      // Find the last message that had providers and restore them
      const lastProviderMsg = [...session.messages].reverse().find(m => m.providers && m.providers.length > 0);
      setLatestProviders(lastProviderMsg?.providers || []);
      
      // Find the last problem/service
      const lastDataMsg = [...session.messages].reverse().find(m => m.problem || m.service);
      setLatestProblem(lastDataMsg?.problem || null);
      setLatestService(lastDataMsg?.service || null);
      
      setShowMap(false);
    }
  };

  const handleNewChat = () => {
    setSessionId(`session-${Math.random().toString(36).substring(7)}`);
    setMessages([
      {
        id: Date.now().toString(),
        role: 'assistant',
        content: 'Started a new session! How can I help you today?',
      }
    ]);
    setLatestProviders([]);
    setLatestProblem(null);
    setLatestService(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim() && !imageUrl) return;

    const currentText = inputText;
    const currentImg = imageUrl;
    const currentAudio = audioUrl;
    
    setInputText("");
    setImageUrl(null);
    setAudioUrl(null);
    setIsProcessing(true);

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: currentText || (currentAudio ? "[Voice Message Sent]" : ""),
      imageUrl: currentImg,
    };

    const thinkingId = (Date.now() + 1).toString();
    const thinkingMessage: Message = {
      id: thinkingId,
      role: 'assistant',
      content: '',
      isThinking: true,
      thoughts: ['Analyzing input...', 'Extracting problem details...', 'Looking up service catalog...']
    };

    setMessages(prev => [...prev, userMessage, thinkingMessage]);

    const sid = sessionId || `session-${Math.random().toString(36).substring(7)}`;
    if (!sessionId) setSessionId(sid);

    try {
      const res = await api.chat(
        sid, 
        currentText, 
        { lat: 17.3850, lng: 78.4867, locality: "Hyderabad" }, 
        currentImg || undefined,
        currentAudio || undefined
      );

      if (res.providers && res.providers.length > 0) {
        setLatestProviders(res.providers);
        setLatestProblem(res.problem);
        setLatestService(res.service);
      }

      let extractedThoughts: string[] = [];
      if (res.problem) {
         extractedThoughts.push(`Detected Object: ${res.problem.object || 'Unknown'}`);
         extractedThoughts.push(`Issue: ${res.problem.issue_summary || 'Unknown'}`);
      }
      if (res.clarification_reasoning) {
         extractedThoughts.push(`Reasoning: ${res.clarification_reasoning}`);
      }

      const responseMessage: Message = {
        id: (Date.now() + 2).toString(),
        role: 'assistant',
        content: res.clarification_question || res.recommendation?.explanation || res.message || "I found some results.",
        thoughts: extractedThoughts.length > 0 ? extractedThoughts : undefined,
        providers: res.providers && res.providers.length > 0 ? res.providers : undefined,
        problem: res.problem,
        service: res.service,
      };

      setMessages(prev => prev.map(m => m.id === thinkingId ? responseMessage : m));
    } catch (e) {
      console.error(e);
      setMessages(prev => prev.map(m => m.id === thinkingId ? {
        id: thinkingId,
        role: 'assistant',
        content: "Oops! Something went wrong while connecting to our servers. Please try again.",
      } : m));
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="flex h-screen bg-[#1e1e1e] text-[#e0e0e0] font-sans selection:bg-[#3d3d3d] overflow-hidden">
      
      {/* Sidebar */}
      <AnimatePresence>
        {isSidebarOpen && (
          <motion.div 
            initial={{ width: 0, opacity: 0 }}
            animate={{ width: 260, opacity: 1 }}
            exit={{ width: 0, opacity: 0 }}
            className="flex-shrink-0 border-r border-[#333] bg-[#252526] flex flex-col h-full overflow-hidden"
          >
            <div className="p-4">
              <button 
                onClick={handleNewChat}
                className="w-full flex items-center gap-3 bg-[#1e1e1e] hover:bg-[#2d2d2d] border border-[#404040] rounded-xl p-3 text-sm font-bold transition-colors"
              >
                <MessageSquarePlus className="w-5 h-5 text-emerald-500" />
                New Chat
              </button>
            </div>
            
            <div className="flex-1 overflow-y-auto px-4 pb-4 space-y-6 mt-4">
              <div className="space-y-2">
                <button 
                  onClick={() => setCurrentView('chat')}
                  className={`w-full flex items-center gap-3 text-sm font-medium p-2 rounded-lg transition-colors text-left ${currentView === 'chat' ? 'bg-emerald-500/10 text-emerald-500' : 'text-gray-300 hover:bg-[#333]'}`}
                >
                  <MessageSquarePlus className="w-5 h-5" />
                  Chat
                </button>
                <button 
                  onClick={() => setCurrentView('my-fixes')}
                  className={`w-full flex items-center gap-3 text-sm font-medium p-2 rounded-lg transition-colors text-left ${currentView === 'my-fixes' ? 'bg-emerald-500/10 text-emerald-500' : 'text-gray-300 hover:bg-[#333]'}`}
                >
                  <Briefcase className="w-5 h-5" />
                  My Fixes
                </button>
                <button 
                  onClick={() => setCurrentView('saved-providers')}
                  className={`w-full flex items-center gap-3 text-sm font-medium p-2 rounded-lg transition-colors text-left ${currentView === 'saved-providers' ? 'bg-emerald-500/10 text-emerald-500' : 'text-gray-300 hover:bg-[#333]'}`}
                >
                  <Bookmark className="w-5 h-5" />
                  Saved Providers
                </button>
              </div>

              <div>
                <button 
                  onClick={() => setShowMap(true)}
                  disabled={latestProviders.length === 0 || currentView !== 'chat'}
                  className="w-full flex items-center gap-3 text-sm font-medium text-gray-300 hover:text-white hover:bg-[#333] p-2 rounded-lg transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
                >
                  <MapIcon className="w-5 h-5" />
                  Map Dashboard
                </button>
              </div>

              <div>
                <div className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3 px-2">History Chats</div>
                <div className="space-y-1">
                  {sessions.length === 0 ? (
                    <div className="text-sm text-gray-600 px-2 italic">No past chats found.</div>
                  ) : (
                    sessions.map(session => (
                      <button 
                        key={session.id}
                        onClick={() => {
                          loadSession(session.id);
                          setCurrentView('chat');
                        }}
                        className={`w-full flex items-center gap-3 text-sm font-medium p-2 rounded-lg transition-colors text-left truncate ${
                          session.id === sessionId ? 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/20' : 'text-gray-300 hover:bg-[#333]'
                        }`}
                      >
                        <History className={`w-4 h-4 flex-shrink-0 ${session.id === sessionId ? 'text-emerald-500' : 'text-gray-500'}`} />
                        <span className="truncate">{session.title}</span>
                      </button>
                    ))
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="flex-1 flex flex-col h-full overflow-hidden relative">
        <header className="h-14 flex-shrink-0 flex items-center px-4 border-b border-[#333] bg-[#252526]">
          <button 
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="p-2 mr-4 hover:bg-[#333] rounded-lg transition-colors text-gray-400 hover:text-white"
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
          </button>
          <div className="flex items-center gap-2 font-bold text-lg text-white tracking-tight">
            <Wrench className="w-5 h-5 text-emerald-500" />
            <span>FixFind AI</span>
          </div>
          <div className="ml-auto flex items-center gap-1 text-sm font-medium text-gray-400">
            <MapPin className="w-4 h-4"/> Hyderabad
          </div>
        </header>

        <main className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6 scroll-smooth">
          {currentView === 'chat' && (
            <div className="max-w-4xl mx-auto space-y-8 pb-32">
            <AnimatePresence initial={false}>
              {messages.map((msg) => (
                <motion.div 
                  key={msg.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  
                  {msg.role === 'assistant' && (
                    <div className="w-10 h-10 rounded-full flex-shrink-0 flex items-center justify-center bg-emerald-600/20 border border-emerald-500/30 text-emerald-500 mt-1">
                      <Wrench className="w-5 h-5" />
                    </div>
                  )}

                  <div className={`max-w-[85%] md:max-w-[80%] space-y-2 ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                    
                    {msg.role === 'assistant' && (msg.thoughts || msg.isThinking) && (
                      <div className="pl-1 mb-2 space-y-1">
                        {(msg.thoughts || []).map((thought, idx) => (
                          <motion.div 
                             key={idx}
                             initial={{ opacity: 0, height: 0 }}
                             animate={{ opacity: 1, height: 'auto' }}
                             transition={{ delay: idx * 0.2 }}
                             className="text-[13px] font-medium text-gray-500 flex items-center gap-2 italic"
                          >
                            <div className="w-1 h-1 rounded-full bg-gray-500" />
                            {thought}
                          </motion.div>
                        ))}
                        {msg.isThinking && (
                          <div className="text-[13px] font-medium text-gray-500 flex items-center gap-2 italic mt-1 animate-pulse">
                            <div className="w-1 h-1 rounded-full bg-gray-500" />
                            ...
                          </div>
                        )}
                      </div>
                    )}

                    {(!msg.isThinking || msg.content) && (
                      <div className={`p-5 rounded-2xl ${
                        msg.role === 'user' 
                          ? 'bg-emerald-600 text-white rounded-tr-sm' 
                          : 'bg-[#2d2d2d] border border-[#404040] text-gray-100 rounded-tl-sm shadow-sm'
                      }`}>
                        
                        {msg.imageUrl && (
                          <div className="mb-4 rounded-xl overflow-hidden border border-black/20 max-w-sm">
                            <img src={msg.imageUrl} alt="Uploaded" className="w-full h-auto object-cover" />
                          </div>
                        )}

                        {/* Recommendation Explanation Section */}
                        {msg.role === 'assistant' && msg.providers && msg.providers.length > 0 && (
                          <div className="mb-6 bg-emerald-500/10 border border-emerald-500/20 p-4 rounded-xl">
                            <div className="flex items-center gap-2 font-bold text-emerald-500 mb-2">
                              <Check className="w-4 h-4" /> Why we recommend these providers:
                            </div>
                            <div className="text-gray-300 text-sm leading-relaxed">
                              {msg.content}
                            </div>
                          </div>
                        )}

                        {msg.role === 'assistant' && (!msg.providers || msg.providers.length === 0) && msg.content && (
                          <div className="whitespace-pre-wrap leading-relaxed text-gray-300">
                            {msg.content}
                          </div>
                        )}
                        {msg.role === 'user' && msg.content && (
                           <div className="whitespace-pre-wrap leading-relaxed text-white">
                             {msg.content}
                           </div>
                        )}

                        {msg.providers && msg.providers.length > 0 && (
                          <div className="mt-8 space-y-4">
                            <div className="flex justify-between items-center mb-4">
                              <div className="text-xs font-bold text-gray-400 uppercase tracking-wider">Top Matches in Hyderabad</div>
                              
                              <button 
                                onClick={() => setShowMap(true)}
                                className="flex items-center gap-1.5 text-xs font-bold bg-[#1e1e1e] hover:bg-[#333] border border-[#404040] px-3 py-1.5 rounded-lg text-emerald-500 transition-colors"
                              >
                                <Navigation className="w-3.5 h-3.5" />
                                Visit in Map
                              </button>
                            </div>

                            {msg.providers.map((p, idx) => (
                              <div key={p.id} className="bg-[#1e1e1e] border border-[#333] rounded-xl p-5 hover:border-emerald-500/50 transition-colors group">
                                <div className="flex justify-between items-start mb-3">
                                  <div>
                                    <div className="flex items-center gap-2 mb-1">
                                      <h3 className="font-bold text-white text-lg">{p.name}</h3>
                                      {p.verified && <CheckCircle2 className="w-4 h-4 text-emerald-500" />}
                                      {idx === 0 && <span className="text-[10px] bg-yellow-500/10 text-yellow-500 border border-yellow-500/30 px-1.5 py-0.5 rounded font-black tracking-widest uppercase">Best Match</span>}
                                    </div>
                                    <p className="text-sm text-gray-400 font-medium">{p.specializations.join(" · ")}</p>
                                  </div>
                                  <div className="bg-emerald-500/10 text-emerald-500 font-bold px-2 py-1 rounded-md text-xs border border-emerald-500/20 flex flex-col items-end">
                                    <span>{Math.round(p.fit_score)}% FIT</span>
                                  </div>
                                </div>
                                
                                {/* Score Breakdown Details */}
                                {idx === 0 && (
                                  <div className="my-3 flex gap-2 flex-wrap">
                                     {Object.entries(p.score_breakdown || {}).map(([key, val]) => (
                                        <div key={key} className="text-[10px] uppercase font-bold text-emerald-500/70 bg-emerald-500/5 px-2 py-1 rounded border border-emerald-500/10">
                                          {key.replace("_score", "")}: {Math.round(Number(val) * 100)}%
                                        </div>
                                     ))}
                                  </div>
                                )}

                                <div className="flex flex-wrap gap-4 text-sm mt-4">
                                  <span className="flex items-center gap-1.5 text-gray-300 bg-[#252526] px-2.5 py-1 rounded-md border border-[#333]">
                                    <MapPin className="w-4 h-4 text-gray-500" /> {p.distance_km}km
                                  </span>
                                  <span className="flex items-center gap-1.5 text-gray-300 bg-[#252526] px-2.5 py-1 rounded-md border border-[#333]">
                                    <Star className="w-4 h-4 text-yellow-500" /> {p.rating}
                                  </span>
                                  <span className="flex items-center gap-1.5 text-gray-300 bg-[#252526] px-2.5 py-1 rounded-md border border-[#333]">
                                    <Clock className="w-4 h-4 text-emerald-500" /> {p.availability_status}
                                  </span>
                                </div>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    )}

                  </div>

                  {msg.role === 'user' && (
                    <div className="w-10 h-10 rounded-full flex-shrink-0 flex items-center justify-center bg-gray-700 text-white mt-1">
                      <User className="w-5 h-5" />
                    </div>
                  )}
                </motion.div>
              ))}
            </AnimatePresence>
            <div ref={messagesEndRef} />
          </div>
          )}

          {currentView === 'my-fixes' && (
            <div className="max-w-4xl mx-auto space-y-8 pb-32">
              <h2 className="text-3xl font-bold text-white mb-6">My Fixes</h2>
              <div className="flex gap-3 mb-6">
                <span className="bg-emerald-500/20 text-emerald-500 px-4 py-1.5 rounded-full text-sm font-medium border border-emerald-500/30 cursor-pointer">All</span>
                <span className="bg-[#252526] text-gray-400 px-4 py-1.5 rounded-full text-sm font-medium border border-[#333] cursor-pointer hover:bg-[#333]">Active</span>
                <span className="bg-[#252526] text-gray-400 px-4 py-1.5 rounded-full text-sm font-medium border border-[#333] cursor-pointer hover:bg-[#333]">Completed</span>
                <span className="bg-[#252526] text-gray-400 px-4 py-1.5 rounded-full text-sm font-medium border border-[#333] cursor-pointer hover:bg-[#333]">Cancelled</span>
              </div>
              
              <div className="space-y-4">
                {myRequests.length === 0 ? (
                  <div className="text-center py-10 text-gray-400 font-bold">No active fixes yet. Start a chat to request a service!</div>
                ) : (
                  myRequests.map((req) => (
                    <div key={req.id} className="bg-[#1e1e1e] border border-[#333] rounded-2xl p-5 relative overflow-hidden">
                      <div className={`absolute top-5 right-5 text-xs font-bold px-3 py-1 rounded-full border ${
                        req.status === 'pending' ? 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20' :
                        req.status === 'accepted' ? 'bg-emerald-500/10 text-emerald-500 border-emerald-500/20' :
                        'bg-red-500/10 text-red-500 border-red-500/20'
                      }`}>
                        {req.status === 'pending' ? 'Pending' : req.status === 'accepted' ? 'Accepted' : 'Declined'}
                      </div>
                      <div className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">
                        {req.service?.category?.replace(/_/g, ' ') || 'General Repair'}
                      </div>
                      <h3 className="text-xl font-bold text-white mb-1">
                        {req.problem?.issue_summary || 'Service Request'}
                      </h3>
                      <p className="text-sm text-gray-400 mb-6">
                        Provider: {req.provider_id} · Request ID: {req.id.substring(0, 8)}
                      </p>
                      
                      <div className="relative flex justify-between items-center w-full">
                        <div className="absolute left-0 right-0 h-1 bg-[#333] top-3 -z-10"></div>
                        <div className={`absolute left-0 h-1 top-3 -z-10 transition-all duration-500 ${
                          req.status === 'declined' ? 'bg-red-500 w-[25%]' :
                          req.status === 'accepted' ? 'bg-emerald-500 w-[75%]' : 
                          'bg-emerald-500 w-[25%]'
                        }`}></div>
                        
                        <div className="flex flex-col items-center gap-2">
                          <div className="w-7 h-7 rounded-full bg-emerald-500 text-white flex items-center justify-center"><Check className="w-4 h-4"/></div>
                          <span className="text-xs font-medium text-emerald-500">Diagnosed</span>
                        </div>
                        <div className="flex flex-col items-center gap-2">
                          <div className="w-7 h-7 rounded-full bg-emerald-500 text-white flex items-center justify-center"><Check className="w-4 h-4"/></div>
                          <span className="text-xs font-medium text-emerald-500">Matched</span>
                        </div>
                        <div className="flex flex-col items-center gap-2">
                          <div className={`w-7 h-7 rounded-full border-2 flex items-center justify-center ${
                            req.status === 'accepted' ? 'bg-emerald-500 text-white border-emerald-500' :
                            req.status === 'declined' ? 'bg-red-500 text-white border-red-500' :
                            'bg-[#1e1e1e] border-emerald-500 text-emerald-500'
                          }`}>
                            {req.status === 'accepted' ? <Check className="w-4 h-4"/> : req.status === 'declined' ? <X className="w-4 h-4"/> : '3'}
                          </div>
                          <span className={`text-xs font-medium ${req.status === 'declined' ? 'text-red-500' : 'text-emerald-500'}`}>
                            {req.status === 'declined' ? 'Declined' : 'Accepted'}
                          </span>
                        </div>
                        <div className="flex flex-col items-center gap-2">
                          <div className="w-7 h-7 rounded-full bg-[#333] border-2 border-[#404040] text-gray-500 flex items-center justify-center">4</div>
                          <span className="text-xs font-medium text-gray-500">Done</span>
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}

          {currentView === 'saved-providers' && (
            <div className="max-w-4xl mx-auto space-y-8 pb-32">
              <h2 className="text-3xl font-bold text-white mb-6">Saved Providers</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-[#1e1e1e] border border-[#333] rounded-2xl p-5 hover:border-emerald-500/50 transition-colors">
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h3 className="font-bold text-white text-lg flex items-center gap-2">CoolCare AC Services <CheckCircle2 className="w-4 h-4 text-emerald-500" /></h3>
                      <p className="text-sm text-gray-400 font-medium mt-1">AC Repair · Gas Filling · Servicing</p>
                    </div>
                    <button className="text-emerald-500 hover:text-emerald-400 p-1"><Bookmark className="w-5 h-5 fill-current" /></button>
                  </div>
                  <div className="flex flex-wrap gap-3 text-sm mt-4">
                    <span className="flex items-center gap-1.5 text-gray-300 bg-[#252526] px-2.5 py-1 rounded-md border border-[#333]"><Star className="w-4 h-4 text-yellow-500" /> 4.8</span>
                    <span className="flex items-center gap-1.5 text-gray-300 bg-[#252526] px-2.5 py-1 rounded-md border border-[#333]"><MapPin className="w-4 h-4 text-gray-500" /> 2.1km</span>
                  </div>
                </div>

                <div className="bg-[#1e1e1e] border border-[#333] rounded-2xl p-5 hover:border-emerald-500/50 transition-colors">
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h3 className="font-bold text-white text-lg flex items-center gap-2">QuickFix Plumbing</h3>
                      <p className="text-sm text-gray-400 font-medium mt-1">Pipe Leaks · Drain Blockage</p>
                    </div>
                    <button className="text-emerald-500 hover:text-emerald-400 p-1"><Bookmark className="w-5 h-5 fill-current" /></button>
                  </div>
                  <div className="flex flex-wrap gap-3 text-sm mt-4">
                    <span className="flex items-center gap-1.5 text-gray-300 bg-[#252526] px-2.5 py-1 rounded-md border border-[#333]"><Star className="w-4 h-4 text-yellow-500" /> 4.5</span>
                    <span className="flex items-center gap-1.5 text-gray-300 bg-[#252526] px-2.5 py-1 rounded-md border border-[#333]"><MapPin className="w-4 h-4 text-gray-500" /> 3.5km</span>
                  </div>
                </div>

                <div className="bg-[#1e1e1e] border border-[#333] rounded-2xl p-5 hover:border-emerald-500/50 transition-colors">
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h3 className="font-bold text-white text-lg flex items-center gap-2">Spark Electricals <CheckCircle2 className="w-4 h-4 text-emerald-500" /></h3>
                      <p className="text-sm text-gray-400 font-medium mt-1">Wiring · Switch Repair · Appliance Install</p>
                    </div>
                    <button className="text-emerald-500 hover:text-emerald-400 p-1"><Bookmark className="w-5 h-5 fill-current" /></button>
                  </div>
                  <div className="flex flex-wrap gap-3 text-sm mt-4">
                    <span className="flex items-center gap-1.5 text-gray-300 bg-[#252526] px-2.5 py-1 rounded-md border border-[#333]"><Star className="w-4 h-4 text-yellow-500" /> 4.9</span>
                    <span className="flex items-center gap-1.5 text-gray-300 bg-[#252526] px-2.5 py-1 rounded-md border border-[#333]"><MapPin className="w-4 h-4 text-gray-500" /> 1.8km</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </main>

        {currentView === 'chat' && (
        <div className="bg-[#252526] border-t border-[#333] p-4 flex-shrink-0 z-10">
          <div className="max-w-4xl mx-auto">
            <AnimatePresence>
              {imageUrl && (
                <motion.div 
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, height: 0 }}
                  className="mb-4 relative inline-block"
                >
                  <div className="w-20 h-20 rounded-lg overflow-hidden border-2 border-[#404040]">
                    <img src={imageUrl} alt="Preview" className="w-full h-full object-cover" />
                  </div>
                  <button 
                    onClick={() => setImageUrl(null)}
                    className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 shadow hover:bg-red-600"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </motion.div>
              )}
              {audioUrl && (
                <motion.div 
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, height: 0 }}
                  className="mb-4 relative inline-flex items-center gap-2 bg-[#2d2d2d] border border-[#404040] rounded-lg p-3 max-w-sm"
                >
                  <div className="w-3 h-3 bg-emerald-500 rounded-full animate-pulse"></div>
                  <span className="text-sm font-medium text-gray-300">Voice message recorded</span>
                  <button 
                    onClick={() => setAudioUrl(null)}
                    className="ml-auto bg-red-500/20 text-red-500 hover:bg-red-500/30 rounded-full p-1 transition-colors"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </motion.div>
              )}
            </AnimatePresence>

            <form onSubmit={handleSubmit} className="relative bg-[#1e1e1e] border border-[#404040] rounded-2xl shadow-sm focus-within:border-emerald-500/50 transition-colors flex items-end p-2 overflow-hidden">
              <label className="p-3 text-gray-400 hover:text-white cursor-pointer transition-colors flex-shrink-0">
                <ImageIcon className="w-6 h-6" />
                <input type="file" accept="image/*" className="hidden" onChange={handleFileChange} disabled={isProcessing} />
              </label>
              <button 
                type="button" 
                className={`p-3 transition-colors flex-shrink-0 cursor-pointer ${isRecording ? 'text-red-500 animate-pulse' : 'text-gray-400 hover:text-white'}`}
                onClick={() => {
                  if (isRecording) {
                    recognitionRef.current?.stop();
                    setIsRecording(false);
                  } else {
                    if (recognitionRef.current) {
                      try {
                        recognitionRef.current.start();
                        setIsRecording(true);
                      } catch (e) {
                        console.error(e);
                      }
                    } else {
                      alert("Speech recognition is not supported in this browser. Try Chrome.");
                    }
                  }
                }}
                disabled={isProcessing}
              >
                <Mic className="w-6 h-6" />
              </button>
              
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Describe your problem (e.g. My AC is leaking water)..."
                disabled={isProcessing}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSubmit(e);
                  }
                }}
                className="flex-1 bg-transparent text-white placeholder:text-gray-500 resize-none outline-none py-3 px-2 max-h-32 min-h-[44px]"
                rows={1}
              />

              <button 
                type="submit"
                disabled={(!inputText.trim() && !imageUrl && !audioUrl) || isProcessing || isRecording}
                className="p-3 m-1 bg-emerald-600 text-white rounded-xl hover:bg-emerald-500 disabled:opacity-50 disabled:bg-gray-600 transition-colors flex-shrink-0"
              >
                <Send className="w-5 h-5" />
              </button>
            </form>
            <div className="text-center mt-2 text-[11px] text-gray-500 font-medium">
              FixFind AI can make mistakes. Always verify provider details.
            </div>
          </div>
        </div>
        )}

        <AnimatePresence>
          {showMap && latestProviders.length > 0 && (
            <ProviderMap 
              providers={latestProviders} 
              onClose={() => setShowMap(false)} 
              problem={latestProblem}
              service={latestService}
              customerLocation={{ lat: 17.3850, lng: 78.4867 }}
            />
          )}
        </AnimatePresence>

      </div>
    </div>
  );
}
