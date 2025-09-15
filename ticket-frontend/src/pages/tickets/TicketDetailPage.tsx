import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Typography,
  Card,
  Tag,
  Descriptions,
  Avatar,
  Button,
  Space,
  Tabs,
  Timeline,
  List,
  Form,
  Input,
  Select,
  message,
  Modal,
  Row,
  Col,
  Spin
} from 'antd';
import { 
  UserOutlined,
  CommentOutlined,
  HistoryOutlined,
  EditOutlined,
  DeleteOutlined,
  ExclamationCircleOutlined,
} from '@ant-design/icons';
import MainLayout from '@/components/layout/MainLayout';
import { TicketStatus, TicketPriority, Ticket, Comment as TicketComment } from '@/types';
import ticketService from '@/api/ticketService';
import { useSocket } from '@/context/SocketContext';
import './TicketDetailPage.css';

const { Title, Text, Paragraph } = Typography;
const { TabPane } = Tabs;
const { TextArea } = Input;
const { Option } = Select;
const { confirm } = Modal;

// Mock data for activity history (will be replaced with real data from API)
const activityHistory = [
  {
    id: 1,
    action: 'Ticket created',
    user: 'John Doe',
    timestamp: '2023-03-15T10:30:00Z',
  },
  {
    id: 2,
    action: 'Status changed from OPEN to IN_PROGRESS',
    user: 'Jane Smith',
    timestamp: '2023-03-15T14:45:00Z',
  },
  {
    id: 3,
    action: 'Comment added',
    user: 'John Doe',
    timestamp: '2023-03-16T09:15:00Z',
  },
  {
    id: 4,
    action: 'Priority changed from MEDIUM to HIGH',
    user: 'Admin User',
    timestamp: '2023-03-16T11:20:00Z',
  },
  {
    id: 5,
    action: 'Attachment added: screenshot.png',
    user: 'Jane Smith',
    timestamp: '2023-03-17T08:40:00Z',
  },
];

// Function to determine the color of the status tag
const getStatusColor = (status: string) => {
  switch (status) {
    case TicketStatus.OPEN:
      return 'blue';
    case TicketStatus.IN_PROGRESS:
      return 'orange';
    case TicketStatus.RESOLVED:
      return 'green';
    case TicketStatus.CLOSED:
      return 'default';
    case TicketStatus.PENDING:
      return 'purple';
    default:
      return 'default';
  }
};

// Function to determine the color of the priority tag
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

const TicketDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { registerCallbacks, joinTicketRoom, leaveTicketRoom } = useSocket();
  const [ticket, setTicket] = useState<Ticket>({} as Ticket);
  const [isEditing, setIsEditing] = useState(false);
  const [commentValue, setCommentValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [form] = Form.useForm();

  // Fetch ticket data when the component mounts
  useEffect(() => {
    if (id) {
      fetchTicketData();
      
      // Join the ticket's socket room
      joinTicketRoom(id);
      
      // Register callbacks for real-time events
      registerCallbacks({
        onTicketUpdated: handleTicketUpdated,
        onCommentAdded: handleCommentAdded,
      });
    }
    
    // Clean up when component unmounts
    return () => {
      if (id) {
        leaveTicketRoom(id);
      }
    };
  }, [id]);

  // Initialize form values when ticket data is available
  useEffect(() => {
    if (ticket && Object.keys(ticket).length > 0) {
      form.setFieldsValue({
        title: ticket.title,
        description: ticket.description,
        status: ticket.status,
        priority: ticket.priority,
        assignedTo: ticket.assignedTo,
        category: ticket.category,
      });
    }
  }, [ticket, form]);

  const fetchTicketData = async () => {
    if (!id) return;
    
    try {
      setLoading(true);
      const response = await ticketService.getTicketById(id);
      setTicket(response.data);
    } catch (error) {
      console.error('Error fetching ticket data:', error);
      message.error('Failed to load ticket data');
    } finally {
      setLoading(false);
    }
  };

  const handleTicketUpdated = (updatedTicket: Ticket) => {
    if (updatedTicket.id === ticket.id) {
      setTicket(updatedTicket);
      message.info('This ticket has been updated');
    }
  };

  const handleCommentAdded = (ticketId: string, newComment: TicketComment) => {
    if (ticketId === id) {
      setTicket((prevTicket) => ({
        ...prevTicket,
        comments: [...(prevTicket.comments || []), newComment],
      }));
      message.info('New comment added');
    }
  };

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const handleStatusChange = async (newStatus: TicketStatus) => {
    if (!id) return;
    
    try {
      await ticketService.changeStatus(id, newStatus);
      message.success('Status updated successfully');
    } catch (error) {
      console.error('Error updating status:', error);
      message.error('Failed to update status');
    }
  };

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleCancel = () => {
    setIsEditing(false);
    form.resetFields();
  };

  const handleSave = async (values: any) => {
    if (!id) return;
    
    try {
      await ticketService.updateTicket(id, values);
      setIsEditing(false);
      message.success('Ticket updated successfully');
      
      // Update local state
      setTicket((prevTicket) => ({
        ...prevTicket,
        ...values,
      }));
    } catch (error) {
      console.error('Error updating ticket:', error);
      message.error('Failed to update ticket');
    }
  };

  const handleCommentSubmit = async () => {
    if (!commentValue.trim() || !id) {
      return;
    }

    try {
      const response = await ticketService.addComment(id, commentValue);
      
      // Cập nhật dữ liệu local - trong trường hợp real-time chưa hoạt động
      const newComment: TicketComment = {
        id: response.data.id || `c${ticket.comments?.length ? ticket.comments.length + 1 : 1}`,
        content: commentValue,
        createdBy: 'Current User', // Trong ứng dụng thực, lấy từ context người dùng hiện tại
        createdAt: new Date().toISOString(),
      };
      
      setTicket((prevTicket) => ({
        ...prevTicket,
        comments: [...(prevTicket.comments || []), newComment],
      }));
      
      setCommentValue('');
      message.success('Comment added successfully');
    } catch (error) {
      console.error('Error adding comment:', error);
      message.error('Failed to add comment');
    }
  };

  const handleDelete = () => {
    confirm({
      title: 'Are you sure you want to delete this ticket?',
      icon: <ExclamationCircleOutlined />,
      content: 'This action cannot be undone.',
      okText: 'Yes',
      okType: 'danger',
      cancelText: 'No',
      onOk: async () => {
        try {
          // In a real application, you would delete the ticket through the API
          // await ticketService.deleteTicket(ticket.id);
          
          message.success('Ticket deleted successfully');
          navigate('/tickets');
        } catch (error) {
          console.error('Error deleting ticket:', error);
          message.error('Failed to delete ticket');
        }
      },
    });
  };

  return (
    <MainLayout>
      <div className="ticket-detail-container">
        <Spin spinning={loading}>
        <div className="ticket-header">
          <div className="ticket-title-section">
            <div className="ticket-title">
              <Title level={2}>Ticket #{ticket.id}</Title>
              <div className="ticket-tags">
                <Tag color={getStatusColor(ticket.status)}>
                  {ticket.status?.replace('_', ' ').toUpperCase()}
                </Tag>
                <Tag color={getPriorityColor(ticket.priority)}>
                  {ticket.priority?.replace('_', ' ').toUpperCase()}
                </Tag>
              </div>
            </div>
            <div className="ticket-actions">
              <Space>
                <Button 
                  type="primary" 
                  icon={<EditOutlined />} 
                  onClick={handleEdit}
                  disabled={isEditing}
                >
                  Edit
                </Button>
                <Button 
                  danger 
                  icon={<DeleteOutlined />} 
                  onClick={handleDelete}
                >
                  Delete
                </Button>
              </Space>
            </div>
          </div>
          
          {isEditing ? (
            <Card className="edit-form-card">
              <Form
                form={form}
                layout="vertical"
                onFinish={handleSave}
              >
                <Row gutter={16}>
                  <Col span={24}>
                    <Form.Item
                      name="title"
                      label="Title"
                      rules={[{ required: true, message: 'Please enter a title' }]}
                    >
                      <Input />
                    </Form.Item>
                  </Col>
                </Row>
                <Row gutter={16}>
                  <Col span={24}>
                    <Form.Item
                      name="description"
                      label="Description"
                      rules={[{ required: true, message: 'Please enter a description' }]}
                    >
                      <TextArea rows={4} />
                    </Form.Item>
                  </Col>
                </Row>
                <Row gutter={16}>
                  <Col span={8}>
                    <Form.Item
                      name="status"
                      label="Status"
                      rules={[{ required: true, message: 'Please select a status' }]}
                    >
                      <Select>
                        {Object.values(TicketStatus).map((status) => (
                          <Option key={status} value={status}>
                            {status.replace('_', ' ')}
                          </Option>
                        ))}
                      </Select>
                    </Form.Item>
                  </Col>
                  <Col span={8}>
                    <Form.Item
                      name="priority"
                      label="Priority"
                      rules={[{ required: true, message: 'Please select a priority' }]}
                    >
                      <Select>
                        {Object.values(TicketPriority).map((priority) => (
                          <Option key={priority} value={priority}>
                            {priority}
                          </Option>
                        ))}
                      </Select>
                    </Form.Item>
                  </Col>
                  <Col span={8}>
                    <Form.Item
                      name="assignedTo"
                      label="Assigned To"
                    >
                      <Select>
                        <Option value="John Doe">John Doe</Option>
                        <Option value="Jane Smith">Jane Smith</Option>
                        <Option value="Admin User">Admin User</Option>
                      </Select>
                    </Form.Item>
                  </Col>
                </Row>
                <Row gutter={16}>
                  <Col span={24}>
                    <Form.Item
                      name="category"
                      label="Category"
                    >
                      <Select>
                        <Option value="Bug">Bug</Option>
                        <Option value="Feature">Feature</Option>
                        <Option value="Support">Support</Option>
                        <Option value="Other">Other</Option>
                      </Select>
                    </Form.Item>
                  </Col>
                </Row>
                <Row gutter={16}>
                  <Col span={24}>
                    <div className="form-actions">
                      <Space>
                        <Button type="primary" htmlType="submit">
                          Save
                        </Button>
                        <Button onClick={handleCancel}>
                          Cancel
                        </Button>
                      </Space>
                    </div>
                  </Col>
                </Row>
              </Form>
            </Card>
          ) : (
            <Card className="ticket-info-card">
              <Descriptions bordered column={{ xxl: 4, xl: 3, lg: 3, md: 3, sm: 2, xs: 1 }}>
                <Descriptions.Item label="Title" span={3}>
                  {ticket.title}
                </Descriptions.Item>
                <Descriptions.Item label="Description" span={3}>
                  <Paragraph>
                    {ticket.description}
                  </Paragraph>
                </Descriptions.Item>
                  <Descriptions.Item label="Status">
                  <Tag 
                    color={getStatusColor(ticket.status)}
                    style={{ cursor: 'pointer' }}
                    onClick={() => handleStatusChange(
                      ticket.status === TicketStatus.OPEN 
                        ? TicketStatus.IN_PROGRESS 
                        : ticket.status === TicketStatus.IN_PROGRESS 
                          ? TicketStatus.RESOLVED 
                          : TicketStatus.OPEN
                    )}
                  >
                    {ticket.status?.replace('_', ' ')}
                  </Tag>
                </Descriptions.Item>
                <Descriptions.Item label="Priority">
                  <Tag color={getPriorityColor(ticket.priority)}>
                    {ticket.priority}
                  </Tag>
                </Descriptions.Item>
                <Descriptions.Item label="Created By">
                  {ticket.createdBy}
                </Descriptions.Item>
                <Descriptions.Item label="Created At">
                  {ticket.createdAt ? new Date(ticket.createdAt).toLocaleString() : ''}
                </Descriptions.Item>
                <Descriptions.Item label="Updated At">
                  {ticket.updatedAt ? new Date(ticket.updatedAt).toLocaleString() : ''}
                </Descriptions.Item>
                <Descriptions.Item label="Assigned To">
                  {ticket.assignedTo || 'Unassigned'}
                </Descriptions.Item>
                <Descriptions.Item label="Category">
                  {ticket.category || 'Uncategorized'}
                </Descriptions.Item>
              </Descriptions>
            </Card>
          )}
        </div>
        
        <div className="ticket-content">
          <Tabs defaultActiveKey="comments">
            <TabPane
              tab={
                <span>
                  <CommentOutlined />
                  Comments
                </span>
              }
              key="comments"
            >
              <div className="comments-section">
                <div className="comment-list">
                  {ticket.comments && ticket.comments.length > 0 ? (
                    <List
                      itemLayout="horizontal"
                      dataSource={ticket.comments}
                      renderItem={(comment) => (
                        <List.Item key={comment.id}>
                          <List.Item.Meta
                            avatar={<Avatar icon={<UserOutlined />} />}
                            title={comment.createdBy}
                            description={
                              <>
                                <div>{comment.content}</div>
                                <div className="comment-date">{new Date(comment.createdAt).toLocaleString()}</div>
                              </>
                            }
                          />
                        </List.Item>
                      )}
                    />
                  ) : (
                    <div className="no-comments">
                      <Text type="secondary">No comments yet</Text>
                    </div>
                  )}
                </div>
                
                <div className="comment-form">
                  <TextArea 
                    rows={4} 
                    placeholder="Add a comment..."
                    value={commentValue}
                    onChange={(e) => setCommentValue(e.target.value)}
                  />
                  <Button 
                    type="primary" 
                    onClick={handleCommentSubmit}
                    disabled={!commentValue.trim()}
                    style={{ marginTop: 16 }}
                  >
                    Add Comment
                  </Button>
                </div>
              </div>
            </TabPane>
            <TabPane
              tab={
                <span>
                  <HistoryOutlined />
                  Activity
                </span>
              }
              key="activity"
            >
              <div className="activity-section">
                <Timeline>
                  {activityHistory.map((activity) => (
                    <Timeline.Item key={activity.id}>
                      <p>{activity.action}</p>
                      <p className="activity-meta">
                        <Text type="secondary">
                          By {activity.user} on {
                            new Date(activity.timestamp).toLocaleString()
                          }
                        </Text>
                      </p>
                    </Timeline.Item>
                  ))}
                </Timeline>
              </div>
            </TabPane>
          </Tabs>
        </div>
        </Spin>
      </div>
    </MainLayout>
  );
};

export default TicketDetailPage;