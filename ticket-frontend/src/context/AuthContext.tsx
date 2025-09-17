import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User } from '@/types';
import { resetPermissionCache } from '@/utils/permissionUtils';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  error: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Kiểm tra nếu người dùng đã đăng nhập trước đó
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('auth_token');
        
        if (token) {
          // TODO: Gọi API để xác thực token và lấy thông tin người dùng
          // const response = await api.auth.verifyToken();
          // setUser(response.data);
          
          // Thử lấy thông tin người dùng từ localStorage nếu có
          const savedUser = localStorage.getItem('user');
          if (savedUser) {
            try {
              const parsedUser = JSON.parse(savedUser);
              setUser(parsedUser);
              return;
            } catch (err) {
              console.error('Error parsing saved user:', err);
            }
          }
          
          // Mock data cho phát triển ban đầu
          setUser({
            id: '1',
            email: 'admin@example.com',
            firstName: 'Admin',
            lastName: 'User',
            fullName: 'Admin User',
            roles: [
              {
                id: 'admin-role',
                name: 'admin',
                description: 'Administrator role with all permissions',
                permissions: [
                  'analytics:view',
                  'analytics:advanced',
                  'ticket:view',
                  'ticket:create',
                  'ticket:update',
                  'ticket:delete',
                  'ticket:assign',
                  'ticket:comment',
                  'ticket:change-status',
                  'ticket:view-all',
                ],
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString(),
              }
            ],
            isActive: true,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
          });
        }
      } catch (err) {
        console.error('Authentication error:', err);
        localStorage.removeItem('auth_token');
        setError('Session expired. Please login again.');
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    setError(null);
    
    try {
      // TODO: Gọi API để xác thực và đăng nhập
      // const response = await api.auth.login({ email, password });
      // const { token, user } = response.data;
      
      // Mock data cho phát triển ban đầu
      const token = 'mock-token-' + Date.now();
      const mockUser: User = {
        id: '1',
        email: email,
        firstName: 'Admin',
        lastName: 'User',
        fullName: 'Admin User',
        roles: [
          {
            id: 'admin-role',
            name: 'admin',
            description: 'Administrator role with all permissions',
            permissions: [
              'analytics:view',
              'analytics:advanced',
              'ticket:view',
              'ticket:create',
              'ticket:update',
              'ticket:delete',
              'ticket:assign',
              'ticket:comment',
              'ticket:change-status',
              'ticket:view-all',
            ],
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
          }
        ],
        isActive: true,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };
      
      localStorage.setItem('auth_token', token);
      localStorage.setItem('user', JSON.stringify(mockUser));
      setUser(mockUser);
      
      // Reset permission cache sau khi đăng nhập
      resetPermissionCache();
    } catch (err: any) {
      setError(err.message || 'Failed to login. Please check your credentials.');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    setUser(null);
    
    // Reset permission cache sau khi đăng xuất
    resetPermissionCache();
  };

  const value = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    logout,
    error,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
};