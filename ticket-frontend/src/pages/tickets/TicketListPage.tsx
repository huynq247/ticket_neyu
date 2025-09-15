import React, { useState, useEffect } from 'react';
import { 
  Typography, 
  Table, 
  Tag, 
  Space, 
  Button, 
  Input, 
  Select, 
  DatePicker, 
  Tooltip, 
  Row, 
  Col,
  Badge,
  message,
  Spin
} from 'antd';
import {
  SearchOutlined,
  PlusOutlined,
  EyeOutlined,
  EditOutlined,
  DeleteOutlined,
  ReloadOutlined,
  FilterOutlined,
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import MainLayout from '@/components/layout/MainLayout';
import { TicketStatus, TicketPriority, Ticket } from '@/types';
import ticketService, { TicketFilterParams } from '@/api/ticketService';
import { useSocket } from '@/context/SocketContext';
import './TicketListPage.css';

const { Title } = Typography;
const { Option } = Select;
const { RangePicker } = DatePicker;

// Mock data for testing
const ticketData = Array(30)
  .fill(0)
  .map((_, index) => {
    const id = (1000 + index).toString();
    const statuses = Object.values(TicketStatus);
    const priorities = Object.values(TicketPriority);
    const status = statuses[Math.floor(Math.random() * statuses.length)];
    const priority = priorities[Math.floor(Math.random() * priorities.length)];
    
    return {
      id,
      title: `Sample Ticket #${id}`,
      description: `This is a sample ticket description ${id}`,
      status,
      priority,
      category: Math.random() > 0.5 ? 'Bug' : 'Feature Request',
      assignedTo: Math.random() > 0.6 ? 'John Doe' : 'Jane Smith',
      createdBy: 'Admin User',
      createdAt: new Date(
        Date.now() - Math.floor(Math.random() * 90) * 24 * 60 * 60 * 1000
      ).toISOString(),
      updatedAt: new Date(
        Date.now() - Math.floor(Math.random() * 30) * 24 * 60 * 60 * 1000
      ).toISOString(),
    };
  });

const getStatusColor = (status: string) => {
  switch (status) {
    case TicketStatus.NEW:
      return 'blue';
    case TicketStatus.OPEN:
      return 'cyan';
    case TicketStatus.IN_PROGRESS:
      return 'gold';
    case TicketStatus.PENDING:
      return 'purple';
    case TicketStatus.RESOLVED:
      return 'green';
    case TicketStatus.CLOSED:
      return 'gray';
    default:
      return 'default';
  }
};

const getPriorityColor = (priority: string) => {
  switch (priority) {
    case TicketPriority.LOW:
      return 'green';
    case TicketPriority.MEDIUM:
      return 'orange';
    case TicketPriority.HIGH:
      return 'volcano';
    case TicketPriority.URGENT:
      return 'red';
    default:
      return 'default';
  }
};

const TicketListPage: React.FC = () => {
  const navigate = useNavigate();
  const { registerCallbacks } = useSocket();
  const [searchText, setSearchText] = useState('');
  const [selectedStatus, setSelectedStatus] = useState<string | null>(null);
  const [selectedPriority, setSelectedPriority] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [selectedAssignee, setSelectedAssignee] = useState<string | null>(null);
  const [dateRange, setDateRange] = useState<[Date | null, Date | null]>([null, null]);
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
    total: 0
  });

  useEffect(() => {
    fetchTickets();
    
    // Đăng ký các callback cho sự kiện ticket
    registerCallbacks({
      onTicketCreated: (ticket) => {
        // Thêm ticket mới vào danh sách nếu phù hợp với bộ lọc hiện tại
        setTickets((prevTickets) => {
          // Kiểm tra xem ticket có thỏa mãn các điều kiện lọc không
          if (
            (selectedStatus && ticket.status !== selectedStatus) ||
            (selectedPriority && ticket.priority !== selectedPriority) ||
            (selectedCategory && ticket.category !== selectedCategory) ||
            (selectedAssignee && ticket.assignedTo !== selectedAssignee)
          ) {
            return prevTickets;
          }
          
          // Thêm ticket mới vào đầu danh sách
          return [ticket, ...prevTickets];
        });
        
        // Cập nhật tổng số ticket
        setPagination((prev) => ({
          ...prev,
          total: prev.total + 1
        }));
      },
      onTicketUpdated: (updatedTicket) => {
        // Cập nhật ticket trong danh sách
        setTickets((prevTickets) => {
          return prevTickets.map((ticket) => {
            if (ticket.id === updatedTicket.id) {
              return updatedTicket;
            }
            return ticket;
          });
        });
      },
      onTicketDeleted: (ticketId) => {
        // Xóa ticket khỏi danh sách
        setTickets((prevTickets) => {
          const filteredTickets = prevTickets.filter((ticket) => ticket.id !== ticketId);
          return filteredTickets;
        });
        
        // Cập nhật tổng số ticket
        setPagination((prev) => ({
          ...prev,
          total: prev.total - 1
        }));
      },
      onTicketStatusChanged: (updatedTicket) => {
        // Cập nhật trạng thái ticket trong danh sách
        setTickets((prevTickets) => {
          return prevTickets.map((ticket) => {
            if (ticket.id === updatedTicket.id) {
              return {
                ...ticket,
                status: updatedTicket.status
              };
            }
            return ticket;
          });
        });
      },
      onTicketAssigned: (updatedTicket) => {
        // Cập nhật người được gán vào ticket
        setTickets((prevTickets) => {
          return prevTickets.map((ticket) => {
            if (ticket.id === updatedTicket.id) {
              return {
                ...ticket,
                assignedTo: updatedTicket.assignedTo
              };
            }
            return ticket;
          });
        });
      }
    });
  }, [selectedStatus, selectedPriority, selectedCategory, selectedAssignee, dateRange]);

  const fetchTickets = async () => {
    try {
      setLoading(true);
      
      // Xây dựng tham số filter dựa trên các giá trị đã chọn
      const params: TicketFilterParams = {
        page: pagination.current,
        limit: pagination.pageSize
      };
      
      if (selectedStatus) {
        params.status = selectedStatus as TicketStatus;
      }
      
      if (selectedPriority) {
        params.priority = selectedPriority as TicketPriority;
      }
      
      if (selectedCategory) {
        params.category = selectedCategory;
      }
      
      if (selectedAssignee) {
        params.assignedTo = selectedAssignee;
      }
      
      if (dateRange[0] && dateRange[1]) {
        params.createdAfter = dateRange[0].toISOString();
        params.createdBefore = dateRange[1].toISOString();
      }
      
      const response = await ticketService.getAllTickets(params);
      
      setTickets(response.data.tickets);
      setPagination({
        ...pagination,
        total: response.data.total
      });
      
    } catch (error) {
      console.error('Error fetching tickets:', error);
      message.error('Failed to load tickets');
      
      // Fallback to mock data for development
      setTickets(ticketData);
    } finally {
      setLoading(false);
    }
  };

  const handleViewTicket = (id: string) => {
    navigate(`/tickets/${id}`);
  };

  const handleCreateTicket = () => {
    navigate('/tickets/new');
  };

  const handleReset = () => {
    setSearchText('');
    setSelectedStatus(null);
    setSelectedPriority(null);
    setSelectedCategory(null);
    setSelectedAssignee(null);
    setDateRange([null, null]);
    fetchTickets();
  };
  
  // Hàm refresh danh sách ticket
  const handleRefresh = () => {
    fetchTickets();
    message.success('Danh sách ticket đã được cập nhật');
  };

  const handleDeleteTicket = async (id: string) => {
    try {
      await ticketService.deleteTicket(id);
      message.success('Ticket deleted successfully');
      fetchTickets();
    } catch (error) {
      console.error('Error deleting ticket:', error);
      message.error('Failed to delete ticket');
    }
  };

  const handleTableChange = (pagination: any) => {
    setPagination({
      ...pagination,
      current: pagination.current
    });
    fetchTickets();
  };

  // Filter the data based on search
  const filteredData = tickets.filter((ticket) => {
    const matchesSearch = !searchText 
      || ticket.title.toLowerCase().includes(searchText.toLowerCase())
      || ticket.description.toLowerCase().includes(searchText.toLowerCase())
      || ticket.id.includes(searchText);
    
    return matchesSearch;
  });

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 100,
      render: (id: string) => <span>#{id}</span>,
    },
    {
      title: 'Title',
      dataIndex: 'title',
      key: 'title',
      ellipsis: true,
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      width: 140,
      render: (status: string) => (
        <Tag color={getStatusColor(status)}>
          {status.replace('_', ' ').toUpperCase()}
        </Tag>
      ),
    },
    {
      title: 'Priority',
      dataIndex: 'priority',
      key: 'priority',
      width: 120,
      render: (priority: string) => (
        <Tag color={getPriorityColor(priority)}>
          {priority.toUpperCase()}
        </Tag>
      ),
    },
    {
      title: 'Category',
      dataIndex: 'category',
      key: 'category',
      width: 160,
    },
    {
      title: 'Assigned To',
      dataIndex: 'assignedTo',
      key: 'assignedTo',
      width: 150,
    },
    {
      title: 'Created',
      dataIndex: 'createdAt',
      key: 'createdAt',
      width: 120,
      render: (date: string) => new Date(date).toLocaleDateString(),
    },
    {
      title: 'Actions',
      key: 'action',
      width: 150,
      render: (_: any, record: any) => (
        <Space size="small">
          <Tooltip title="View">
            <Button 
              type="text"
              icon={<EyeOutlined />} 
              onClick={() => handleViewTicket(record.id)} 
            />
          </Tooltip>
          <Tooltip title="Edit">
            <Button 
              type="text"
              icon={<EditOutlined />} 
              onClick={() => navigate(`/tickets/${record.id}/edit`)} 
            />
          </Tooltip>
          <Tooltip title="Delete">
            <Button 
              type="text"
              danger
              icon={<DeleteOutlined />}
              onClick={() => handleDeleteTicket(record.id)}
            />
          </Tooltip>
        </Space>
      ),
    },
  ];

  return (
    <MainLayout>
      <div className="ticket-list-container">
        <div className="ticket-list-header">
          <Title level={2}>Tickets</Title>
          <Button 
            type="primary" 
            icon={<PlusOutlined />}
            onClick={handleCreateTicket}
          >
            Create Ticket
          </Button>
        </div>

        <div className="ticket-list-filters">
          <Row gutter={[16, 16]} align="middle">
            <Col xs={24} sm={8} md={6} lg={6} xl={5}>
              <Input
                placeholder="Search tickets..."
                prefix={<SearchOutlined />}
                value={searchText}
                onChange={(e) => setSearchText(e.target.value)}
                allowClear
              />
            </Col>
            <Col xs={12} sm={8} md={4} lg={4} xl={3}>
              <Select
                placeholder="Status"
                style={{ width: '100%' }}
                value={selectedStatus}
                onChange={setSelectedStatus}
                allowClear
              >
                {Object.values(TicketStatus).map((status) => (
                  <Option key={status} value={status}>
                    <Badge color={getStatusColor(status)} />
                    {status.replace('_', ' ').toUpperCase()}
                  </Option>
                ))}
              </Select>
            </Col>
            <Col xs={12} sm={8} md={4} lg={4} xl={3}>
              <Select
                placeholder="Priority"
                style={{ width: '100%' }}
                value={selectedPriority}
                onChange={setSelectedPriority}
                allowClear
              >
                {Object.values(TicketPriority).map((priority) => (
                  <Option key={priority} value={priority}>
                    <Badge color={getPriorityColor(priority)} />
                    {priority.toUpperCase()}
                  </Option>
                ))}
              </Select>
            </Col>
            <Col xs={12} sm={8} md={5} lg={5} xl={4}>
              <Select
                placeholder="Category"
                style={{ width: '100%' }}
                value={selectedCategory}
                onChange={setSelectedCategory}
                allowClear
              >
                <Option value="Bug">Bug</Option>
                <Option value="Feature Request">Feature Request</Option>
                <Option value="Enhancement">Enhancement</Option>
                <Option value="Support">Support</Option>
              </Select>
            </Col>
            <Col xs={12} sm={8} md={5} lg={5} xl={4}>
              <Select
                placeholder="Assigned To"
                style={{ width: '100%' }}
                value={selectedAssignee}
                onChange={setSelectedAssignee}
                allowClear
              >
                <Option value="John Doe">John Doe</Option>
                <Option value="Jane Smith">Jane Smith</Option>
              </Select>
            </Col>
            <Col xs={24} sm={16} md={8} lg={8} xl={5}>
              <Space>
                <Button 
                  icon={<ReloadOutlined />} 
                  onClick={handleReset}
                >
                  Reset
                </Button>
                <Button 
                  icon={<ReloadOutlined />} 
                  onClick={handleRefresh}
                >
                  Refresh
                </Button>
                <Tooltip title="More Filters">
                  <Button icon={<FilterOutlined />} />
                </Tooltip>
              </Space>
            </Col>
          </Row>
        </div>

        <div className="ticket-list-table">
          <Spin spinning={loading}>
            <Table
              columns={columns}
              dataSource={filteredData}
              rowKey="id"
              pagination={{
                ...pagination,
                showSizeChanger: true,
                showTotal: (total) => `Total ${total} tickets`,
              }}
              onChange={handleTableChange}
            />
          </Spin>
        </div>
      </div>
    </MainLayout>
  );
};

export default TicketListPage;