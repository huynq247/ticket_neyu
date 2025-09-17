import { Role, Permission } from '@/types';
import { USER_SERVICE_URL } from '@/utils/env';
import axios from 'axios';

// Tạo client riêng cho user service
const userServiceClient = axios.create({
  baseURL: USER_SERVICE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Thêm interceptor cho authentication
userServiceClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export interface RoleFilters {
  search?: string;
  page?: number;
  limit?: number;
}

export interface CreateRoleRequest {
  name: string;
  description?: string;
  permissions: string[];
}

export interface UpdateRoleRequest {
  name?: string;
  description?: string;
  permissions?: string[];
}

// Lấy danh sách vai trò
export const getRoles = async (filters?: RoleFilters) => {
  return userServiceClient.get<{ roles: Role[]; total: number }>('/api/v1/roles', {
    params: filters,
  });
};

// Lấy thông tin chi tiết vai trò
export const getRoleById = async (id: string) => {
  return userServiceClient.get<Role>(`/api/v1/roles/${id}`);
};

// Tạo vai trò mới
export const createRole = async (roleData: CreateRoleRequest) => {
  return userServiceClient.post<Role>('/api/v1/roles', roleData);
};

// Cập nhật thông tin vai trò
export const updateRole = async (id: string, roleData: UpdateRoleRequest) => {
  return userServiceClient.put<Role>(`/api/v1/roles/${id}`, roleData);
};

// Xóa vai trò
export const deleteRole = async (id: string) => {
  return userServiceClient.delete<{ success: boolean; message: string }>(`/api/v1/roles/${id}`);
};

// Lấy danh sách quyền
export const getPermissions = async () => {
  try {
    const response = await userServiceClient.get<{ permissions: Permission[] }>('/api/v1/permissions');
    return response;
  } catch (error) {
    console.error('Error fetching permissions from API:', error);
    throw error;
  }
};

// Lấy vai trò của người dùng
export const getUserRoles = async (userId: string) => {
  return userServiceClient.get<{ roles: Role[] }>(`/api/v1/users/${userId}/roles`);
};

// Gán vai trò cho người dùng
export const assignRoleToUser = async (userId: string, roleId: string) => {
  return userServiceClient.post<{ success: boolean; message: string }>(`/api/v1/users/${userId}/roles`, { roleId });
};

// Xóa vai trò khỏi người dùng
export const removeRoleFromUser = async (userId: string, roleId: string) => {
  return userServiceClient.delete<{ success: boolean; message: string }>(`/api/v1/users/${userId}/roles/${roleId}`);
};