import React from 'react';
import { Wallet, ArrowUpRight, ArrowDownRight, DollarSign, Building } from 'lucide-react';

export default function FinancialWallet() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
          <Wallet className="w-8 h-8 text-rentmate-green" /> Financial Dashboard
        </h1>
        <button className="bg-gray-900 text-white px-6 py-2 rounded-full font-medium hover:bg-gray-800">
          Withdraw Funds
        </button>
      </div>

      <div className="grid md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white/80 backdrop-blur-md p-6 rounded-3xl shadow-sm border border-white/40">
          <p className="text-gray-500 font-medium mb-1">Available Balance</p>
          <h2 className="text-4xl font-extrabold text-gray-900">$1,250.00</h2>
          <p className="text-sm text-green-500 mt-2 flex items-center gap-1"><ArrowUpRight className="w-4 h-4" /> +$450 this month</p>
        </div>
        <div className="bg-white/80 backdrop-blur-md p-6 rounded-3xl shadow-sm border border-white/40">
          <p className="text-gray-500 font-medium mb-1">Pending Payouts</p>
          <h2 className="text-4xl font-extrabold text-gray-900">$320.00</h2>
          <p className="text-sm text-gray-500 mt-2">Clearing in 2-3 days</p>
        </div>
        <div className="bg-white/80 backdrop-blur-md p-6 rounded-3xl shadow-sm border border-white/40">
          <p className="text-gray-500 font-medium mb-1">Security Deposits Held</p>
          <h2 className="text-4xl font-extrabold text-gray-900">$850.00</h2>
          <p className="text-sm text-gray-500 mt-2 flex items-center gap-1"><ShieldCheckIcon className="w-4 h-4" /> Protected by RentMate</p>
        </div>
      </div>

      <div className="bg-white/80 backdrop-blur-md rounded-3xl shadow-sm border border-white/40 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center">
          <h3 className="font-bold text-lg">Recent Transactions</h3>
          <span className="text-sm text-blue-500 cursor-pointer hover:underline">View All</span>
        </div>
        <div className="divide-y divide-gray-50">
          {[1,2,3,4].map((i, index) => {
            const txAmounts = [82.50, 140.00, 95.25, 115.75];
            return (
              <div key={i} className="px-6 py-4 flex items-center justify-between hover:bg-gray-50/50">
                <div className="flex items-center gap-4">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center ${i%2===0 ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'}`}>
                    {i%2===0 ? <ArrowUpRight className="w-5 h-5" /> : <ArrowDownRight className="w-5 h-5" />}
                  </div>
                  <div>
                    <p className="font-bold text-sm">{i%2===0 ? 'Rental Income - DSLR Camera' : 'Withdrawal to Bank'}</p>
                    <p className="text-xs text-gray-500">Sep 2{i}, 2026</p>
                  </div>
                </div>
                <div className={`font-bold ${i%2===0 ? 'text-green-600' : 'text-gray-900'}`}>
                  {i%2===0 ? '+$' : '-$'}{txAmounts[index].toFixed(2)}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
// Hack for lucide icon missing above
function ShieldCheckIcon(props) { return <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>; }
