import { useState, useEffect, useContext, createContext } from 'react';
import { User } from '@/types';
import authService from '@/api/authService';

interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
  loading: boolean;
}

interface AuthContextType {
  authState: AuthState;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const initialAuthState: AuthState = {
  isAuthenticated: false,
  user: null,
  token: null,
  loading: true,
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Singleton pattern để truy cập trạng thái xác thực từ bất kỳ đâu
let _authState: AuthState = { ...initialAuthState };

export const getAuthState = (): AuthState => {
  return _authState;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [authState, setAuthState] = useState<AuthState>(initialAuthState);

  // Cập nhật singleton khi authState thay đổi
  useEffect(() => {
    _authState = authState;
  }, [authState]);

  // Kiểm tra phiên đăng nhập khi khởi động
  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          // Tải thông tin người dùng nếu có token
          const userResponse = await authService.getCurrentUser();
          setAuthState({
            isAuthenticated: true,
            user: userResponse.data,
            token,
            loading: false,
          });
        } catch (error) {
          // Token không hợp lệ hoặc hết hạn
          localStorage.removeItem('token');
          setAuthState({
            ...initialAuthState,
            loading: false,
          });
        }
      } else {
        setAuthState({
          ...initialAuthState,
          loading: false,
        });
      }
    };

    initAuth();
  }, []);

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      const response = await authService.login({ email, password });
      const { token, user } = response.data;
      
      // Lưu token vào localStorage
      localStorage.setItem('token', token);
      
      // Cập nhật trạng thái xác thực
      setAuthState({
        isAuthenticated: true,
        user,
        token,
        loading: false,
      });
      
      return true;
    } catch (error) {
      return false;
    }
  };

  const logout = async (): Promise<void> => {
    try {
      await authService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Xóa token từ localStorage
      localStorage.removeItem('token');
      
      // Đặt lại trạng thái xác thực
      setAuthState({
        isAuthenticated: false,
        user: null,
        token: null,
        loading: false,
      });
    }
  };

  const refreshUser = async (): Promise<void> => {
    try {
      const response = await authService.getCurrentUser();
      setAuthState(prevState => ({
        ...prevState,
        user: response.data,
      }));
    } catch (error) {
      console.error('Error refreshing user:', error);
    }
  };

  return (
    <AuthContext.Provider value={{ authState, login, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};