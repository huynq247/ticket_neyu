import apiClient from './apiClient';
import { User } from '@/types';

// Lấy danh sách dispatchers
export const getDispatchers = async () => {
  return apiClient.get<{ dispatchers: User[] }>('/dispatchers');
};

// Lấy danh sách coordinators
export const getCoordinators = async () => {
  return apiClient.get<{ coordinators: User[] }>('/coordinators');
};

// Lấy danh sách dispatchers của phòng ban
export const getDepartmentDispatchers = async (departmentId: string) => {
  return apiClient.get<{ dispatchers: User[] }>(`/departments/${departmentId}/dispatchers`);
};

// Thêm dispatcher cho phòng ban
export const addDispatcherToDepartment = async (departmentId: string, userId: string) => {
  return apiClient.post<{ success: boolean; message: string }>(`/departments/${departmentId}/dispatchers`, { 
    userId 
  });
};

// Xóa dispatcher khỏi phòng ban
export const removeDispatcherFromDepartment = async (departmentId: string, userId: string) => {
  return apiClient.delete<{ success: boolean; message: string }>(`/departments/${departmentId}/dispatchers/${userId}`);
};

// Lấy danh sách coordinators của phòng ban
export const getDepartmentCoordinators = async (departmentId: string) => {
  return apiClient.get<{ coordinators: User[] }>(`/departments/${departmentId}/coordinators`);
};

// Thêm coordinator cho phòng ban
export const addCoordinatorToDepartment = async (departmentId: string, userId: string) => {
  return apiClient.post<{ success: boolean; message: string }>(`/departments/${departmentId}/coordinators`, { 
    userId 
  });
};

// Xóa coordinator khỏi phòng ban
export const removeCoordinatorFromDepartment = async (departmentId: string, userId: string) => {
  return apiClient.delete<{ success: boolean; message: string }>(`/departments/${departmentId}/coordinators/${userId}`);
};