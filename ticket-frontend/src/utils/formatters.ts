import { TicketStatus, TicketPriority } from '@/types';

// Format date từ ISO string sang định dạng dễ đọc
export const formatDate = (dateString: string, options: Intl.DateTimeFormatOptions = {}) => {
  const defaultOptions: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  };
  
  const mergedOptions = { ...defaultOptions, ...options };
  const date = new Date(dateString);
  
  return new Intl.DateTimeFormat('en-US', mergedOptions).format(date);
};

// Định dạng số với dấu phẩy phân cách hàng nghìn
export const formatNumber = (num: number) => {
  return new Intl.NumberFormat().format(num);
};

// Lấy color code cho trạng thái ticket
export const getStatusColor = (status: TicketStatus) => {
  const statusColors = {
    [TicketStatus.NEW]: '#1677ff', // blue
    [TicketStatus.OPEN]: '#52c41a', // green
    [TicketStatus.IN_PROGRESS]: '#722ed1', // purple
    [TicketStatus.PENDING]: '#faad14', // yellow
    [TicketStatus.RESOLVED]: '#13c2c2', // cyan
    [TicketStatus.CLOSED]: '#8c8c8c', // grey
  };
  
  return statusColors[status] || '#000000';
};

// Lấy color code cho độ ưu tiên ticket
export const getPriorityColor = (priority: TicketPriority) => {
  const priorityColors = {
    [TicketPriority.LOW]: '#52c41a', // green
    [TicketPriority.MEDIUM]: '#1677ff', // blue
    [TicketPriority.HIGH]: '#faad14', // yellow
    [TicketPriority.URGENT]: '#f5222d', // red
  };
  
  return priorityColors[priority] || '#000000';
};

// Truncate text với ellipsis
export const truncateText = (text: string, maxLength: number) => {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
};

// Tạo initials từ tên người dùng
export const getInitials = (name: string) => {
  if (!name) return '';
  
  const names = name.split(' ');
  if (names.length === 1) return names[0].charAt(0).toUpperCase();
  
  return (names[0].charAt(0) + names[names.length - 1].charAt(0)).toUpperCase();
};

// Tạo một mảng các trang cho phân trang
export const getPaginationRange = (
  currentPage: number,
  totalPages: number,
  maxVisiblePages: number = 5
) => {
  if (totalPages <= maxVisiblePages) {
    return Array.from({ length: totalPages }, (_, i) => i + 1);
  }
  
  const halfVisible = Math.floor(maxVisiblePages / 2);
  let startPage = Math.max(currentPage - halfVisible, 1);
  let endPage = startPage + maxVisiblePages - 1;
  
  if (endPage > totalPages) {
    endPage = totalPages;
    startPage = Math.max(endPage - maxVisiblePages + 1, 1);
  }
  
  return Array.from({ length: endPage - startPage + 1 }, (_, i) => startPage + i);
};

// Chuyển đổi kích thước file sang định dạng dễ đọc
export const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

// Chuyển đổi snake_case thành camelCase
export const snakeToCamel = (str: string) => {
  return str.toLowerCase().replace(/([-_][a-z])/g, (group) =>
    group.toUpperCase().replace('-', '').replace('_', '')
  );
};

// Chuyển đổi camelCase thành Title Case
export const camelToTitleCase = (str: string) => {
  const result = str.replace(/([A-Z])/g, ' $1');
  return result.charAt(0).toUpperCase() + result.slice(1);
};