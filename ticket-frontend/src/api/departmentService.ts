import apiClient from './apiClient';
import { Department } from '@/types';

export interface DepartmentFilters {
  search?: string;
  managerId?: string;
  page?: number;
  limit?: number;
}

export interface CreateDepartmentRequest {
  name: string;
  description?: string;
  managerId?: string;
}

export interface UpdateDepartmentRequest {
  name?: string;
  description?: string;
  managerId?: string;
}

// Lấy danh sách phòng ban
export const getDepartments = async (filters?: DepartmentFilters) => {
  return apiClient.get<{ departments: Department[]; total: number }>('/departments', {
    params: filters,
  });
};

// Lấy thông tin chi tiết phòng ban
export const getDepartmentById = async (id: string) => {
  return apiClient.get<Department>(`/departments/${id}`);
};

// Tạo phòng ban mới
export const createDepartment = async (departmentData: CreateDepartmentRequest) => {
  return apiClient.post<Department>('/departments', departmentData);
};

// Cập nhật thông tin phòng ban
export const updateDepartment = async (id: string, departmentData: UpdateDepartmentRequest) => {
  return apiClient.put<Department>(`/departments/${id}`, departmentData);
};

// Xóa phòng ban
export const deleteDepartment = async (id: string) => {
  return apiClient.delete<{ success: boolean; message: string }>(`/departments/${id}`);
};

// Thêm người dùng vào phòng ban
export const addUserToDepartment = async (departmentId: string, userId: string) => {
  return apiClient.post<Department>(`/departments/${departmentId}/users`, { userId });
};

// Xóa người dùng khỏi phòng ban
export const removeUserFromDepartment = async (departmentId: string, userId: string) => {
  return apiClient.delete<Department>(`/departments/${departmentId}/users/${userId}`);
};

// Thiết lập manager cho phòng ban
export const setDepartmentManager = async (departmentId: string, managerId: string) => {
  return apiClient.post<Department>(`/departments/${departmentId}/manager`, { managerId });
};

// Lấy thống kê của phòng ban
export const getDepartmentStatistics = async (
  departmentId: string,
  startDate?: string,
  endDate?: string
) => {
  return apiClient.get<{
    totalTickets: number;
    resolvedTickets: number;
    averageResponseTime: number;
    userPerformance: { userId: string; username: string; resolved: number; responseTime: number }[];
  }>(`/departments/${departmentId}/statistics`, {
    params: { startDate, endDate },
  });
};