import apiClient from './apiClient';
import { User } from '@/types';

export interface UserFilters {
  search?: string;
  role?: string;
  department?: string;
  isActive?: boolean;
  page?: number;
  limit?: number;
}

export interface UpdateUserRequest {
  firstName?: string;
  lastName?: string;
  email?: string;
  department?: string;
  position?: string;
  phoneNumber?: string;
  isActive?: boolean;
  avatar?: string;
}

// Lấy danh sách tất cả người dùng với filter
export const getUsers = async (filters?: UserFilters) => {
  return apiClient.get<{ users: User[]; total: number }>('/users', { params: filters });
};

// Lấy thông tin chi tiết của một người dùng
export const getUserById = async (id: string) => {
  return apiClient.get<User>(`/users/${id}`);
};

// Cập nhật thông tin người dùng
export const updateUser = async (id: string, userData: UpdateUserRequest) => {
  return apiClient.put<User>(`/users/${id}`, userData);
};

// Đổi mật khẩu
export const changePassword = async (id: string, oldPassword: string, newPassword: string) => {
  return apiClient.post<{ success: boolean; message: string }>(`/users/${id}/change-password`, {
    oldPassword,
    newPassword,
  });
};

// Cập nhật avatar người dùng
export const updateAvatar = async (id: string, file: File) => {
  const formData = new FormData();
  formData.append('avatar', file);
  
  return apiClient.post<{ avatarUrl: string }>(`/users/${id}/avatar`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

// Vô hiệu hóa/kích hoạt người dùng
export const toggleUserStatus = async (id: string, isActive: boolean) => {
  return apiClient.patch<User>(`/users/${id}/status`, { isActive });
};

// Phân công người dùng vào phòng ban
export const assignUserToDepartment = async (userId: string, departmentId: string) => {
  return apiClient.post<User>(`/users/${userId}/departments`, { departmentId });
};

// Lấy thông tin hiệu suất người dùng
export const getUserPerformance = async (id: string, startDate?: string, endDate?: string) => {
  return apiClient.get<{
    ticketsResolved: number;
    averageResponseTime: number;
    satisfactionRate: number;
  }>(`/users/${id}/performance`, {
    params: { startDate, endDate },
  });
};