import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Layout from './components/Layout';
import FileUpload from './components/FileUpload';
import PDFViewer from './components/PDFViewer';
import AnalysisDashboard from './components/AnalysisDashboard';
import { Loader2 } from 'lucide-react';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';

// Separate Analysis component to keep App.jsx clean
const Analysis = () => {
  const [file, setFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleFileUpload = (uploadedFile) => {
    setIsProcessing(true);
    setTimeout(() => {
      setFile(uploadedFile);
      setIsProcessing(false);
    }, 1500);
  };

  if (isProcessing) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center animate-in fade-in zoom-in duration-300 h-full">
        <div className="text-center">
          <Loader2 className="w-16 h-16 text-indigo-600 animate-spin mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-slate-800">Processing Document...</h3>
          <p className="text-slate-500">Extracting key financial metrics and risk factors.</p>
        </div>
      </div>
    );
  }

  if (file) {
    return (
      <div className="flex-1 flex flex-row gap-6 h-full p-2 overflow-hidden animate-in slide-in-from-bottom-4 duration-500">
        <div className="w-1/2 h-full min-w-[400px]">
          <PDFViewer file={file} />
        </div>
        <div className="w-1/2 h-full min-w-[400px] overflow-hidden">
          <AnalysisDashboard />
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col items-center justify-center fade-in h-full">
      <div className="w-full max-w-4xl px-4">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-slate-900 mb-2">
            Financial Analysis <span className="text-indigo-600">Reimagined</span>
          </h1>
          <p className="text-lg text-slate-500">
            Upload your credit memos and get instant AI-powered insights.
          </p>
        </div>
        <FileUpload onFileUpload={handleFileUpload} />
      </div>
    </div>
  );
};

// Placeholder components for other routes
const Dashboard = () => <div className="p-6 text-2xl font-bold">Main Dashboard Placeholder</div>;
const Reports = () => <div className="p-6 text-2xl font-bold">Financial Reports Placeholder</div>;

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />

          {/* Protected Routes */}
          <Route path="/" element={
            <ProtectedRoute>
              <Layout>
                <Analysis />
              </Layout>
            </ProtectedRoute>
          } />

          <Route path="/dashboard" element={
            <ProtectedRoute>
              <Layout>
                <Dashboard />
              </Layout>
            </ProtectedRoute>
          } />

          <Route path="/reports" element={
            <ProtectedRoute>
              <Layout>
                <Reports />
              </Layout>
            </ProtectedRoute>
          } />

          <Route path="/settings" element={
            <ProtectedRoute>
              <Layout>
                <div className="p-6 text-2xl font-bold">Settings Placeholder</div>
              </Layout>
            </ProtectedRoute>
          } />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
