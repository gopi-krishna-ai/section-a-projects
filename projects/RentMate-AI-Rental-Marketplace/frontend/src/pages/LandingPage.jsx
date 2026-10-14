import React from 'react';
import { Link } from 'react-router-dom';
import { Search, MapPin, Calendar, Sparkles } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="bg-transparent">
      {/* Hero Section */}
      <div className="relative overflow-hidden bg-transparent">
        <div className="absolute top-0 -left-4 w-72 h-72 bg-emerald-200 rounded-full mix-blend-multiply filter blur-2xl opacity-30 animate-blob"></div>
        <div className="absolute top-0 -right-4 w-72 h-72 bg-emerald-300 rounded-full mix-blend-multiply filter blur-2xl opacity-30 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-20 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-2xl opacity-30 animate-blob animation-delay-4000"></div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-32 text-center">
          <h1 className="text-5xl md:text-7xl font-extrabold text-gray-900 tracking-tight mb-8 drop-shadow-sm">
            RENT WHAT YOU NEED.<br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-rentmate-green to-emerald-600">EARN FROM WHAT YOU OWN.</span>
          </h1>
          <p className="mt-4 max-w-2xl text-xl md:text-2xl text-gray-600 mx-auto mb-12 bg-white/30 backdrop-blur-sm p-4 rounded-xl border border-white/40 shadow-sm">
            Why buy something you only need for a few days? <br/>
            Rent it from someone nearby using our AI-powered marketplace.
          </p>
          
          <div className="flex flex-col sm:flex-row justify-center gap-6">
            <Link to="/login" className="px-8 py-4 bg-rentmate-green text-white rounded-full font-bold text-lg hover:bg-emerald-600 transition-all hover:scale-105 shadow-xl shadow-emerald-200/50">
              Find Something to Rent
            </Link>
            <Link to="/login" className="px-8 py-4 bg-white/80 backdrop-blur-sm text-gray-900 rounded-full font-bold text-lg border-2 border-emerald-100 hover:border-emerald-200 hover:bg-white transition-all hover:scale-105 shadow-xl shadow-gray-100">
              Rent Out My Item
            </Link>
          </div>
        </div>
      </div>

      {/* Visual Cards Example */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <p className="text-center text-sm font-semibold text-gray-500 uppercase tracking-widest mb-8">Popular Items to Rent</p>
        <div className="flex flex-wrap justify-center gap-4">
          {['Power Drill', 'Camping Tent', 'Projector', 'Table Fan', 'Plastic Chairs', 'Hand Trolley'].map((item) => (
            <div key={item} className="px-6 py-3 bg-white/80 backdrop-blur-sm border border-white/50 rounded-full text-gray-700 font-medium shadow-sm flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-rentmate-green"></span>
              {item}
            </div>
          ))}
        </div>
      </div>

      {/* How it Works */}
      <div className="bg-white/40 backdrop-blur-md border-y border-white/40 py-24 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900">How RentMate Works</h2>
            <p className="mt-4 text-lg text-gray-700">Our AI understands what you need, even if you don't know the exact item name.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-12">
            <div className="text-center bg-white/60 p-8 rounded-2xl border border-white/50 shadow-sm">
              <div className="w-16 h-16 bg-blue-100 text-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-sm">
                <Sparkles className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-bold mb-2">1. Tell the AI</h3>
              <p className="text-gray-700">"I'm organizing a movie night for 10 people outdoors."</p>
            </div>
            <div className="text-center bg-white/60 p-8 rounded-2xl border border-white/50 shadow-sm">
              <div className="w-16 h-16 bg-green-100 text-rentmate-green rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-sm">
                <Search className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-bold mb-2">2. Get Matches</h3>
              <p className="text-gray-700">AI recommends Projectors, Screens, and Speakers available nearby.</p>
            </div>
            <div className="text-center bg-white/60 p-8 rounded-2xl border border-white/50 shadow-sm">
              <div className="w-16 h-16 bg-purple-100 text-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-sm">
                <Calendar className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-bold mb-2">3. Book & Use</h3>
              <p className="text-gray-700">Select your dates, pay securely, and pick up the items.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="bg-white/30 backdrop-blur-sm py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div className="bg-white/50 p-6 rounded-2xl border border-white/50">
              <p className="text-4xl font-extrabold text-gray-900">1,250+</p>
              <p className="text-sm text-gray-700 font-medium mt-1">Items Listed</p>
            </div>
            <div className="bg-white/50 p-6 rounded-2xl border border-white/50">
              <p className="text-4xl font-extrabold text-gray-900">850+</p>
              <p className="text-sm text-gray-700 font-medium mt-1">Successful Rentals</p>
            </div>
            <div className="bg-white/50 p-6 rounded-2xl border border-white/50">
              <p className="text-4xl font-extrabold text-gray-900">620+</p>
              <p className="text-sm text-gray-700 font-medium mt-1">Active Owners</p>
            </div>
            <div className="bg-white/50 p-6 rounded-2xl border border-white/50">
              <p className="text-4xl font-extrabold text-gray-900">2,400+</p>
              <p className="text-sm text-gray-700 font-medium mt-1">Happy Renters</p>
            </div>
          </div>
          <p className="text-center text-xs text-gray-500 font-medium mt-8">* Statistics represent demo seed data.</p>
        </div>
      </div>
    </div>
  );
}
