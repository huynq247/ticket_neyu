/**
 * Tiện ích để truy cập biến môi trường một cách an toàn
 */

// API Gateway Configuration
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080';
export const API_TIMEOUT = Number(import.meta.env.VITE_API_TIMEOUT) || 10000;

// Service URLs 
export const USER_SERVICE_URL = import.meta.env.VITE_USER_SERVICE_URL || 'http://localhost:8000';
export const TICKET_SERVICE_URL = import.meta.env.VITE_TICKET_SERVICE_URL || 'http://localhost:8001';
export const FILE_SERVICE_URL = import.meta.env.VITE_FILE_SERVICE_URL || 'http://localhost:8002';
export const NOTIFICATION_SERVICE_URL = import.meta.env.VITE_NOTIFICATION_SERVICE_URL || 'http://localhost:8003';
export const REPORT_SERVICE_URL = import.meta.env.VITE_REPORT_SERVICE_URL || 'http://localhost:8004';
export const ANALYTICS_SERVICE_URL = import.meta.env.VITE_ANALYTICS_SERVICE_URL || 'http://localhost:8005';

// Authentication
export const AUTH_STORAGE_KEY = import.meta.env.VITE_AUTH_STORAGE_KEY || 'auth_token';
export const AUTH_EXPIRY_DAYS = Number(import.meta.env.VITE_AUTH_EXPIRY_DAYS) || 7;

// Features
export const ENABLE_SOCKET_NOTIFICATIONS = 
  import.meta.env.VITE_ENABLE_SOCKET_NOTIFICATIONS === 'true' || true;
export const ENABLE_ANALYTICS = 
  import.meta.env.VITE_ENABLE_ANALYTICS === 'true' || true;

// Development Settings
export const DEV_SERVER_PORT = Number(import.meta.env.VITE_DEV_SERVER_PORT) || 3000;

/**
 * Kiểm tra xem ứng dụng có đang chạy trong môi trường production không
 */
export const isProduction = import.meta.env.MODE === 'production';

/**
 * Kiểm tra xem ứng dụng có đang chạy trong môi trường development không
 */
export const isDevelopment = import.meta.env.MODE === 'development';

export default {
  API_BASE_URL,
  API_TIMEOUT,
  USER_SERVICE_URL,
  TICKET_SERVICE_URL,
  FILE_SERVICE_URL,
  NOTIFICATION_SERVICE_URL,
  REPORT_SERVICE_URL,
  ANALYTICS_SERVICE_URL,
  AUTH_STORAGE_KEY,
  AUTH_EXPIRY_DAYS,
  ENABLE_SOCKET_NOTIFICATIONS,
  ENABLE_ANALYTICS,
  DEV_SERVER_PORT,
  isProduction,
  isDevelopment
};