import React, { useContext, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { Package, User, LogOut, Bell, CheckCircle } from 'lucide-react';

export default function Navbar() {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const [showNotifs, setShowNotifs] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const mockNotifs = [
    { id: 1, title: 'Payment Successful', desc: 'Your rental for Sony Alpha A7III was confirmed.', time: '2m ago', type: 'success' },
    { id: 2, title: 'Delivery Partner Assigned', desc: 'Speedy Delivery will pick up your item tomorrow.', time: '1h ago', type: 'info' },
    { id: 3, title: 'New Review', desc: 'Priya left you a 5-star review.', time: '2h ago', type: 'success' }
  ];

  return (
    <nav className="bg-white/80 backdrop-blur-md shadow-sm border-b border-gray-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center gap-2 group">
              <Package className="h-8 w-8 text-emerald-500 group-hover:scale-110 transition-transform" />
              <span className="font-bold text-2xl tracking-tight text-gray-900">RentMate</span>
            </Link>
          </div>
          
          <div className="flex items-center gap-6">
            <Link to="/map" className="text-gray-600 hover:text-emerald-600 font-medium text-sm flex items-center gap-1 transition-colors"><span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></span>Map</Link>
            <Link to="/how-ai-works" className="text-gray-600 hover:text-emerald-600 font-medium text-sm transition-colors">How AI Works</Link>
            
            {user ? (
              <>
                <Link to="/dashboard" className="text-gray-600 hover:text-emerald-600 font-medium text-sm transition-colors">Dashboard</Link>
                <Link to="/inbox" className="text-gray-600 hover:text-emerald-600 font-medium text-sm transition-colors">Inbox</Link>
                <Link to="/alerts" className="text-gray-600 hover:text-emerald-600 font-medium text-sm transition-colors">Alerts</Link>
                {user.role === 'OWNER' && <Link to="/wallet" className="text-gray-600 hover:text-emerald-600 font-medium text-sm transition-colors">Wallet</Link>}
                <Link to="/disputes" className="text-gray-600 hover:text-emerald-600 font-medium text-sm transition-colors">Support</Link>
                
                <div className="flex items-center gap-4 border-l border-gray-200 pl-6 ml-2 relative">
                  
                  {/* Notifications Bell */}
                  <div className="relative">
                    <button 
                      onClick={() => setShowNotifs(!showNotifs)} 
                      className="p-2 text-gray-500 hover:text-emerald-600 transition-colors relative focus:outline-none"
                    >
                      <Bell className="h-5 w-5" />
                      <span className="absolute top-1.5 right-1.5 flex h-2.5 w-2.5">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-red-500"></span>
                      </span>
                    </button>

                    {showNotifs && (
                      <div className="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-2xl border border-gray-100 overflow-hidden animate-in fade-in slide-in-from-top-2 duration-200">
                        <div className="px-4 py-3 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
                          <h3 className="font-bold text-gray-800 text-sm">Notifications</h3>
                          <span className="text-xs text-emerald-600 font-medium cursor-pointer hover:underline">Mark all as read</span>
                        </div>
                        <div className="max-h-80 overflow-y-auto">
                          {mockNotifs.map(n => (
                            <div key={n.id} className="p-4 border-b border-gray-50 hover:bg-gray-50 cursor-pointer transition-colors">
                              <div className="flex gap-3">
                                <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${n.type === 'success' ? 'bg-emerald-100 text-emerald-600' : 'bg-blue-100 text-blue-600'}`}>
                                  {n.type === 'success' ? <CheckCircle size={16} /> : <Bell size={16} />}
                                </div>
                                <div>
                                  <p className="text-sm font-semibold text-gray-800">{n.title}</p>
                                  <p className="text-xs text-gray-500 mt-0.5 line-clamp-2">{n.desc}</p>
                                  <p className="text-[10px] text-gray-400 mt-1">{n.time}</p>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                        <div className="p-2 text-center bg-gray-50 border-t border-gray-100 cursor-pointer hover:bg-gray-100">
                          <span className="text-xs font-medium text-gray-600">View all notifications</span>
                        </div>
                      </div>
                    )}
                  </div>

                  <Link to="/profile" className="text-sm text-right hidden md:block hover:opacity-75">
                    <p className="font-bold text-gray-900">{user.name}</p>
                    <p className="text-xs text-emerald-600 font-bold bg-emerald-50 px-2 py-0.5 rounded inline-block mt-0.5">{user.role}</p>
                  </Link>
                  <button onClick={handleLogout} className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-full transition-all">
                    <LogOut className="h-5 w-5" />
                  </button>
                </div>
              </>
            ) : (
              <div className="flex items-center gap-4">
                <Link to="/login" className="text-gray-600 hover:text-emerald-600 font-medium transition-colors">Sign In</Link>
                <Link to="/login" className="bg-gray-900 text-white px-5 py-2.5 rounded-xl hover:bg-gray-800 shadow-md hover:shadow-lg transition-all font-medium text-sm">Get Started</Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
