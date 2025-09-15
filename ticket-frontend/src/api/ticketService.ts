import apiClient from './apiClient';
import { Ticket, TicketStatus, TicketPriority } from '@/types';

export interface CreateTicketRequest {
  title: string;
  description: string;
  category: string;
  priority: TicketPriority;
  tags?: string[];
  attachments?: File[];
}

export interface UpdateTicketRequest {
  title?: string;
  description?: string;
  status?: TicketStatus;
  priority?: TicketPriority;
  category?: string;
  assignedTo?: string;
  tags?: string[];
}

export interface TicketFilterParams {
  status?: TicketStatus | TicketStatus[];
  priority?: TicketPriority | TicketPriority[];
  category?: string | string[];
  assignedTo?: string;
  createdBy?: string;
  createdAfter?: string;
  createdBefore?: string;
  page?: number;
  limit?: number;
  sort?: string;
  order?: 'asc' | 'desc';
}

const ticketService = {
  getAllTickets: (params?: TicketFilterParams) => {
    return apiClient.get<{ tickets: Ticket[]; total: number; page: number; limit: number }>(
      '/tickets',
      { params }
    );
  },
  
  getTicketById: (id: string) => {
    return apiClient.get<Ticket>(`/tickets/${id}`);
  },
  
  createTicket: (data: CreateTicketRequest) => {
    // Xử lý attachments nếu có
    if (data.attachments && data.attachments.length > 0) {
      const formData = new FormData();
      
      // Thêm dữ liệu ticket vào form data
      Object.entries(data).forEach(([key, value]) => {
        if (key !== 'attachments') {
          if (typeof value === 'object' && value !== null) {
            formData.append(key, JSON.stringify(value));
          } else if (value !== undefined) {
            formData.append(key, String(value));
          }
        }
      });
      
      // Thêm attachments vào form data
      data.attachments.forEach((file) => {
        formData.append('attachments', file);
      });
      
      return apiClient.post<Ticket>('/tickets', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
    }
    
    return apiClient.post<Ticket>('/tickets', data);
  },
  
  updateTicket: (id: string, data: UpdateTicketRequest) => {
    return apiClient.put<Ticket>(`/tickets/${id}`, data);
  },
  
  deleteTicket: (id: string) => {
    return apiClient.delete(`/tickets/${id}`);
  },
  
  assignTicket: (id: string, userId: string) => {
    return apiClient.post<Ticket>(`/tickets/${id}/assign`, { userId });
  },
  
  changeStatus: (id: string, status: TicketStatus) => {
    return apiClient.patch<Ticket>(`/tickets/${id}/status`, { status });
  },
  
  addComment: (id: string, content: string, attachments?: File[]) => {
    if (attachments && attachments.length > 0) {
      const formData = new FormData();
      formData.append('content', content);
      
      attachments.forEach((file) => {
        formData.append('attachments', file);
      });
      
      return apiClient.post<{ id: string }>(`/tickets/${id}/comments`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
    }
    
    return apiClient.post<{ id: string }>(`/tickets/${id}/comments`, { content });
  },
  
  getComments: (id: string) => {
    return apiClient.get<{ comments: Comment[] }>(`/tickets/${id}/comments`);
  },
};

export default ticketService;