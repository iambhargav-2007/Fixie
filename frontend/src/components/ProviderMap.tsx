"use client";

import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap, Polyline } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { ProviderResponse, api } from "@/lib/api";
import { CheckCircle2, Star, Clock, X, Navigation } from "lucide-react";

// Fix for default Leaflet icon issues in Next.js
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

// Custom icons
const goldIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-gold.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const redIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const blueIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const MapBounds = ({ providers, customerLocation }: { providers: ProviderResponse[], customerLocation?: {lat: number, lng: number} }) => {
  const map = useMap();
  useEffect(() => {
    if (providers.length > 0) {
      const bounds = L.latLngBounds(providers.map(p => [p.location.lat, p.location.lng]));
      if (customerLocation) {
        bounds.extend([customerLocation.lat, customerLocation.lng]);
      }
      map.fitBounds(bounds, { padding: [50, 50] });
    }
  }, [providers, customerLocation, map]);
  return null;
};

export default function ProviderMap({ 
  providers, 
  onClose,
  problem,
  service,
  customerLocation
}: { 
  providers: ProviderResponse[];
  onClose: () => void;
  problem: any;
  service: any;
  customerLocation?: {lat: number, lng: number};
}) {
  // Ensure we get the provider with the highest fit score as top
  const topProvider = providers.length > 0 
    ? providers.reduce((prev, current) => (prev.fit_score > current.fit_score) ? prev : current)
    : null;
  const topProviderId = topProvider?.id;

  const [selectedProvider, setSelectedProvider] = useState<ProviderResponse | null>(null);
  const [requestStatus, setRequestStatus] = useState<"idle" | "requesting" | "success" | "error">("idle");

  const handleRequest = async () => {
    if (!selectedProvider) return;
    setRequestStatus("requesting");
    try {
      await api.createRequest(selectedProvider.id, problem, service, { lat: 17.3850, lng: 78.4867 });
      setRequestStatus("success");
      setTimeout(() => {
        setSelectedProvider(null);
        setRequestStatus("idle");
      }, 2000);
    } catch (e) {
      setRequestStatus("error");
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 md:p-8">
      <div className="bg-[#1e1e1e] border border-[#333] rounded-3xl overflow-hidden w-full max-w-5xl h-[80vh] flex flex-col shadow-2xl relative">
        
        {/* Header */}
        <div className="flex justify-between items-center p-6 border-b border-[#333] bg-[#252526] z-10 relative">
          <h2 className="text-xl font-bold text-white flex items-center gap-3">
            <Navigation className="w-6 h-6 text-emerald-500" />
            Service Provider Map
          </h2>
          <button onClick={onClose} className="p-2 hover:bg-[#333] rounded-full text-gray-400 hover:text-white transition-colors">
            <X className="w-6 h-6" />
          </button>
        </div>
        
        {/* Leaflet Map */}
        <div className="flex-1 relative bg-gray-900">
          <MapContainer 
            center={[17.3850, 78.4867]} 
            zoom={12} 
            style={{ height: '100%', width: '100%', zIndex: 0 }}
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <MapBounds providers={providers} customerLocation={customerLocation} />
            
            {/* Customer Location */}
            {customerLocation && (
              <Marker position={[customerLocation.lat, customerLocation.lng]} icon={blueIcon}>
                <Popup className="custom-popup">
                  <div className="font-bold text-base">Your Location</div>
                  <div className="text-sm text-gray-600">Hyderabad</div>
                </Popup>
              </Marker>
            )}

            {/* Polyline to Top Provider */}
            {customerLocation && topProvider && (
              <Polyline 
                positions={[
                  [customerLocation.lat, customerLocation.lng],
                  [topProvider.location.lat, topProvider.location.lng]
                ]} 
                color="#10b981" 
                weight={3} 
                dashArray="5, 10" 
                opacity={0.7} 
              />
            )}
            
            {providers.map((p, idx) => {
              const isTop = p.id === topProviderId;
              return (
                <Marker 
                  key={p.id} 
                  position={[p.location.lat, p.location.lng]}
                  icon={isTop ? goldIcon : redIcon}
                  eventHandlers={{
                    click: () => setSelectedProvider(p)
                  }}
                >
                  <Popup className="custom-popup">
                    <div className="font-sans">
                      <div className="font-bold text-base flex items-center gap-1 mb-1">
                        {p.name} {p.verified && <CheckCircle2 className="w-4 h-4 text-emerald-500" />}
                      </div>
                      <div className="text-sm text-gray-600 mb-2">{p.specializations.join(" · ")}</div>
                      <div className="flex gap-3 text-sm font-medium">
                        <span className="flex items-center gap-1"><Star className="w-3.5 h-3.5 text-yellow-500" /> {p.rating}</span>
                        <span className="flex items-center gap-1">{p.distance_km}km</span>
                      </div>
                      <button 
                        onClick={() => setSelectedProvider(p)}
                        className="mt-3 w-full bg-emerald-600 text-white font-bold py-1.5 rounded-lg text-sm hover:bg-emerald-700"
                      >
                        View Details
                      </button>
                    </div>
                  </Popup>
                </Marker>
              )
            })}
          </MapContainer>
        </div>

        {/* Request Dialog Modal (Overlay within the Map Modal) */}
        {selectedProvider && (
          <div className="absolute inset-0 z-20 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
            <div className="bg-[#252526] border border-[#404040] p-6 rounded-2xl w-full max-w-sm shadow-2xl">
              <h3 className="text-xl font-bold text-white mb-2">{selectedProvider.name}</h3>
              <p className="text-gray-400 text-sm mb-6">You are about to request a service from this provider. The provider will be notified on their dashboard.</p>
              
              {requestStatus === "error" && (
                <div className="mb-4 text-red-500 text-sm font-bold bg-red-500/10 p-2 rounded">Failed to send request.</div>
              )}
              {requestStatus === "success" && (
                <div className="mb-4 text-emerald-500 text-sm font-bold bg-emerald-500/10 p-2 rounded flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4" /> Request sent successfully!
                </div>
              )}

              <div className="flex justify-end gap-3">
                <button 
                  onClick={() => setSelectedProvider(null)}
                  disabled={requestStatus === "requesting" || requestStatus === "success"}
                  className="px-4 py-2 text-sm font-bold text-gray-300 hover:text-white transition-colors"
                >
                  Cancel
                </button>
                <button 
                  onClick={handleRequest}
                  disabled={requestStatus === "requesting" || requestStatus === "success"}
                  className="px-4 py-2 text-sm font-bold bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl transition-colors flex items-center justify-center min-w-[100px]"
                >
                  {requestStatus === "requesting" ? "Sending..." : "Request"}
                </button>
              </div>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
