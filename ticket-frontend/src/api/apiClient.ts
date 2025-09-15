import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

// Cấu hình mặc định
const config: AxiosRequestConfig = {
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
};

// Tạo instance axios
const axiosInstance: AxiosInstance = axios.create(config);

// Interceptor cho request
axiosInstance.interceptors.request.use(
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

// Interceptor cho response
axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      // Xử lý lỗi 401 Unauthorized
      if (error.response.status === 401) {
        // Xóa token nếu hết hạn và chuyển về trang login
        localStorage.removeItem('auth_token');
        window.location.href = '/login';
      }
      
      // Xử lý lỗi 403 Forbidden
      if (error.response.status === 403) {
        console.error('Forbidden: Access denied');
      }
      
      // Xử lý lỗi 404 Not Found
      if (error.response.status === 404) {
        console.error('Resource not found');
      }
      
      // Xử lý lỗi 500 Internal Server Error
      if (error.response.status >= 500) {
        console.error('Server error');
      }
    } else if (error.request) {
      // Lỗi không nhận được response
      console.error('No response from server');
    } else {
      // Lỗi trong quá trình thiết lập request
      console.error('Error setting up request:', error.message);
    }
    
    return Promise.reject(error);
  }
);

// Hàm wrapper cho các phương thức HTTP
const apiClient = {
  get: <T = any>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return axiosInstance.get<T>(url, config);
  },
  
  post: <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return axiosInstance.post<T>(url, data, config);
  },
  
  put: <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return axiosInstance.put<T>(url, data, config);
  },
  
  patch: <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return axiosInstance.patch<T>(url, data, config);
  },
  
  delete: <T = any>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return axiosInstance.delete<T>(url, config);
  },
};

export default apiClient;