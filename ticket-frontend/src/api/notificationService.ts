import apiClient from './apiClient';

export interface Notification {
  id: string;
  userId: string;
  title: string;
  content: string;
  type: string;
  isRead: boolean;
  relatedEntityId?: string;
  relatedEntityType?: string;
  createdAt: string;
  updatedAt: string;
}

export interface NotificationFilters {
  isRead?: boolean;
  type?: string;
  page?: number;
  limit?: number;
}

export interface CreateNotificationPreference {
  email: boolean;
  push: boolean;
  inApp: boolean;
}

export interface NotificationPreferences {
  ticketAssigned: CreateNotificationPreference;
  ticketStatusUpdated: CreateNotificationPreference;
  commentAdded: CreateNotificationPreference;
  ticketDueSoon: CreateNotificationPreference;
  ticketCreated: CreateNotificationPreference;
}

// Lấy danh sách thông báo của người dùng hiện tại
export const getNotifications = async (filters?: NotificationFilters) => {
  return apiClient.get<{ notifications: Notification[]; total: number; unread: number }>(
    '/notifications',
    { params: filters }
  );
};

// Đánh dấu thông báo đã đọc
export const markNotificationAsRead = async (id: string) => {
  return apiClient.patch<Notification>(`/notifications/${id}/read`, {});
};

// Đánh dấu tất cả thông báo đã đọc
export const markAllNotificationsAsRead = async () => {
  return apiClient.patch<{ success: boolean; count: number }>('/notifications/read-all', {});
};

// Xóa thông báo
export const deleteNotification = async (id: string) => {
  return apiClient.delete<{ success: boolean }>(`/notifications/${id}`);
};

// Xóa tất cả thông báo
export const deleteAllNotifications = async () => {
  return apiClient.delete<{ success: boolean; count: number }>('/notifications');
};

// Lấy thông báo mới nhất
export const getLatestNotifications = async (limit: number = 5) => {
  return apiClient.get<Notification[]>('/notifications/latest', { params: { limit } });
};

// Lấy số lượng thông báo chưa đọc
export const getUnreadNotificationsCount = async () => {
  return apiClient.get<{ count: number }>('/notifications/unread-count');
};

// Lấy tùy chọn thông báo của người dùng
export const getNotificationPreferences = async () => {
  return apiClient.get<NotificationPreferences>('/notifications/preferences');
};

// Cập nhật tùy chọn thông báo của người dùng
export const updateNotificationPreferences = async (preferences: Partial<NotificationPreferences>) => {
  return apiClient.put<NotificationPreferences>('/notifications/preferences', preferences);
};