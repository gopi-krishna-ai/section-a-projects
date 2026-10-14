import React, { useState, useEffect } from 'react';
import api from '../../api';

export default function OwnerDashboard() {
  const [items, setItems] = useState([]);
  const [rentals, setRentals] = useState([]);
  
  // Add item state
  const [showAddForm, setShowAddForm] = useState(false);
  const [newItem, setNewItem] = useState({ name: '', category: 'Furniture', condition: 'Good', description: '', price_per_day: '', location: '', image_url: '' });
  const [priceSuggestion, setPriceSuggestion] = useState(null);

  async function fetchItems() {
    const res = await api.get('/items/owner');
    setItems(res.data);
  }

  async function fetchRentals() {
    const res = await api.get('/rentals/my-requests');
    setRentals(res.data);
  }

  useEffect(() => {
    fetchItems();
    fetchRentals();
  }, []);

  const handleStatusUpdate = async (id, status) => {
    await api.put(`/rentals/${id}/status`, { status });
    fetchRentals();
  };

  const getPriceSuggestion = async () => {
    if(!newItem.name) return;
    try {
      const res = await api.post('/items/ai/price-suggest', {
        category: newItem.category, name: newItem.name, condition: newItem.condition
      });
      setPriceSuggestion(res.data);
      if(!newItem.price_per_day) {
        setNewItem({...newItem, price_per_day: res.data.suggested_price});
      }
    } catch(err) {
      console.error(err);
    }
  };

  const handleAddItem = async (e) => {
    e.preventDefault();
    await api.post('/items/', newItem);
    setShowAddForm(false);
    fetchItems();
    setNewItem({ name: '', category: 'Furniture', condition: 'Good', description: '', price_per_day: '', location: '', image_url: '' });
    setPriceSuggestion(null);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Owner Dashboard</h1>
        <button onClick={() => setShowAddForm(!showAddForm)} className="px-6 py-2 bg-rentmate-green text-white font-bold rounded-lg hover:bg-emerald-600">
          {showAddForm ? 'Cancel' : '+ List an Item'}
        </button>
      </div>

      {showAddForm && (
        <div className="bg-white p-6 rounded-xl shadow-sm border mb-8">
          <h2 className="text-xl font-bold mb-4">List a New Item</h2>
          <form onSubmit={handleAddItem} className="space-y-4">
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Item Name</label>
                <input required type="text" value={newItem.name} onChange={e => setNewItem({...newItem, name: e.target.value})} onBlur={getPriceSuggestion} className="w-full border rounded-lg p-2" />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Category</label>
                <select value={newItem.category} onChange={e => {setNewItem({...newItem, category: e.target.value}); getPriceSuggestion();}} className="w-full border rounded-lg p-2">
                  <option>Furniture</option><option>Electronics</option><option>Home Appliances</option><option>Kitchen</option><option>Tools</option><option>Outdoor</option><option>Moving</option>
                </select>
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium mb-1">Description</label>
                <textarea required value={newItem.description} onChange={e => setNewItem({...newItem, description: e.target.value})} className="w-full border rounded-lg p-2 h-24"></textarea>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Price Per Day (₹)</label>
                <input required type="number" value={newItem.price_per_day} onChange={e => setNewItem({...newItem, price_per_day: e.target.value})} className="w-full border rounded-lg p-2" />
                {priceSuggestion && (
                  <p className="text-xs text-emerald-600 mt-1">Suggested: ₹{priceSuggestion.suggested_price} ({priceSuggestion.message})</p>
                )}
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Image URL</label>
                <input type="url" value={newItem.image_url} onChange={e => setNewItem({...newItem, image_url: e.target.value})} placeholder="https://example.com/image.jpg" className="w-full border rounded-lg p-2" />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Location</label>
                <input required type="text" value={newItem.location} onChange={e => setNewItem({...newItem, location: e.target.value})} className="w-full border rounded-lg p-2" />
              </div>
            </div>
            <button type="submit" className="px-6 py-2 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700">Submit Listing</button>
          </form>
        </div>
      )}

      <div className="grid md:grid-cols-2 gap-8">
        <div>
          <h2 className="text-2xl font-bold mb-4">My Listings</h2>
          <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
            <ul className="divide-y">
              {items.map(item => (
                <li key={item.id} className="p-4 flex justify-between items-center">
                  <div>
                    <p className="font-bold">{item.name}</p>
                    <p className="text-sm text-gray-500">₹{item.price_per_day}/day • {item.category}</p>
                  </div>
                  <span className={`px-2 py-1 text-xs font-bold rounded ${item.status === 'APPROVED' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>{item.status}</span>
                </li>
              ))}
              {items.length === 0 && <li className="p-4 text-gray-500 text-center">No items listed yet.</li>}
            </ul>
          </div>
        </div>

        <div>
          <h2 className="text-2xl font-bold mb-4">Rental Requests</h2>
          <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
            <ul className="divide-y">
              {rentals.map(r => (
                <li key={r.id} className="p-4">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <p className="font-bold">{r.item_name}</p>
                      <p className="text-sm text-gray-500">Requested by: {r.other_party_name}</p>
                      <p className="text-sm text-gray-500">{new Date(r.start_date).toLocaleDateString()} - {new Date(r.end_date).toLocaleDateString()}</p>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-lg">₹{r.total_amount}</p>
                      <span className="text-xs font-bold text-gray-500 uppercase">{r.status}</span>
                    </div>
                  </div>
                  {r.status === 'PENDING' && (
                    <div className="flex gap-2 mt-3">
                      <button onClick={() => handleStatusUpdate(r.id, 'APPROVED')} className="flex-1 py-1 bg-green-100 text-green-800 font-bold rounded hover:bg-green-200">Approve</button>
                      <button onClick={() => handleStatusUpdate(r.id, 'REJECTED')} className="flex-1 py-1 bg-red-100 text-red-800 font-bold rounded hover:bg-red-200">Reject</button>
                    </div>
                  )}
                  {r.status === 'APPROVED' && (
                    <button onClick={() => handleStatusUpdate(r.id, 'ACTIVE')} className="w-full mt-3 py-1 bg-blue-100 text-blue-800 font-bold rounded hover:bg-blue-200">Mark as Active (Picked Up)</button>
                  )}
                  {r.status === 'ACTIVE' && (
                    <button onClick={() => handleStatusUpdate(r.id, 'COMPLETED')} className="w-full mt-3 py-1 bg-gray-100 text-gray-800 font-bold rounded hover:bg-gray-200">Mark as Completed (Returned)</button>
                  )}
                </li>
              ))}
              {rentals.length === 0 && <li className="p-4 text-gray-500 text-center">No rental requests.</li>}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
