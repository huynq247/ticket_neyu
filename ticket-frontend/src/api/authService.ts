import apiClient from './apiClient';
import { User } from '@/types';

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  user: User;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  fullName: string;
}

const authService = {
  login: (data: LoginRequest) => {
    return apiClient.post<LoginResponse>('/auth/login', data);
  },
  
  register: (data: RegisterRequest) => {
    return apiClient.post<User>('/auth/register', data);
  },
  
  getCurrentUser: () => {
    return apiClient.get<User>('/auth/me');
  },
  
  refreshToken: () => {
    return apiClient.post<{ token: string }>('/auth/refresh-token');
  },
  
  logout: () => {
    return apiClient.post('/auth/logout');
  },
  
  forgotPassword: (email: string) => {
    return apiClient.post('/auth/forgot-password', { email });
  },
  
  resetPassword: (token: string, password: string) => {
    return apiClient.post('/auth/reset-password', { token, password });
  },
};

export default authService;