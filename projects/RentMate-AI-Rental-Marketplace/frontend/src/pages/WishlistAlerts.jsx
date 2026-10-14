import React from 'react';
import { BellRing, Heart, Plus } from 'lucide-react';

export default function WishlistAlerts() {
  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-10">
        <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
          <BellRing className="w-8 h-8 text-purple-500" /> Wishlist & AI Alerts
        </h1>
        <p className="text-gray-600 mt-2">Save items for later or set up AI agents to find specific rentals for you.</p>
      </div>

      <div className="grid md:grid-cols-2 gap-12">
        {/* Saved Items */}
        <div>
          <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
            <Heart className="w-5 h-5 text-rose-500 fill-rose-500" /> Saved Items
          </h2>
          <div className="space-y-4">
            {[1, 2].map(i => (
              <div key={i} className="flex gap-4 bg-white/80 backdrop-blur-md p-4 rounded-2xl border border-white/40 shadow-sm">
                <div className="w-24 h-24 bg-gray-200 rounded-xl"></div>
                <div className="flex-1">
                  <h3 className="font-bold text-gray-900">DJI Mavic Pro Drone</h3>
                  <p className="text-sm text-gray-500 mb-2">$45/day • 2.4 miles away</p>
                  <button className="text-sm font-medium text-rentmate-green hover:underline">View Listing</button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* AI Alerts */}
        <div>
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold flex items-center gap-2">
              <BellRing className="w-5 h-5 text-purple-500" /> Active AI Alerts
            </h2>
            <button className="flex items-center gap-1 text-sm font-medium text-purple-600 hover:text-purple-700 bg-purple-50 px-3 py-1 rounded-full">
              <Plus className="w-4 h-4" /> New Alert
            </button>
          </div>
          
          <div className="space-y-4">
            <div className="bg-white/80 backdrop-blur-md p-5 rounded-2xl border border-white/40 shadow-sm relative overflow-hidden">
              <div className="absolute left-0 top-0 bottom-0 w-1 bg-purple-500"></div>
              <h3 className="font-bold text-gray-900 mb-1">"DSLR Camera under $30/day"</h3>
              <p className="text-sm text-gray-500 mb-3">Looking in: San Francisco, CA • Any Weekend</p>
              <div className="flex justify-between items-center border-t border-gray-100 pt-3">
                <span className="text-xs font-bold text-green-500 bg-green-50 px-2 py-1 rounded-full">1 Match Found!</span>
                <button className="text-xs font-medium text-gray-500 hover:text-gray-900">Edit / Delete</button>
              </div>
            </div>

            <div className="bg-white/80 backdrop-blur-md p-5 rounded-2xl border border-white/40 shadow-sm relative overflow-hidden opacity-75">
              <div className="absolute left-0 top-0 bottom-0 w-1 bg-gray-300"></div>
              <h3 className="font-bold text-gray-900 mb-1">"Standup Paddleboard"</h3>
              <p className="text-sm text-gray-500 mb-3">Looking in: Lake Tahoe • Next Month</p>
              <div className="flex justify-between items-center border-t border-gray-100 pt-3">
                <span className="text-xs text-gray-400">Scanning marketplace continuously...</span>
                <button className="text-xs font-medium text-gray-500 hover:text-gray-900">Edit / Delete</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
