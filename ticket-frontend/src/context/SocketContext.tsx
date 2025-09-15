import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import socketService, { SocketCallbacks } from '@/services/socketService';
import { message } from 'antd';

interface SocketContextProps {
  isConnected: boolean;
  connectSocket: () => void;
  disconnectSocket: () => void;
  registerCallbacks: (callbacks: SocketCallbacks) => void;
  joinTicketRoom: (ticketId: string) => void;
  leaveTicketRoom: (ticketId: string) => void;
}

const SocketContext = createContext<SocketContextProps | undefined>(undefined);

interface SocketProviderProps {
  children: ReactNode;
}

export const SocketProvider: React.FC<SocketProviderProps> = ({ children }) => {
  const [isConnected, setIsConnected] = useState(false);

  // Kết nối socket khi component mount
  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    
    // Chỉ kết nối nếu người dùng đã đăng nhập
    if (token) {
      connectSocket();
      
      // Đăng ký các callback mặc định
      const defaultCallbacks: SocketCallbacks = {
        onTicketCreated: (ticket) => {
          message.info(`Ticket mới đã được tạo: ${ticket.title}`);
        },
        onTicketUpdated: (ticket) => {
          message.info(`Ticket đã được cập nhật: ${ticket.title}`);
        },
        onTicketDeleted: (ticketId) => {
          message.warning(`Ticket #${ticketId} đã bị xóa`);
        },
        onTicketAssigned: (ticket) => {
          message.info(`Ticket đã được gán cho: ${ticket.assignedTo}`);
        },
        onTicketStatusChanged: (ticket) => {
          message.info(`Trạng thái ticket đã thay đổi thành: ${ticket.status}`);
        },
        onNotification: (msg) => {
          message.info(msg);
        }
      };
      
      socketService.registerCallbacks(defaultCallbacks);
      
      // Clean up khi component unmount
      return () => {
        disconnectSocket();
      };
    }
  }, []);

  // Kiểm tra trạng thái kết nối mỗi 5 giây
  useEffect(() => {
    const interval = setInterval(() => {
      setIsConnected(socketService.isConnected());
    }, 5000);
    
    return () => clearInterval(interval);
  }, []);

  const connectSocket = () => {
    socketService.connect();
    setIsConnected(socketService.isConnected());
  };

  const disconnectSocket = () => {
    socketService.disconnect();
    setIsConnected(false);
  };

  const registerCallbacks = (callbacks: SocketCallbacks) => {
    socketService.registerCallbacks(callbacks);
  };

  const joinTicketRoom = (ticketId: string) => {
    socketService.joinTicketRoom(ticketId);
  };

  const leaveTicketRoom = (ticketId: string) => {
    socketService.leaveTicketRoom(ticketId);
  };

  return (
    <SocketContext.Provider
      value={{
        isConnected,
        connectSocket,
        disconnectSocket,
        registerCallbacks,
        joinTicketRoom,
        leaveTicketRoom
      }}
    >
      {children}
    </SocketContext.Provider>
  );
};

// Hook để sử dụng SocketContext
export const useSocket = (): SocketContextProps => {
  const context = useContext(SocketContext);
  
  if (context === undefined) {
    throw new Error('useSocket must be used within a SocketProvider');
  }
  
  return context;
};