import apiClient from './apiClient';

export interface ReportFilters {
  startDate?: string;
  endDate?: string;
  departmentId?: string;
  assigneeId?: string;
  reportType?: string;
}

export interface ReportOptions {
  includeCharts?: boolean;
  format?: 'json' | 'csv' | 'pdf' | 'excel';
}

// Lấy báo cáo hiệu suất chung
export const getPerformanceReport = async (filters?: ReportFilters, options?: ReportOptions) => {
  return apiClient.get('/reports/performance', {
    params: { ...filters, ...options },
    responseType: options?.format === 'pdf' || options?.format === 'excel' ? 'blob' : 'json',
  });
};

// Lấy báo cáo về tiến độ ticket
export const getTicketProgressReport = async (filters?: ReportFilters, options?: ReportOptions) => {
  return apiClient.get('/reports/ticket-progress', {
    params: { ...filters, ...options },
    responseType: options?.format === 'pdf' || options?.format === 'excel' ? 'blob' : 'json',
  });
};

// Lấy báo cáo về thời gian phản hồi và giải quyết ticket
export const getResponseTimeReport = async (filters?: ReportFilters, options?: ReportOptions) => {
  return apiClient.get('/reports/response-time', {
    params: { ...filters, ...options },
    responseType: options?.format === 'pdf' || options?.format === 'excel' ? 'blob' : 'json',
  });
};

// Lấy báo cáo về mức độ hài lòng của người dùng
export const getSatisfactionReport = async (filters?: ReportFilters, options?: ReportOptions) => {
  return apiClient.get('/reports/satisfaction', {
    params: { ...filters, ...options },
    responseType: options?.format === 'pdf' || options?.format === 'excel' ? 'blob' : 'json',
  });
};

// Lấy báo cáo về phân phối công việc
export const getWorkloadReport = async (filters?: ReportFilters, options?: ReportOptions) => {
  return apiClient.get('/reports/workload', {
    params: { ...filters, ...options },
    responseType: options?.format === 'pdf' || options?.format === 'excel' ? 'blob' : 'json',
  });
};

// Tạo báo cáo tùy chỉnh
export const createCustomReport = async (
  reportConfig: {
    title: string;
    description?: string;
    metrics: string[];
    filters: ReportFilters;
    groupBy?: string[];
    sortBy?: string;
    limit?: number;
  },
  options?: ReportOptions
) => {
  return apiClient.post('/reports/custom', reportConfig, {
    params: options,
    responseType: options?.format === 'pdf' || options?.format === 'excel' ? 'blob' : 'json',
  });
};

// Lưu cấu hình báo cáo
export const saveReportTemplate = async (
  template: {
    name: string;
    description?: string;
    reportType: string;
    config: any;
    isPublic?: boolean;
  }
) => {
  return apiClient.post('/reports/templates', template);
};

// Lấy danh sách các mẫu báo cáo đã lưu
export const getReportTemplates = async () => {
  return apiClient.get('/reports/templates');
};

// Xuất báo cáo theo định dạng
export const exportReport = async (
  reportId: string,
  format: 'csv' | 'pdf' | 'excel',
  filters?: ReportFilters
) => {
  return apiClient.get(`/reports/${reportId}/export`, {
    params: { format, ...filters },
    responseType: 'blob',
  });
};

// Lên lịch báo cáo tự động
export const scheduleReport = async (
  reportConfig: {
    templateId?: string;
    reportType: string;
    filters?: ReportFilters;
    schedule: {
      frequency: 'daily' | 'weekly' | 'monthly';
      day?: number; // Ngày trong tháng hoặc ngày trong tuần
      time: string; // HH:MM
      recipients: string[]; // Danh sách email
    };
    format: 'csv' | 'pdf' | 'excel';
    name: string;
  }
) => {
  return apiClient.post('/reports/schedule', reportConfig);
};

// Lấy danh sách các báo cáo đã lên lịch
export const getScheduledReports = async () => {
  return apiClient.get('/reports/schedule');
};

// Hủy lịch báo cáo tự động
export const cancelScheduledReport = async (id: string) => {
  return apiClient.delete(`/reports/schedule/${id}`);
};