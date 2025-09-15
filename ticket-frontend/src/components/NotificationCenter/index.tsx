import React, { useState, useEffect } from 'react';
import { notification as antNotification, Badge, Button } from 'antd';
import { BellOutlined } from '@ant-design/icons';
import { useSocket } from '@/context/SocketContext';
import './style.css';

interface NotificationMessage {
  id: string;
  title: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'error';
  timestamp: string;
  read: boolean;
}

const NotificationCenter: React.FC = () => {
  const [notifications, setNotifications] = useState<NotificationMessage[]>([]);
  const [visible, setVisible] = useState(false);
  const { isConnected, registerCallbacks } = useSocket();

  useEffect(() => {
    // Đăng ký callback cho thông báo từ socket
    registerCallbacks({
      onTicketCreated: (ticket) => {
        addNotification({
          id: `ticket-created-${ticket.id}`,
          title: 'New Ticket Created',
          message: `Ticket "${ticket.title}" has been created`,
          type: 'info',
          timestamp: new Date().toISOString(),
          read: false,
        });
      },
      onTicketUpdated: (ticket) => {
        addNotification({
          id: `ticket-updated-${ticket.id}`,
          title: 'Ticket Updated',
          message: `Ticket #${ticket.id} has been updated`,
          type: 'info',
          timestamp: new Date().toISOString(),
          read: false,
        });
      },
      onTicketDeleted: (ticketId) => {
        addNotification({
          id: `ticket-deleted-${ticketId}`,
          title: 'Ticket Deleted',
          message: `Ticket #${ticketId} has been deleted`,
          type: 'warning',
          timestamp: new Date().toISOString(),
          read: false,
        });
      },
      onTicketStatusChanged: (ticket) => {
        addNotification({
          id: `ticket-status-${ticket.id}`,
          title: 'Ticket Status Changed',
          message: `Ticket #${ticket.id} status changed to ${ticket.status}`,
          type: 'info',
          timestamp: new Date().toISOString(),
          read: false,
        });
      },
      onTicketAssigned: (ticket) => {
        addNotification({
          id: `ticket-assigned-${ticket.id}`,
          title: 'Ticket Assigned',
          message: `Ticket #${ticket.id} assigned to ${ticket.assignedTo}`,
          type: 'info',
          timestamp: new Date().toISOString(),
          read: false,
        });
      },
      onCommentAdded: (ticketId, comment) => {
        addNotification({
          id: `comment-added-${ticketId}-${comment.id}`,
          title: 'New Comment',
          message: `New comment on Ticket #${ticketId}`,
          type: 'info',
          timestamp: new Date().toISOString(),
          read: false,
        });
      },
      onNotification: (message) => {
        addNotification({
          id: `notification-${Date.now()}`,
          title: 'Notification',
          message,
          type: 'info',
          timestamp: new Date().toISOString(),
          read: false,
        });
      },
    });
  }, [registerCallbacks]);

  const addNotification = (notification: NotificationMessage) => {
    setNotifications((prev) => [notification, ...prev]);
    
    // Hiển thị thông báo popup
    showNotificationPopup(notification);
  };

  const showNotificationPopup = (notification: NotificationMessage) => {
    antNotification[notification.type]({
      message: notification.title,
      description: notification.message,
      placement: 'topRight',
    });
  };

  const markAsRead = (id: string) => {
    setNotifications((prev) =>
      prev.map((item) => (item.id === id ? { ...item, read: true } : item))
    );
  };

  const markAllAsRead = () => {
    setNotifications((prev) =>
      prev.map((item) => ({ ...item, read: true }))
    );
  };

  const toggleNotificationPanel = () => {
    setVisible(!visible);
  };

  const unreadCount = notifications.filter((item) => !item.read).length;

  return (
    <div className="notification-center">
      <Badge count={unreadCount} overflowCount={99}>
        <Button
          className="notification-button"
          icon={<BellOutlined />}
          type="text"
          onClick={toggleNotificationPanel}
        />
      </Badge>

      {visible && (
        <div className="notification-panel">
          <div className="notification-header">
            <h3>Notifications</h3>
            {unreadCount > 0 && (
              <Button type="link" onClick={markAllAsRead}>
                Mark all as read
              </Button>
            )}
          </div>

          <div className="notification-list">
            {notifications.length === 0 ? (
              <div className="empty-notification">No notifications</div>
            ) : (
              notifications.map((item) => (
                <div
                  key={item.id}
                  className={`notification-item ${!item.read ? 'unread' : ''}`}
                  onClick={() => markAsRead(item.id)}
                >
                  <div className="notification-content">
                    <div className="notification-title">{item.title}</div>
                    <div className="notification-message">{item.message}</div>
                    <div className="notification-time">
                      {new Date(item.timestamp).toLocaleString()}
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default NotificationCenter;