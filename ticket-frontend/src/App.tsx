import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import './App.css';

// Auth pages
import LoginPage from '@/pages/auth/LoginPage';
import RegisterPage from '@/pages/auth/RegisterPage';
import ForgotPasswordPage from '@/pages/auth/ForgotPasswordPage';
import ResetPasswordPage from '@/pages/auth/ResetPasswordPage';

// Dashboard and other pages
import DashboardPage from '@/pages/dashboard/DashboardPage';
import TicketListPage from '@/pages/tickets/TicketListPage';
import TicketDetailPage from '@/pages/tickets/TicketDetailPage';
import NewTicketPage from '@/pages/tickets/NewTicketPage';
import AnalyticsDashboardPage from '@/pages/analytics/AnalyticsDashboardPage';

// Placeholder components - sẽ được triển khai sau
const NotFound = () => <div>404 - Page Not Found</div>;

import { AuthProvider, useAuth } from '@/context/AuthContext';
import { SocketProvider } from '@/context/SocketContext';

// Protected Route wrapper component
const ProtectedRoute: React.FC<{ element: React.ReactElement }> = ({ element }) => {
  const { isAuthenticated, isLoading } = useAuth();
  
  if (isLoading) {
    return <div>Loading...</div>; // Could be replaced with a proper loading component
  }
  
  return isAuthenticated ? element : <Navigate to="/login" replace />;
};

const AppRoutes: React.FC = () => {
  const { isAuthenticated } = useAuth();
  
  return (
    <Routes>
      {/* Public routes */}
      <Route 
        path="/login" 
        element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <LoginPage />} 
      />
      <Route 
        path="/register" 
        element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <RegisterPage />} 
      />
      <Route 
        path="/forgot-password" 
        element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <ForgotPasswordPage />} 
      />
      <Route 
        path="/reset-password" 
        element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <ResetPasswordPage />} 
      />
      
      {/* Protected routes */}
      <Route path="/dashboard" element={<ProtectedRoute element={<DashboardPage />} />} />
      <Route path="/tickets" element={<ProtectedRoute element={<TicketListPage />} />} />
      <Route path="/tickets/new" element={<ProtectedRoute element={<NewTicketPage />} />} />
      <Route path="/tickets/:id" element={<ProtectedRoute element={<TicketDetailPage />} />} />
      <Route path="/analytics" element={<ProtectedRoute element={<AnalyticsDashboardPage />} />} />
      
      {/* Redirect to dashboard if authenticated, otherwise to login */}
      <Route
        path="/"
        element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <Navigate to="/login" replace />}
      />
      
      {/* 404 - Not Found */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

const App: React.FC = () => {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: '#1677ff',
          borderRadius: 4,
        },
      }}
    >
      <AuthProvider>
        <SocketProvider>
          <Router>
            <AppRoutes />
          </Router>
        </SocketProvider>
      </AuthProvider>
    </ConfigProvider>
  );
};

export default App;