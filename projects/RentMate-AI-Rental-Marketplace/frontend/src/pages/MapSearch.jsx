import React from 'react';
import { Map as MapIcon, Search, MapPin, Filter } from 'lucide-react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';

// Fix for default marker icon in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const MOCK_ITEMS = [
  { id: 1, name: 'Power Drill', price: 15, lat: 37.7749, lng: -122.4194, dist: '1.2 miles' },
  { id: 2, name: 'Camping Tent', price: 25, lat: 37.7849, lng: -122.4094, dist: '2.5 miles' },
  { id: 3, name: 'Projector', price: 35, lat: 37.7649, lng: -122.4294, dist: '3.1 miles' }
];

export default function MapSearch() {
  const position = [37.7749, -122.4194]; // SF coordinates

  return (
    <div className="flex h-[calc(100vh-4rem)] bg-white/40 backdrop-blur-md">
      {/* Sidebar */}
      <div className="w-96 bg-white/90 border-r border-gray-200 p-4 flex flex-col gap-4 z-10 shadow-lg">
        <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
          <MapIcon className="w-5 h-5 text-rentmate-green" />
          Interactive Map
        </h2>
        
        <div className="relative">
          <Search className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
          <input 
            type="text" 
            placeholder="Search map area..." 
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-rentmate-green focus:border-transparent outline-none"
          />
        </div>
        
        <div className="flex gap-2">
          <button className="flex-1 flex items-center justify-center gap-2 bg-gray-100 py-2 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors">
            <Filter className="w-4 h-4" /> Filters
          </button>
          <button className="flex-1 flex items-center justify-center gap-2 bg-gray-100 py-2 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors">
            <MapPin className="w-4 h-4" /> Near Me
          </button>
        </div>

        <div className="flex-1 overflow-y-auto space-y-3 mt-2 pr-2">
          {MOCK_ITEMS.map(item => (
            <div key={item.id} className="p-3 border border-gray-100 rounded-xl bg-white shadow-sm hover:border-rentmate-green hover:shadow-md cursor-pointer transition-all group">
              <div className="w-full h-32 bg-gray-100 rounded-lg mb-3 flex items-center justify-center text-gray-400 overflow-hidden relative">
                <div className="absolute inset-0 bg-gradient-to-tr from-gray-200 to-gray-50 opacity-50 group-hover:scale-105 transition-transform duration-500"></div>
                <span className="relative z-10 font-medium">Image</span>
              </div>
              <div className="flex justify-between items-start">
                <h4 className="font-bold text-gray-900">{item.name}</h4>
                <span className="font-bold text-rentmate-green">${item.price}/day</span>
              </div>
              <p className="text-sm text-gray-500 flex items-center gap-1 mt-1">
                <MapPin className="w-3 h-3" /> {item.dist} away
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Map Area */}
      <div className="flex-1 relative z-0">
        <MapContainer center={position} zoom={13} style={{ height: '100%', width: '100%' }}>
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
          
          {MOCK_ITEMS.map(item => (
            <Marker key={item.id} position={[item.lat, item.lng]}>
              <Popup className="rounded-xl">
                <div className="font-bold text-gray-900">{item.name}</div>
                <div className="text-rentmate-green font-medium">${item.price}/day</div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
}
