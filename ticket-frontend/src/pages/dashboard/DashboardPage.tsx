import React from 'react';
import { Typography, Row, Col, Card, Statistic, List, Tag, Divider } from 'antd';
import {
  TeamOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  FileOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined,
} from '@ant-design/icons';
import MainLayout from '@/components/layout/MainLayout';
import './DashboardPage.css';

const { Title, Text } = Typography;

// Mock data for testing
const recentTickets = [
  {
    id: '1',
    title: 'System login issue after update',
    status: 'open',
    priority: 'high',
    createdAt: '2025-09-12T10:30:00Z',
    assignedTo: 'John Doe',
  },
  {
    id: '2',
    title: 'New feature request: Export to PDF',
    status: 'in_progress',
    priority: 'medium',
    createdAt: '2025-09-11T15:45:00Z',
    assignedTo: 'Jane Smith',
  },
  {
    id: '3',
    title: 'Dashboard loading slow in Firefox',
    status: 'pending',
    priority: 'medium',
    createdAt: '2025-09-10T09:15:00Z',
    assignedTo: 'Mike Johnson',
  },
  {
    id: '4',
    title: 'Cannot update user profile picture',
    status: 'resolved',
    priority: 'low',
    createdAt: '2025-09-09T14:20:00Z',
    assignedTo: 'Sarah Williams',
  },
  {
    id: '5',
    title: 'Add support for multi-factor authentication',
    status: 'open',
    priority: 'high',
    createdAt: '2025-09-08T11:10:00Z',
    assignedTo: 'John Doe',
  },
];

const getStatusColor = (status: string) => {
  switch (status) {
    case 'open':
      return 'blue';
    case 'in_progress':
      return 'gold';
    case 'pending':
      return 'purple';
    case 'resolved':
      return 'green';
    case 'closed':
      return 'gray';
    default:
      return 'default';
  }
};

const getPriorityColor = (priority: string) => {
  switch (priority) {
    case 'high':
      return 'red';
    case 'medium':
      return 'orange';
    case 'low':
      return 'green';
    default:
      return 'default';
  }
};

const DashboardPage: React.FC = () => {
  return (
    <MainLayout>
      <div className="dashboard-container">
        <Title level={2}>Dashboard</Title>
        <Text type="secondary">Welcome back! Here's what's happening today.</Text>

        <div className="dashboard-stats">
          <Row gutter={[16, 16]} className="stats-row">
            <Col xs={24} sm={12} md={6}>
              <Card>
                <Statistic
                  title="Total Tickets"
                  value={248}
                  prefix={<FileOutlined />}
                />
              </Card>
            </Col>
            <Col xs={24} sm={12} md={6}>
              <Card>
                <Statistic
                  title="Open Tickets"
                  value={42}
                  valueStyle={{ color: '#1677ff' }}
                  prefix={<ClockCircleOutlined />}
                />
              </Card>
            </Col>
            <Col xs={24} sm={12} md={6}>
              <Card>
                <Statistic
                  title="Resolved Today"
                  value={12}
                  valueStyle={{ color: '#3f8600' }}
                  prefix={<CheckCircleOutlined />}
                  suffix={<ArrowUpOutlined />}
                />
              </Card>
            </Col>
            <Col xs={24} sm={12} md={6}>
              <Card>
                <Statistic
                  title="Team Members"
                  value={8}
                  prefix={<TeamOutlined />}
                />
              </Card>
            </Col>
          </Row>
        </div>

        <Divider orientation="left">Recent Tickets</Divider>
        
        <Card className="recent-tickets-card">
          <List
            itemLayout="horizontal"
            dataSource={recentTickets}
            renderItem={(ticket) => (
              <List.Item
                actions={[<a href={`/tickets/${ticket.id}`}>View</a>]}
              >
                <List.Item.Meta
                  title={
                    <a href={`/tickets/${ticket.id}`}>
                      {ticket.title}
                    </a>
                  }
                  description={
                    <>
                      <Tag color={getStatusColor(ticket.status)}>
                        {ticket.status.replace('_', ' ').toUpperCase()}
                      </Tag>
                      <Tag color={getPriorityColor(ticket.priority)}>
                        {ticket.priority.toUpperCase()}
                      </Tag>
                      <span className="ticket-meta">
                        Assigned to: {ticket.assignedTo}
                      </span>
                      <span className="ticket-meta">
                        Created: {new Date(ticket.createdAt).toLocaleDateString()}
                      </span>
                    </>
                  }
                />
              </List.Item>
            )}
          />
        </Card>
      </div>
    </MainLayout>
  );
};

export default DashboardPage;