import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import api from '../../api';

// Fix leaflet default icon issue
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

// Custom icons
const ownerIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const renterIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

export default function DeliveryDashboard() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  // Center of India roughly
  const center = [20.5937, 78.9629];

  async function fetchTasks() {
    try {
      const res = await api.get('/delivery/tasks');
      setTasks(res.data);
      setLoading(false);
    } catch (error) {
      console.error("Failed to fetch delivery tasks", error);
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchTasks();
  }, []);

  const acceptTask = async (taskId) => {
    try {
      await api.post(`/delivery/accept/${taskId}`);
      fetchTasks();
    } catch (err) {
      alert(err.response?.data?.message || 'Failed to accept task');
    }
  };

  const updateStatus = async (taskId, status) => {
    try {
      await api.post(`/delivery/update/${taskId}`, { status });
      fetchTasks();
    } catch (err) {
      alert(err.response?.data?.message || 'Failed to update status');
    }
  };

  if (loading) return <div className="p-8 text-center">Loading delivery tasks...</div>;

  return (
    <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Delivery Dashboard</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Map View */}
        <div className="lg:col-span-2 bg-white rounded-lg shadow-sm overflow-hidden h-[600px] border border-gray-200">
          <MapContainer center={center} zoom={5} style={{ height: '100%', width: '100%' }}>
            <TileLayer
              attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            
            {tasks.map((task) => {
              if (!task.owner.lat || !task.renter.lat) return null;
              
              const ownerPos = [task.owner.lat, task.owner.lng];
              const renterPos = [task.renter.lat, task.renter.lng];
              
              return (
                <React.Fragment key={task.id}>
                  {/* Owner Marker */}
                  <Marker position={ownerPos} icon={ownerIcon}>
                    <Popup>
                      <div className="text-sm">
                        <strong className="block mb-1">Pick up: {task.item_name}</strong>
                        Owner: {task.owner.name}<br/>
                        Phone: {task.owner.phone || 'N/A'}<br/>
                        Location: {task.owner.location}
                      </div>
                    </Popup>
                  </Marker>
                  
                  {/* Renter Marker */}
                  <Marker position={renterPos} icon={renterIcon}>
                    <Popup>
                      <div className="text-sm">
                        <strong className="block mb-1">Deliver: {task.item_name}</strong>
                        Renter: {task.renter.name}<br/>
                        Phone: {task.renter.phone || 'N/A'}<br/>
                        Location: {task.renter.location}
                      </div>
                    </Popup>
                  </Marker>
                  
                  {/* Line between Pick up and Delivery */}
                  <Polyline positions={[ownerPos, renterPos]} color={task.delivery_guy_id ? '#10b981' : '#6b7280'} dashArray="5, 10" />
                </React.Fragment>
              )
            })}
          </MapContainer>
        </div>

        {/* Task List Sidebar */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 h-[600px] overflow-y-auto">
          <h2 className="text-xl font-semibold mb-4">Available & Active Tasks</h2>
          
          {tasks.length === 0 ? (
            <p className="text-gray-500 text-sm">No tasks available right now.</p>
          ) : (
            <div className="space-y-4">
              {tasks.map(task => (
                <div key={task.id} className={`border rounded-lg p-4 ${task.delivery_guy_id ? 'border-green-300 bg-green-50' : 'border-gray-200 bg-white'}`}>
                  <div className="flex items-center mb-2">
                    <img src={task.item_image} alt={task.item_name} className="w-12 h-12 rounded object-cover mr-3" />
                    <div>
                      <h3 className="font-semibold text-gray-900">{task.item_name}</h3>
                      <p className="text-xs text-gray-500">Task #{task.id}</p>
                    </div>
                  </div>
                  
                  <div className="text-sm text-gray-600 mb-4 space-y-1">
                    <p><span className="font-medium text-blue-600">Pick up:</span> {task.owner.location}</p>
                    <p><span className="font-medium text-green-600">Drop off:</span> {task.renter.location}</p>
                    <p>Status: <span className="font-semibold">{task.delivery_status.replace('_', ' ')}</span></p>
                  </div>
                  
                  {!task.delivery_guy_id ? (
                    <button 
                      onClick={() => acceptTask(task.id)}
                      className="w-full bg-orange-500 hover:bg-orange-600 text-white font-medium py-2 px-4 rounded text-sm transition-colors"
                    >
                      Accept Order
                    </button>
                  ) : (
                    <div className="flex space-x-2">
                      {task.delivery_status === 'PENDING_PICKUP' && (
                        <button 
                          onClick={() => updateStatus(task.id, 'IN_TRANSIT')}
                          className="flex-1 bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-2 rounded text-sm transition-colors"
                        >
                          Pick Up from Owner
                        </button>
                      )}
                      {task.delivery_status === 'IN_TRANSIT' && (
                        <button 
                          onClick={() => updateStatus(task.id, 'DELIVERED')}
                          className="flex-1 bg-green-500 hover:bg-green-600 text-white font-medium py-2 px-2 rounded text-sm transition-colors"
                        >
                          Deliver to Renter
                        </button>
                      )}
                      {task.delivery_status === 'DELIVERED' && (
                        <span className="w-full text-center bg-gray-100 text-gray-800 font-medium py-2 px-4 rounded text-sm">
                          Completed
                        </span>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
        
      </div>
    </div>
  );
}
