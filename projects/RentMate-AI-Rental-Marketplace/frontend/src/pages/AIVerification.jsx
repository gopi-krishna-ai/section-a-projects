import React from 'react';
import { Camera, CheckCircle, AlertTriangle, ScanLine } from 'lucide-react';

export default function AIVerification() {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center mb-10">
        <h1 className="text-3xl font-bold text-gray-900 flex items-center justify-center gap-3">
          <ScanLine className="w-8 h-8 text-blue-500" /> AI Condition Verification
        </h1>
        <p className="text-gray-600 mt-2">Log item condition before and after rental to protect yourself.</p>
      </div>

      <div className="bg-white/80 backdrop-blur-md rounded-3xl shadow-sm border border-white/40 p-8 mb-8">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold">Rental #RN-84920</h2>
          <span className="px-3 py-1 bg-blue-100 text-blue-600 rounded-full text-xs font-bold uppercase tracking-wider">Handoff Phase</span>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Upload Area */}
          <div className="border-2 border-dashed border-gray-300 rounded-2xl p-8 flex flex-col items-center justify-center text-center cursor-pointer hover:border-blue-400 hover:bg-blue-50/50 transition-colors">
            <div className="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center mb-4 text-blue-500">
              <Camera className="w-8 h-8" />
            </div>
            <h3 className="font-bold text-gray-700">Upload Pre-Rental Photos</h3>
            <p className="text-sm text-gray-400 mt-2">Take clear photos of all sides of the item.</p>
          </div>

          {/* AI Analysis Result Mock */}
          <div className="bg-gray-50 rounded-2xl p-6 border border-gray-100">
            <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-rentmate-green" /> AI Analysis Complete
            </h3>
            
            <div className="space-y-4">
              <div className="bg-white p-3 rounded-lg border border-gray-100 shadow-sm flex items-start gap-3">
                <CheckCircle className="w-5 h-5 text-rentmate-green shrink-0 mt-0.5" />
                <div>
                  <p className="font-medium text-sm">Model Match Verified</p>
                  <p className="text-xs text-gray-500">Item in photo matches listing "Sony Alpha A7III".</p>
                </div>
              </div>
              <div className="bg-white p-3 rounded-lg border border-gray-100 shadow-sm flex items-start gap-3">
                <AlertTriangle className="w-5 h-5 text-orange-500 shrink-0 mt-0.5" />
                <div>
                  <p className="font-medium text-sm">Minor Scratch Detected</p>
                  <p className="text-xs text-gray-500">A small 2cm scratch detected on the bottom plate. Logged in system.</p>
                </div>
              </div>
            </div>
            
            <button className="w-full mt-6 bg-blue-600 text-white py-2 rounded-xl font-bold hover:bg-blue-700">
              Confirm & Handover
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
