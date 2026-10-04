const API_BASE = "http://localhost:8000/api";

export interface LocationInput {
  lat: number;
  lng: number;
  locality?: string;
}

export interface ProviderResponse {
  id: string;
  name: string;
  services: string[];
  specializations: string[];
  distance_km: number;
  rating: number;
  price_min: number;
  price_max: number;
  availability_status: string;
  availability_slots: string[];
  verified: boolean;
  fit_score: number;
  score_breakdown: Record<string, number>;
  location: {
    lat: number;
    lng: number;
  };
}

export interface ChatResponse {
  session_id: string;
  workflow_status: string;
  message: string;
  clarification_question?: string;
  clarification_reasoning?: string;
  problem?: any;
  service?: {
    category: string;
    service: string;
    specialization: string;
  };
  providers: ProviderResponse[];
  recommendation?: any;
}

export const api = {
  chat: async (sessionId: string, text: string, location?: LocationInput, imageUrl?: string, audioUrl?: string): Promise<ChatResponse> => {
    const res = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: sessionId,
        text,
        location,
        image_url: imageUrl,
        audio_url: audioUrl,
      }),
    });
    if (!res.ok) throw new Error("Failed to communicate with chat API");
    return res.json();
  },
  
  createRequest: async (providerId: string, problem: any, service: any, location: any): Promise<any> => {
    const res = await fetch(`${API_BASE}/requests`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        provider_id: providerId,
        problem,
        service,
        location,
      }),
    });
    if (!res.ok) throw new Error("Failed to create request");
    return res.json();
  },

  getRequest: async (requestId: string): Promise<any> => {
    const res = await fetch(`${API_BASE}/requests/${requestId}`, { cache: 'no-store' });
    if (!res.ok) throw new Error("Failed to get request status");
    return res.json();
  },

  listRequests: async (): Promise<any[]> => {
    const res = await fetch(`${API_BASE}/requests`, { cache: 'no-store' });
    if (!res.ok) throw new Error("Failed to list requests");
    return res.json();
  },

  updateRequestStatus: async (requestId: string, status: string): Promise<any> => {
    const res = await fetch(`${API_BASE}/requests/${requestId}/status`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status }),
    });
    if (!res.ok) throw new Error("Failed to update status");
    return res.json();
  }
};
