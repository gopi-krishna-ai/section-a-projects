import React, { useContext } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, AuthContext } from './context/AuthContext';

// Pages
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import AIModePage from './pages/AIModePage';
import RenterDashboard from './pages/dashboard/RenterDashboard';
import OwnerDashboard from './pages/dashboard/OwnerDashboard';
import AdminDashboard from './pages/dashboard/AdminDashboard';
import DeliveryDashboard from './pages/dashboard/DeliveryDashboard';
import ItemDetails from './pages/ItemDetails';

// Components
import Navbar from './components/Navbar';

// New Features
import MapSearch from './pages/MapSearch';
import Inbox from './pages/Inbox';
import PublicProfile from './pages/PublicProfile';
import FinancialWallet from './pages/FinancialWallet';
import AIVerification from './pages/AIVerification';
import DisputeCenter from './pages/DisputeCenter';
import WishlistAlerts from './pages/WishlistAlerts';

const ProtectedRoute = ({ children, allowedRoles }) => {
  const { user, loading } = useContext(AuthContext);
  if (loading) return <div>Loading...</div>;
  if (!user) return <Navigate to="/login" />;
  if (allowedRoles && !allowedRoles.includes(user.role)) return <Navigate to="/" />;
  return children;
};

const DashboardRouter = () => {
  const { user } = useContext(AuthContext);
  if (!user) return <Navigate to="/login" />;
  if (user.role === 'RENTER') return <RenterDashboard />;
  if (user.role === 'OWNER') return <OwnerDashboard />;
  if (user.role === 'ADMIN') return <AdminDashboard />;
  if (user.role === 'DELIVERY') return <Navigate to="/delivery-dashboard" />;
  return <Navigate to="/" />;
};

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className="min-h-screen flex flex-col bg-transparent text-gray-900">
          <Navbar />
          <main className="flex-1">
            <Routes>
              <Route path="/" element={<LandingPage />} />
              <Route path="/how-ai-works" element={<AIModePage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/dashboard" element={<ProtectedRoute><DashboardRouter /></ProtectedRoute>} />
              <Route path="/delivery-dashboard" element={<ProtectedRoute allowedRoles={['DELIVERY']}><DeliveryDashboard /></ProtectedRoute>} />
              <Route path="/items/:id" element={<ProtectedRoute><ItemDetails /></ProtectedRoute>} />
              
              {/* New Feature Routes */}
              <Route path="/map" element={<MapSearch />} />
              <Route path="/inbox" element={<ProtectedRoute><Inbox /></ProtectedRoute>} />
              <Route path="/profile" element={<PublicProfile />} />
              <Route path="/wallet" element={<ProtectedRoute allowedRoles={['OWNER']}><FinancialWallet /></ProtectedRoute>} />
              <Route path="/verify" element={<ProtectedRoute><AIVerification /></ProtectedRoute>} />
              <Route path="/disputes" element={<ProtectedRoute><DisputeCenter /></ProtectedRoute>} />
              <Route path="/alerts" element={<ProtectedRoute><WishlistAlerts /></ProtectedRoute>} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
