import React, { useState, useContext, useEffect } from 'react';
import { AuthContext } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { UserCircle, Shield, ShoppingBag, Truck, ChevronRight } from 'lucide-react';

const ROLE_DATA = {
  RENTER: {
    bg: 'https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&q=80',
    title: 'Rent What You Need',
    subtitle: 'Access thousands of items nearby without the commitment of buying.',
    color: 'from-green-600 to-emerald-400',
    icon: ShoppingBag,
    email: 'renter@rentmate.demo',
    pass: '1234'
  },
  OWNER: {
    bg: 'https://images.unsplash.com/photo-1556910103-1c02745a872f?auto=format&fit=crop&q=80',
    title: 'Earn From Your Items',
    subtitle: 'Turn your idle items into a steady stream of passive income.',
    color: 'from-blue-600 to-cyan-400',
    icon: UserCircle,
    email: 'owner@rentmate.demo',
    pass: '1234'
  },
  DELIVERY: {
    bg: 'https://images.unsplash.com/photo-1617347454431-f49cd38d5c12?auto=format&fit=crop&q=80',
    title: 'Deliver & Earn',
    subtitle: 'Flexible hours. Pick up and drop off rentals in your local area.',
    color: 'from-orange-600 to-amber-400',
    icon: Truck,
    email: 'delivery@rentmate.demo',
    pass: '1234'
  },
  ADMIN: {
    bg: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80',
    title: 'Platform Control',
    subtitle: 'Monitor marketplace health, resolve disputes, and manage users.',
    color: 'from-purple-600 to-fuchsia-400',
    icon: Shield,
    email: 'admin@rentmate.demo',
    pass: 'admin123'
  }
};

export default function LoginPage() {
  const [activeRole, setActiveRole] = useState('RENTER');
  const [email, setEmail] = useState(ROLE_DATA['RENTER'].email);
  const [password, setPassword] = useState(ROLE_DATA['RENTER'].pass);
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const [isFading, setIsFading] = useState(false);
  const [isRegistering, setIsRegistering] = useState(false);
  
  const { login, register } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleRoleChange = (role) => {
    setIsFading(true);
    setTimeout(() => {
      setActiveRole(role);
      if (!isRegistering) {
        setEmail(ROLE_DATA[role].email);
        setPassword(ROLE_DATA[role].pass);
      }
      setIsFading(false);
    }, 200); // quick fade transition
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const user = await register(name, email, password, activeRole);
      if (user?.role === 'DELIVERY') navigate('/delivery-dashboard');
      else navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed');
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const user = await login(email, password);
      if (user?.role === 'DELIVERY') {
        navigate('/delivery-dashboard');
      } else {
        navigate('/dashboard');
      }
    } catch (err) {
      setError('Invalid credentials');
    }
  };

  const ActiveIcon = ROLE_DATA[activeRole].icon;

  return (
    <div className="relative min-h-[calc(100vh-4rem)] flex w-full bg-gray-900 overflow-hidden">
      {/* Dynamic Background */}
      <div 
        className={`absolute inset-0 transition-opacity duration-500 ease-in-out ${isFading ? 'opacity-0' : 'opacity-100'}`}
        style={{
          backgroundImage: `url(${ROLE_DATA[activeRole].bg})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }}
      >
        <div className="absolute inset-0 bg-gray-900/60 backdrop-blur-sm mix-blend-multiply" />
        <div className={`absolute inset-0 bg-gradient-to-br ${ROLE_DATA[activeRole].color} opacity-40 mix-blend-overlay`} />
      </div>

      <div className="relative z-10 flex flex-col md:flex-row w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Left Side: Role Selector & Copy */}
        <div className="flex-1 flex flex-col justify-center py-12 pr-0 md:pr-12">
          <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-4 tracking-tight drop-shadow-md transition-all duration-300">
            {ROLE_DATA[activeRole].title}
          </h1>
          <p className="text-lg md:text-xl text-gray-200 mb-10 max-w-lg transition-all duration-300">
            {ROLE_DATA[activeRole].subtitle}
          </p>
          
          <div className="space-y-3">
            <p className="text-sm font-bold text-gray-300 uppercase tracking-widest mb-4">Choose your journey</p>
            {Object.keys(ROLE_DATA).map((role) => {
              const Icon = ROLE_DATA[role].icon;
              const isActive = activeRole === role;
              return (
                <button
                  key={role}
                  onClick={() => handleRoleChange(role)}
                  className={`w-full max-w-md flex items-center justify-between p-4 rounded-xl transition-all duration-300 border ${
                    isActive 
                      ? 'bg-white/20 border-white/50 shadow-lg backdrop-blur-md translate-x-2' 
                      : 'bg-white/5 border-white/10 hover:bg-white/10 text-gray-300'
                  }`}
                >
                  <div className="flex items-center gap-4">
                    <div className={`p-2 rounded-lg ${isActive ? 'bg-white text-gray-900' : 'bg-white/10 text-white'}`}>
                      <Icon className="w-5 h-5" />
                    </div>
                    <span className={`font-bold text-lg ${isActive ? 'text-white' : ''}`}>
                      Join as {role.charAt(0) + role.slice(1).toLowerCase()}
                    </span>
                  </div>
                  {isActive && <ChevronRight className="w-5 h-5 text-white" />}
                </button>
              );
            })}
          </div>
        </div>

        {/* Right Side: Login/Register Form */}
        <div className="flex-1 flex flex-col justify-center items-center md:items-end py-12">
          <div className="w-full max-w-md bg-white/10 backdrop-blur-xl p-8 rounded-3xl border border-white/20 shadow-2xl">
            <div className="text-center mb-8">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-white/20 mb-4">
                <ActiveIcon className="w-8 h-8 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-white">{isRegistering ? 'Create Account' : 'Sign In'}</h2>
              <p className="text-gray-300 text-sm mt-2">
                {isRegistering ? 'Join the platform today' : 'Enter your credentials to access the platform'}
              </p>
            </div>

            <form className="space-y-5" onSubmit={isRegistering ? handleRegister : handleLogin}>
              {error && (
                <div className="bg-red-500/20 border border-red-500/50 text-white text-sm text-center p-3 rounded-xl">
                  {error}
                </div>
              )}
              
              {isRegistering && (
                <div>
                  <label className="block text-sm font-medium text-gray-200 mb-1">Full Name</label>
                  <input 
                    type="text" 
                    required 
                    value={name} 
                    onChange={(e) => setName(e.target.value)} 
                    className="w-full px-4 py-3 bg-gray-900/50 border border-white/10 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all" 
                  />
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-gray-200 mb-1">Email Address</label>
                <input 
                  type="email" 
                  required 
                  value={email} 
                  onChange={(e) => setEmail(e.target.value)} 
                  className="w-full px-4 py-3 bg-gray-900/50 border border-white/10 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all" 
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-200 mb-1">Password</label>
                <input 
                  type="password" 
                  required 
                  value={password} 
                  onChange={(e) => setPassword(e.target.value)} 
                  className="w-full px-4 py-3 bg-gray-900/50 border border-white/10 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all" 
                />
              </div>

              <div className="pt-4">
                <button 
                  type="submit" 
                  className={`w-full flex justify-center py-3 px-4 border border-transparent rounded-xl shadow-sm text-lg font-bold text-white bg-gradient-to-r ${ROLE_DATA[activeRole].color} hover:opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-900 focus:ring-white transition-all transform hover:scale-[1.02]`}
                >
                  {isRegistering ? `Register as ${activeRole.charAt(0) + activeRole.slice(1).toLowerCase()}` : `Continue as ${activeRole.charAt(0) + activeRole.slice(1).toLowerCase()}`}
                </button>
              </div>
              
              <div className="text-center mt-4">
                <button 
                  type="button" 
                  onClick={() => {
                    setIsRegistering(!isRegistering);
                    setError('');
                  }}
                  className="text-sm font-medium text-white hover:underline focus:outline-none"
                >
                  {isRegistering ? 'Already have an account? Sign in' : "Don't have an account? Register"}
                </button>
              </div>
            </form>
          </div>
        </div>

      </div>
    </div>
  );
}
