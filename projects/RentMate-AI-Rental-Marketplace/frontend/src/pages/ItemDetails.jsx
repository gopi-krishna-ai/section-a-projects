import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api';
import { differenceInDays, parseISO } from 'date-fns';

export default function ItemDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [item, setItem] = useState(null);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [loading, setLoading] = useState(true);
  const [requesting, setRequesting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    api.get(`/items/${id}`)
      .then(res => {
        setItem(res.data);
        setLoading(false);
      })
      .catch(err => {
        setError("Item not found");
        setLoading(false);
      });
  }, [id]);

  if (loading) return <div className="p-12 text-center">Loading...</div>;
  if (error || !item) return <div className="p-12 text-center text-red-500">{error}</div>;

  let days = 0;
  let subtotal = 0;
  const platformFee = 10;
  let total = 0;

  if (startDate && endDate) {
    const s = new Date(startDate);
    const e = new Date(endDate);
    if (e >= s) {
      // Inclusive difference
      days = differenceInDays(e, s) + 1;
      subtotal = days * item.price_per_day;
      total = subtotal + item.security_deposit + platformFee;
    }
  }

  const [showCheckout, setShowCheckout] = useState(false);
  const [paymentProcessing, setPaymentProcessing] = useState(false);
  const [paymentSuccess, setPaymentSuccess] = useState(false);

  const handleOpenCheckout = () => {
    if (days < 1) return setError("Select valid dates");
    setShowCheckout(true);
  };

  const handleConfirmPayment = async () => {
    setPaymentProcessing(true);
    setError('');
    
    // Simulate payment gateway delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    setPaymentSuccess(true);
    
    try {
      await api.post('/rentals/', {
        item_id: item.id,
        start_date: new Date(startDate).toISOString(),
        end_date: new Date(endDate).toISOString()
      });
      
      // Wait to show success state before redirecting
      setTimeout(() => {
        navigate('/dashboard');
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.error || "Failed to process payment & rental");
      setPaymentProcessing(false);
      setPaymentSuccess(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-12 relative">
      <div className="bg-white/80 backdrop-blur-md rounded-3xl shadow-xl shadow-gray-200/50 border border-white/50 overflow-hidden flex flex-col md:flex-row">
        {/* Left: Image Placeholder & Details */}
        <div className="md:w-2/3 p-8 md:p-12 border-r bg-white/50">
          <div className="bg-gradient-to-tr from-gray-200 to-gray-100 h-80 rounded-2xl flex items-center justify-center mb-10 shadow-inner overflow-hidden">
            {item.image_url ? (
              <img src={item.image_url} alt={item.name} className="w-full h-full object-cover" />
            ) : (
              <span className="text-gray-400 font-medium text-lg">Image Placeholder for {item.name}</span>
            )}
          </div>
          <div className="flex justify-between items-start mb-6">
            <div>
              <h1 className="text-4xl font-extrabold text-gray-900 mb-2">{item.name}</h1>
              <span className="inline-block px-3 py-1 bg-emerald-100 text-emerald-800 rounded-full font-semibold text-sm shadow-sm">{item.category}</span>
            </div>
            <div className="text-right bg-white/80 p-3 rounded-xl shadow-sm border border-white/50">
              <p className="text-xs text-gray-500 uppercase font-bold tracking-wider mb-1">Condition</p>
              <p className="font-bold text-gray-900">{item.condition}</p>
            </div>
          </div>
          <div className="prose max-w-none text-gray-600 mb-8">
            <p>{item.description}</p>
          </div>
          <div className="bg-white/60 p-4 rounded-xl border border-white/50 flex justify-between items-center shadow-sm">
            <div>
              <p className="text-sm text-gray-500">Owner</p>
              <p className="font-bold text-gray-900">{item.owner_name}</p>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-500">Location</p>
              <p className="font-medium text-gray-900">{item.location}</p>
            </div>
          </div>
        </div>

        {/* Right: Calculator */}
        <div className="md:w-1/3 p-8 bg-white/40">
          <div className="text-3xl font-bold text-gray-900 mb-6">
            ₹{item.price_per_day} <span className="text-base font-normal text-gray-500">/ day</span>
          </div>

          <div className="space-y-4 mb-8">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
              <input type="date" value={startDate} onChange={e => setStartDate(e.target.value)} className="w-full border-gray-200 shadow-sm rounded-lg p-2 bg-white/80 focus:ring-2 focus:ring-emerald-500 outline-none" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
              <input type="date" value={endDate} onChange={e => setEndDate(e.target.value)} className="w-full border-gray-200 shadow-sm rounded-lg p-2 bg-white/80 focus:ring-2 focus:ring-emerald-500 outline-none" />
            </div>
          </div>

          {days > 0 ? (
            <div className="bg-white/80 p-5 rounded-2xl space-y-3 mb-6 shadow-sm border border-white">
              <div className="flex justify-between text-gray-600">
                <span>₹{item.price_per_day} × {days} days</span>
                <span>₹{subtotal}</span>
              </div>
              <div className="flex justify-between text-gray-600">
                <span>Security Deposit <span className="text-xs ml-1 text-emerald-600 bg-emerald-50 px-1 py-0.5 rounded">Refundable</span></span>
                <span>₹{item.security_deposit}</span>
              </div>
              <div className="flex justify-between text-gray-600">
                <span>Platform Fee</span>
                <span>₹{platformFee}</span>
              </div>
              <div className="border-t border-gray-200 pt-3 flex justify-between font-bold text-xl text-gray-900 mt-2">
                <span>Total to Pay</span>
                <span className="text-emerald-600">₹{total}</span>
              </div>
            </div>
          ) : (
            <div className="bg-blue-50/80 text-blue-800 p-4 rounded-xl text-sm mb-6 border border-blue-100">
              Select valid dates to calculate total cost. Start and End dates are inclusive.
            </div>
          )}

          {error && <div className="text-red-500 text-sm mb-4 bg-red-50 p-2 rounded">{error}</div>}

          <button 
            onClick={handleOpenCheckout}
            disabled={days < 1}
            className="w-full py-4 bg-gradient-to-r from-emerald-500 to-teal-600 text-white font-bold rounded-xl shadow-lg hover:shadow-xl hover:from-emerald-600 hover:to-teal-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Rent Now
          </button>
        </div>
      </div>

      {/* Checkout Modal Overlay */}
      {showCheckout && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/40 backdrop-blur-sm">
          <div className="bg-white rounded-3xl shadow-2xl max-w-md w-full overflow-hidden animate-in fade-in zoom-in-95 duration-200">
            {/* Header */}
            <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
              <h3 className="font-bold text-lg text-gray-800">Secure Checkout</h3>
              {!paymentProcessing && !paymentSuccess && (
                <button onClick={() => setShowCheckout(false)} className="text-gray-400 hover:text-gray-600">
                  <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
                </button>
              )}
            </div>
            
            {/* Body */}
            <div className="p-6">
              {paymentSuccess ? (
                <div className="text-center py-8">
                  <div className="w-20 h-20 bg-emerald-100 text-emerald-500 rounded-full flex items-center justify-center mx-auto mb-4 animate-bounce">
                    <svg className="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" /></svg>
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">Payment Successful!</h2>
                  <p className="text-gray-500">Your rental request for {item.name} has been confirmed. Redirecting to dashboard...</p>
                </div>
              ) : (
                <>
                  <div className="mb-6 p-4 bg-gray-50 rounded-xl border border-gray-100">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-gray-600 font-medium">Total Amount</span>
                      <span className="text-2xl font-bold text-emerald-600">₹{total}</span>
                    </div>
                    <p className="text-xs text-gray-500">Includes ₹{item.security_deposit} fully refundable security deposit.</p>
                  </div>

                  <div className="space-y-4">
                    <div className="border border-gray-200 rounded-xl p-4 cursor-pointer hover:border-emerald-500 transition-colors bg-emerald-50/30">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-blue-600"><svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" /></svg></div>
                        <div className="flex-1">
                          <p className="font-semibold text-gray-800">Credit / Debit Card</p>
                          <p className="text-xs text-gray-500">Visa, Mastercard, RuPay</p>
                        </div>
                        <div className="w-5 h-5 rounded-full border-2 border-emerald-500 flex items-center justify-center">
                          <div className="w-2.5 h-2.5 bg-emerald-500 rounded-full"></div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="border border-gray-200 rounded-xl p-4 cursor-pointer hover:border-gray-300 transition-colors">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center text-purple-600"><svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" /></svg></div>
                        <div className="flex-1">
                          <p className="font-semibold text-gray-800">UPI / QR</p>
                          <p className="text-xs text-gray-500">GPay, PhonePe, Paytm</p>
                        </div>
                        <div className="w-5 h-5 rounded-full border-2 border-gray-300"></div>
                      </div>
                    </div>
                  </div>

                  <button 
                    onClick={handleConfirmPayment}
                    disabled={paymentProcessing}
                    className="w-full mt-8 py-4 bg-gray-900 text-white font-bold rounded-xl shadow-lg hover:shadow-xl hover:bg-gray-800 transition-all flex justify-center items-center gap-2"
                  >
                    {paymentProcessing ? (
                      <><svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> Processing...</>
                    ) : (
                      `Pay ₹${total}`
                    )}
                  </button>
                  <p className="text-center text-xs text-gray-400 mt-4 flex items-center justify-center gap-1">
                    <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>
                    256-bit SSL Encrypted
                  </p>
                </>
              )}
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
