import React from 'react';
import { Star, ShieldCheck, MapPin, CalendarDays } from 'lucide-react';

export default function PublicProfile() {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="bg-white/80 backdrop-blur-md rounded-3xl shadow-sm border border-white/40 overflow-hidden">
        <div className="h-32 bg-gradient-to-r from-blue-400 to-emerald-400"></div>
        <div className="px-8 pb-8">
          <div className="flex justify-between items-end -mt-12 mb-6">
            <div className="w-24 h-24 bg-white rounded-full p-1 shadow-md">
              <div className="w-full h-full bg-gray-200 rounded-full flex items-center justify-center text-gray-500 text-3xl font-bold">
                JD
              </div>
            </div>
            <button className="px-6 py-2 bg-gray-900 text-white rounded-full font-medium hover:bg-gray-800">
              Contact User
            </button>
          </div>
          
          <div className="flex items-center gap-3 mb-2">
            <h1 className="text-3xl font-bold">John Doe</h1>
            <ShieldCheck className="text-blue-500 w-6 h-6" />
          </div>
          <p className="text-gray-500 flex items-center gap-2 mb-6">
            <MapPin className="w-4 h-4" /> San Francisco, CA • <CalendarDays className="w-4 h-4 ml-2" /> Joined 2026
          </p>

          <div className="grid grid-cols-3 gap-4 mb-8">
            <div className="bg-gray-50/50 p-4 rounded-2xl border">
              <div className="text-2xl font-bold flex items-center gap-1">4.9 <Star className="w-5 h-5 text-yellow-400 fill-yellow-400" /></div>
              <p className="text-sm text-gray-500">Trust Score</p>
            </div>
            <div className="bg-gray-50/50 p-4 rounded-2xl border">
              <div className="text-2xl font-bold">142</div>
              <p className="text-sm text-gray-500">Successful Rentals</p>
            </div>
            <div className="bg-gray-50/50 p-4 rounded-2xl border">
              <div className="text-2xl font-bold">100%</div>
              <p className="text-sm text-gray-500">Response Rate</p>
            </div>
          </div>

          <h3 className="font-bold text-lg mb-4">Recent Reviews</h3>
          <div className="space-y-4">
            {[1, 2].map((i) => (
              <div key={i} className="p-4 border rounded-2xl bg-white/50">
                <div className="flex items-center gap-2 mb-2">
                  <div className="flex text-yellow-400">
                    <Star className="w-4 h-4 fill-yellow-400" /><Star className="w-4 h-4 fill-yellow-400" /><Star className="w-4 h-4 fill-yellow-400" /><Star className="w-4 h-4 fill-yellow-400" /><Star className="w-4 h-4 fill-yellow-400" />
                  </div>
                  <span className="text-sm font-medium">Jane S.</span>
                </div>
                <p className="text-gray-600 text-sm">"Great communication and the camera was in perfect condition. Highly recommend renting from John!"</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
