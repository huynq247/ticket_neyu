import { io, Socket } from 'socket.io-client';
import { Ticket, Comment } from '@/types';

// Các loại event sẽ nhận từ server
export enum SocketEvent {
  CONNECT = 'connect',
  DISCONNECT = 'disconnect',
  CONNECT_ERROR = 'connect_error',
  TICKET_CREATED = 'ticket:created',
  TICKET_UPDATED = 'ticket:updated',
  TICKET_DELETED = 'ticket:deleted',
  TICKET_ASSIGNED = 'ticket:assigned',
  TICKET_STATUS_CHANGED = 'ticket:status_changed',
  COMMENT_ADDED = 'comment:added',
  NOTIFICATION = 'notification'
}

// Interface cho các callback function
export interface SocketCallbacks {
  onTicketCreated?: (ticket: Ticket) => void;
  onTicketUpdated?: (ticket: Ticket) => void;
  onTicketDeleted?: (ticketId: string) => void;
  onTicketAssigned?: (ticket: Ticket) => void;
  onTicketStatusChanged?: (ticket: Ticket) => void;
  onCommentAdded?: (ticketId: string, comment: Comment) => void;
  onNotification?: (message: string) => void;
}

class SocketService {
  private socket: Socket | null = null;
  private callbacks: SocketCallbacks = {};

  // Kết nối đến socket server
  connect() {
    if (this.socket) return;

    const token = localStorage.getItem('auth_token');
    const baseURL = import.meta.env.VITE_SOCKET_URL || 'http://localhost:8000';

    this.socket = io(baseURL, {
      auth: {
        token
      },
      autoConnect: true,
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
    });

    this.setupEventListeners();
  }

  // Ngắt kết nối socket
  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  // Thiết lập các event listener
  private setupEventListeners() {
    if (!this.socket) return;

    this.socket.on(SocketEvent.CONNECT, () => {
      console.log('Connected to socket server');
    });

    this.socket.on(SocketEvent.DISCONNECT, (reason) => {
      console.log(`Disconnected: ${reason}`);
    });

    this.socket.on(SocketEvent.CONNECT_ERROR, (error) => {
      console.error('Socket connection error:', error);
    });

    // Lắng nghe sự kiện ticket được tạo mới
    this.socket.on(SocketEvent.TICKET_CREATED, (ticket: Ticket) => {
      if (this.callbacks.onTicketCreated) {
        this.callbacks.onTicketCreated(ticket);
      }
    });

    // Lắng nghe sự kiện ticket được cập nhật
    this.socket.on(SocketEvent.TICKET_UPDATED, (ticket: Ticket) => {
      if (this.callbacks.onTicketUpdated) {
        this.callbacks.onTicketUpdated(ticket);
      }
    });

    // Lắng nghe sự kiện ticket bị xóa
    this.socket.on(SocketEvent.TICKET_DELETED, (ticketId: string) => {
      if (this.callbacks.onTicketDeleted) {
        this.callbacks.onTicketDeleted(ticketId);
      }
    });

    // Lắng nghe sự kiện ticket được gán cho ai đó
    this.socket.on(SocketEvent.TICKET_ASSIGNED, (ticket: Ticket) => {
      if (this.callbacks.onTicketAssigned) {
        this.callbacks.onTicketAssigned(ticket);
      }
    });

    // Lắng nghe sự kiện trạng thái ticket thay đổi
    this.socket.on(SocketEvent.TICKET_STATUS_CHANGED, (ticket: Ticket) => {
      if (this.callbacks.onTicketStatusChanged) {
        this.callbacks.onTicketStatusChanged(ticket);
      }
    });

    // Lắng nghe sự kiện comment mới được thêm vào
    this.socket.on(SocketEvent.COMMENT_ADDED, (data: { ticketId: string, comment: Comment }) => {
      if (this.callbacks.onCommentAdded) {
        this.callbacks.onCommentAdded(data.ticketId, data.comment);
      }
    });

    // Lắng nghe các thông báo từ server
    this.socket.on(SocketEvent.NOTIFICATION, (message: string) => {
      if (this.callbacks.onNotification) {
        this.callbacks.onNotification(message);
      }
    });
  }

  // Đăng ký các callback function
  registerCallbacks(callbacks: SocketCallbacks) {
    this.callbacks = { ...this.callbacks, ...callbacks };
  }

  // Gỡ bỏ các callback function
  unregisterCallbacks() {
    this.callbacks = {};
  }

  // Kiểm tra trạng thái kết nối
  isConnected(): boolean {
    return this.socket?.connected || false;
  }

  // Tham gia vào phòng của một ticket cụ thể
  joinTicketRoom(ticketId: string) {
    if (this.socket && this.socket.connected) {
      this.socket.emit('join:ticket', ticketId);
    }
  }

  // Rời khỏi phòng của một ticket cụ thể
  leaveTicketRoom(ticketId: string) {
    if (this.socket && this.socket.connected) {
      this.socket.emit('leave:ticket', ticketId);
    }
  }
}

// Tạo instance singleton
const socketService = new SocketService();

export default socketService;