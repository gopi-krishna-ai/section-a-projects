import React, { useState, useEffect } from 'react';
import api from '../../api';
import { Search, Loader2, Calendar, IndianRupee } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function RenterDashboard() {
  const [query, setQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [loadingText, setLoadingText] = useState('');
  const [results, setResults] = useState([]);
  const [rentals, setRentals] = useState([]);

  async function fetchRentals() {
    try {
      const res = await api.get('/rentals/my-requests');
      setRentals(res.data);
    } catch (err) {
      console.error("Failed to fetch rentals", err);
    }
  }

  useEffect(() => {
    fetchRentals();
  }, []);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query) return;
    
    setIsSearching(true);
    setResults([]);
    
    // Fake loading states for UI feedback
    setLoadingText('Understanding your requirement...');
    await new Promise(r => setTimeout(r, 800));
    setLoadingText('Finding suitable categories...');
    await new Promise(r => setTimeout(r, 800));
    setLoadingText('Ranking rental options...');
    
    try {
      const res = await api.post('/items/ai/match', { query });
      setResults(res.data.matches);
    } catch (err) {
      console.error(err);
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Renter Dashboard</h1>
      
      {/* AI Search Section */}
      <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 mb-12">
        <h2 className="text-2xl font-bold mb-2">Describe what you need</h2>
        <p className="text-gray-600 mb-6">Our AI will find the best items for your requirement.</p>
        
        <form onSubmit={handleSearch} className="flex gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-4 top-4 text-gray-400 h-6 w-6" />
            <input 
              type="text" 
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g., I am organizing a small birthday party for 30 people this weekend."
              className="w-full pl-14 pr-4 py-4 text-lg border border-gray-300 rounded-xl focus:ring-2 focus:ring-rentmate-green focus:border-rentmate-green"
            />
          </div>
          <button 
            disabled={isSearching}
            className="px-8 py-4 bg-rentmate-green text-white font-bold rounded-xl hover:bg-emerald-600 disabled:opacity-50 flex items-center gap-2"
          >
            {isSearching ? <Loader2 className="animate-spin h-6 w-6" /> : "Find What I Need"}
          </button>
        </form>

        {isSearching && (
          <div className="mt-8 text-center text-gray-500 animate-pulse">
            {loadingText}
          </div>
        )}

        {results.length > 0 && (
          <div className="mt-10">
            <h3 className="text-xl font-bold mb-6">Based on your requirement, we recommend:</h3>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {results.map((match, idx) => (
                <Link to={`/items/${match.item.id}`} key={idx} className="block bg-white border rounded-xl overflow-hidden hover:shadow-lg transition-shadow">
                  {match.item.image_url && (
                    <div className="h-48 w-full bg-gray-100 overflow-hidden">
                      <img src={match.item.image_url} alt={match.item.name} className="w-full h-full object-cover" />
                    </div>
                  )}
                  <div className="p-6">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h4 className="text-xl font-bold text-gray-900">{match.item.name}</h4>
                        <p className="text-sm text-gray-500">{match.item.category}</p>
                      </div>
                      <div className="bg-green-100 text-green-800 text-xs font-bold px-3 py-1 rounded-full">
                        {match.match_score}% Match
                      </div>
                    </div>
                    <div className="text-2xl font-bold text-gray-900 mb-4">
                      ₹{match.item.price_per_day} <span className="text-sm font-normal text-gray-500">/day</span>
                    </div>
                    <div className="bg-gray-50 p-3 rounded-lg text-sm text-gray-600">
                      <strong>Why this matched?</strong>
                      <ul className="list-disc pl-4 mt-1">
                        {match.reasons.map((r, i) => <li key={i}>{r}</li>)}
                      </ul>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Rentals Section */}
      <div>
        <h2 className="text-2xl font-bold mb-6">My Rentals</h2>
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <table className="w-full text-left">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="px-6 py-4 font-medium text-gray-500">Item</th>
                <th className="px-6 py-4 font-medium text-gray-500">Owner</th>
                <th className="px-6 py-4 font-medium text-gray-500">Dates</th>
                <th className="px-6 py-4 font-medium text-gray-500">Total</th>
                <th className="px-6 py-4 font-medium text-gray-500">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {rentals.map(r => (
                <tr key={r.id}>
                  <td className="px-6 py-4 font-medium text-gray-900">{r.item_name}</td>
                  <td className="px-6 py-4 text-gray-500">{r.other_party_name}</td>
                  <td className="px-6 py-4 text-gray-500">{new Date(r.start_date).toLocaleDateString()} - {new Date(r.end_date).toLocaleDateString()}</td>
                  <td className="px-6 py-4 font-medium">₹{r.total_amount}</td>
                  <td className="px-6 py-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                      r.status === 'APPROVED' ? 'bg-blue-100 text-blue-800' :
                      r.status === 'ACTIVE' ? 'bg-green-100 text-green-800' :
                      r.status === 'COMPLETED' ? 'bg-gray-100 text-gray-800' :
                      'bg-yellow-100 text-yellow-800'
                    }`}>
                      {r.status}
                    </span>
                  </td>
                </tr>
              ))}
              {rentals.length === 0 && (
                <tr>
                  <td colSpan="5" className="px-6 py-8 text-center text-gray-500">No rental history yet.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
