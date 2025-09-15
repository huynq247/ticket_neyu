import apiClient from './apiClient';
import { DashboardData } from '@/types';

export interface AnalyticsParams {
  startDate?: string;
  endDate?: string;
  timeRange?: string;
  departmentId?: string;
  department?: string;
  category?: string;
  groupBy?: string;
}

const analyticsService = {
  getDashboardData: () => {
    return apiClient.get<DashboardData>('/analytics/dashboard');
  },
  
  getTimeAnalysis: (params: AnalyticsParams) => {
    return apiClient.get('/analytics/time/trend', { params });
  },
  
  getTimeCompare: (params: AnalyticsParams) => {
    return apiClient.get('/analytics/time/periods/compare', { params });
  },
  
  getSeasonalAnalysis: (params: AnalyticsParams) => {
    return apiClient.get('/analytics/time/seasonal', { params });
  },
  
  getUserPerformance: (params: AnalyticsParams) => {
    return apiClient.get('/analytics/users/performance', { params });
  },
  
  getDepartmentAnalytics: (params: AnalyticsParams) => {
    return apiClient.get('/analytics/users/departments', { params });
  },
  
  getTopPerformers: (params: AnalyticsParams) => {
    return apiClient.get('/analytics/users/top-performers', { params });
  },
  
  getUserDetails: (userId: string, params: AnalyticsParams) => {
    return apiClient.get(`/analytics/users/user-details/${userId}`, { params });
  },
  
  getCustomAnalytics: (data: any) => {
    return apiClient.post('/analytics/custom', data);
  },
  
  getCorrelationAnalysis: (data: any) => {
    return apiClient.post('/analytics/custom/correlation', data);
  },
  
  getAnomalyDetection: (data: any) => {
    return apiClient.post('/analytics/custom/anomaly-detection', data);
  },
  
  exportAnalytics: (data: any) => {
    return apiClient.post('/analytics/export', data, {
      responseType: 'blob',
    });
  },
};

export default analyticsService;