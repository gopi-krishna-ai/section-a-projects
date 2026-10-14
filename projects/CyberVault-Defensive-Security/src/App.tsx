import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import PasswordAnalysis from './pages/PasswordAnalysis';
import PasswordGenerator from './pages/PasswordGenerator';
import UrlAnalysis from './pages/UrlAnalysis';
import PhishingDetector from './pages/PhishingDetector';
import WebsiteScanner from './pages/WebsiteScanner';
import FileHashes from './pages/FileHashes';
import IntegrityCheck from './pages/IntegrityCheck';
import LogAnalyzer from './pages/LogAnalyzer';
import PortScanner from './pages/PortScanner';
import UserAnalytics from './pages/UserAnalytics';
import ScanHistory from './pages/ScanHistory';
import PdfReport from './pages/PdfReport';
import Assistant from './pages/Assistant';
import Settings from './pages/Settings';
import Layout from './components/Layout';

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        
        {/* Protected Dashboard Routes */}
        <Route element={<Layout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/dashboard/password" element={<PasswordAnalysis />} />
          <Route path="/dashboard/generate" element={<PasswordGenerator />} />
          <Route path="/dashboard/url" element={<UrlAnalysis />} />
          <Route path="/dashboard/phishing" element={<PhishingDetector />} />
          <Route path="/dashboard/website" element={<WebsiteScanner />} />
          <Route path="/dashboard/hash" element={<FileHashes />} />
          <Route path="/dashboard/integrity" element={<IntegrityCheck />} />
          <Route path="/dashboard/logs" element={<LogAnalyzer />} />
          <Route path="/dashboard/ports" element={<PortScanner />} />
          <Route path="/dashboard/analytics" element={<UserAnalytics />} />
          <Route path="/dashboard/history" element={<ScanHistory />} />
          <Route path="/dashboard/report" element={<PdfReport />} />
          <Route path="/dashboard/assistant" element={<Assistant />} />
          <Route path="/dashboard/settings" element={<Settings />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
