// Các kiểu dữ liệu cơ bản cho ứng dụng
export * from './user';
export * from './role';

export enum UserRole {
  ADMIN = 'admin',
  MANAGER = 'manager',
  AGENT = 'agent',
  CUSTOMER = 'customer',
  DISPATCHER = 'dispatcher',
  COORDINATOR = 'coordinator',
}

// Import và export các kiểu dữ liệu role và permission
export * from './role';

export interface Ticket {
  id: string;
  title: string;
  description: string;
  status: TicketStatus;
  priority: TicketPriority;
  category: string;
  assignedTo?: string;
  createdBy: string;
  createdAt: string;
  updatedAt: string;
  dueDate?: string;
  tags?: string[];
  attachments?: Attachment[];
  comments?: Comment[];
}

export enum TicketStatus {
  NEW = 'new',
  OPEN = 'open',
  IN_PROGRESS = 'in_progress',
  PENDING = 'pending',
  RESOLVED = 'resolved',
  CLOSED = 'closed',
}

export enum TicketPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  URGENT = 'urgent',
}

export interface Attachment {
  id: string;
  fileName: string;
  fileType: string;
  fileSize: number;
  fileUrl: string;
  uploadedBy: string;
  uploadedAt: string;
}

export interface Comment {
  id: string;
  content: string;
  createdBy: string;
  createdAt: string;
  updatedAt?: string;
  attachments?: Attachment[];
}

export interface Department {
  id: string;
  name: string;
  description?: string;
  managerId?: string;
  members?: string[];
  createdAt: string;
  updatedAt: string;
}

export interface Category {
  id: string;
  name: string;
  description?: string;
  parentId?: string;
  createdAt: string;
  updatedAt: string;
}

export interface APIResponse<T> {
  data?: T;
  error?: string;
  message?: string;
  status: number;
}

// Request Types
export interface TicketCreateRequest {
  title: string;
  description: string;
  priority: TicketPriority;
  category: string;
  assignedTo?: string;
  dueDate?: string;
  tags?: string[];
  attachments?: File[];
}

export interface TicketUpdateRequest {
  title?: string;
  description?: string;
  status?: TicketStatus;
  priority?: TicketPriority;
  category?: string;
  assignedTo?: string;
  dueDate?: string;
  tags?: string[];
}

export interface CommentCreateRequest {
  content: string;
}

// Statistics Types
export interface TicketStatistics {
  totalTickets: number;
  ticketsByStatus: Record<string, number>;
  ticketsByPriority: Record<string, number>;
  ticketsByCategory: Record<string, number>;
  ticketsTrend: {
    date: string;
    count: number;
  }[];
  averageResolutionTime: number;
  topAssignees: {
    name: string;
    count: number;
  }[];
}

// Dashboard Types
export interface DashboardData {
  ticketsCount: {
    total: number;
    new: number;
    open: number;
    inProgress: number;
    pending: number;
    resolved: number;
    closed: number;
  };
  ticketsOverTime: {
    date: string;
    created: number;
    resolved: number;
  }[];
  priorityDistribution: {
    priority: string;
    count: number;
  }[];
  categoryDistribution: {
    category: string;
    count: number;
  }[];
  recentTickets: Ticket[];
}