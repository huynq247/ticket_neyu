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

// User Management pages
import UserManagementPage from '@/pages/users/UserManagementPage';
import UserCreatePage from '@/pages/users/UserCreatePage';
import UserEditPage from '@/pages/users/UserEditPage';
import UserProfilePage from '@/pages/users/UserProfilePage';
import RoleManagementPage from '@/pages/users/RoleManagementPage';
import DepartmentManagementPage from '@/pages/users/DepartmentManagementPage';
import CoordinatorManagementPage from '@/pages/users/CoordinatorManagementPage';

// Error pages
import UnauthorizedPage from '@/pages/UnauthorizedPage';
import DebugPage from '@/pages/debug/DebugPage'; // Thêm trang debug

const NotFound = () => <div>404 - Page Not Found</div>;

import { AuthProvider, useAuth } from '@/context/AuthContext';
import { SocketProvider } from '@/context/SocketContext';
import PermissionGuard from '@/components/common/PermissionGuard';

// Protected Route wrapper component
const ProtectedRoute: React.FC<{ element: React.ReactElement; permissions?: string[]; permissionId?: string; requireAll?: boolean }> = ({ 
  element, 
  permissions = [], 
  permissionId,
  requireAll = false 
}) => {
  const { isAuthenticated, isLoading } = useAuth();
  
  if (isLoading) {
    return <div>Loading...</div>; // Could be replaced with a proper loading component
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <PermissionGuard
      permissions={permissions}
      permissionId={permissionId}
      requireAll={requireAll}
      redirectTo="/unauthorized"
    >
      {element}
    </PermissionGuard>
  );
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

      {/* Error Pages */}
      <Route path="/unauthorized" element={<UnauthorizedPage />} />
      
      {/* Protected routes */}
      <Route path="/dashboard" element={<ProtectedRoute element={<DashboardPage />} />} />
      
      {/* Tickets Routes with Permissions */}
      <Route path="/tickets" element={<ProtectedRoute element={<TicketListPage />} permissionId="ticket:view" />} />
      <Route path="/tickets/new" element={<ProtectedRoute element={<NewTicketPage />} permissionId="ticket:create" />} />
      <Route path="/tickets/:id" element={<ProtectedRoute element={<TicketDetailPage />} permissionId="ticket:view" />} />
      
      {/* Analytics Routes with Permissions */}
      <Route path="/analytics" element={<ProtectedRoute element={<AnalyticsDashboardPage />} permissionId="analytics:view" />} />
      
      {/* User Management Routes with Permissions */}
      <Route path="/users" element={<ProtectedRoute element={<UserManagementPage />} permissionId="user:view" />} />
      <Route path="/users/create" element={<ProtectedRoute element={<UserCreatePage />} permissionId="user:create" />} />
      <Route path="/users/:userId/edit" element={<ProtectedRoute element={<UserEditPage />} permissionId="user:update" />} />
      <Route path="/profile" element={<ProtectedRoute element={<UserProfilePage />} />} />
      <Route path="/roles" element={<ProtectedRoute element={<RoleManagementPage />} permissionId="role:view" />} />
      <Route path="/departments" element={<ProtectedRoute element={<DepartmentManagementPage />} permissionId="department:view" />} />
      <Route path="/coordinators" element={<ProtectedRoute element={<CoordinatorManagementPage />} permissions={['dispatcher:assign', 'coordinator:assign']} requireAll={false} />} />
      
      {/* Debug Route */}
      <Route path="/debug" element={<ProtectedRoute element={<DebugPage />} />} />
      
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