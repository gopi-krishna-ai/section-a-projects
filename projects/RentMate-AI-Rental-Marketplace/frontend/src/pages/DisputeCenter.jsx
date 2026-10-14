import React from 'react';
import { ShieldAlert, FileText, CheckCircle } from 'lucide-react';

export default function DisputeCenter() {
  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
            <ShieldAlert className="w-8 h-8 text-orange-500" /> Resolution Center
          </h1>
          <p className="text-gray-600 mt-2">Manage disputes, refunds, and support tickets securely.</p>
        </div>
        <button className="bg-orange-500 text-white px-6 py-2 rounded-full font-medium hover:bg-orange-600 shadow-sm">
          Open New Ticket
        </button>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        <div className="md:col-span-2 space-y-4">
          {[
            { id: 'TKT-9921', title: 'Late Return - Camping Tent', status: 'In Review', color: 'bg-yellow-100 text-yellow-700' },
            { id: 'TKT-9842', title: 'Damage Report - Drone Propeller', status: 'Resolved', color: 'bg-green-100 text-green-700' }
          ].map(ticket => (
            <div key={ticket.id} className="bg-white/80 backdrop-blur-md p-6 rounded-2xl border border-white/40 shadow-sm flex items-center justify-between hover:border-orange-200 cursor-pointer transition-colors">
              <div className="flex items-start gap-4">
                <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center text-gray-500">
                  <FileText className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-bold text-gray-900">{ticket.title}</h3>
                  <p className="text-sm text-gray-500">Ticket ID: {ticket.id} • Opened 2 days ago</p>
                </div>
              </div>
              <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${ticket.color}`}>
                {ticket.status}
              </span>
            </div>
          ))}
        </div>
        
        <div className="bg-white/80 backdrop-blur-md p-6 rounded-2xl border border-white/40 shadow-sm h-fit">
          <h3 className="font-bold text-lg mb-4 border-b pb-2">Support Resources</h3>
          <ul className="space-y-3 text-sm text-blue-600">
            <li className="hover:underline cursor-pointer">RentMate Guarantee Policy</li>
            <li className="hover:underline cursor-pointer">How security deposits work</li>
            <li className="hover:underline cursor-pointer">Reporting damage rules</li>
            <li className="hover:underline cursor-pointer">Contact human support</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
