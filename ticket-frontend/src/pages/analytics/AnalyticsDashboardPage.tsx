import React, { useState, useEffect } from 'react';
import {
  Typography,
  Card,
  Row,
  Col,
  Statistic,
  Select,
  Button,
  Table,
  Tag,
  Spin,
  Empty,
  DatePicker,
  Divider,
  message,
} from 'antd';
import {
  BarChartOutlined,
  LineChartOutlined,
  PieChartOutlined,
  ReloadOutlined,
  DownloadOutlined,
  FilterOutlined,
} from '@ant-design/icons';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title as ChartTitle,
  Tooltip as ChartTooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Line, Bar, Pie, Doughnut } from 'react-chartjs-2';
import MainLayout from '@/components/layout/MainLayout';
import { TicketStatus, TicketPriority, TicketStatistics, DashboardData } from '@/types';
import analyticsService from '@/api/analyticsService';
import './AnalyticsDashboardPage.css';

const { Title, Text } = Typography;
const { Option } = Select;
const { RangePicker } = DatePicker;

// Đăng ký các component của ChartJS
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  ChartTitle,
  ChartTooltip,
  Legend,
  Filler
);

// Cấu hình theme cho charts
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top' as const,
    },
  },
};

// Mock statistics data for testing
const mockStatistics: TicketStatistics = {
  totalTickets: 124,
  ticketsByStatus: {
    [TicketStatus.NEW]: 15,
    [TicketStatus.OPEN]: 22,
    [TicketStatus.IN_PROGRESS]: 35,
    [TicketStatus.PENDING]: 18,
    [TicketStatus.RESOLVED]: 24,
    [TicketStatus.CLOSED]: 10,
  },
  ticketsByPriority: {
    [TicketPriority.LOW]: 30,
    [TicketPriority.MEDIUM]: 45,
    [TicketPriority.HIGH]: 38,
    [TicketPriority.URGENT]: 11,
  },
  ticketsByCategory: {
    'Bug': 52,
    'Feature Request': 28,
    'Enhancement': 32,
    'Support': 12,
  },
  ticketsTrend: [
    { date: '2025-08-01', count: 5 },
    { date: '2025-08-02', count: 8 },
    { date: '2025-08-03', count: 3 },
    { date: '2025-08-04', count: 10 },
    { date: '2025-08-05', count: 7 },
    { date: '2025-08-06', count: 11 },
    { date: '2025-08-07', count: 9 },
  ],
  averageResolutionTime: 26.5, // hours
  topAssignees: [
    { name: 'John Doe', count: 35 },
    { name: 'Jane Smith', count: 28 },
    { name: 'Alice Johnson', count: 22 },
    { name: 'Bob Williams', count: 18 },
    { name: 'Charlie Brown', count: 12 },
  ],
};

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

const AnalyticsDashboardPage: React.FC = () => {
  const [statistics, setStatistics] = useState<TicketStatistics>(mockStatistics);
  const [loading, setLoading] = useState(false);
  const [timeRange, setTimeRange] = useState('week');

  // Fetch statistics when the component mounts or when timeRange changes
  useEffect(() => {
    // In a real application, you would fetch the statistics from the API
    fetchStatistics();
  }, [timeRange]);

  const fetchStatistics = async () => {
    setLoading(true);
    try {
      // Sử dụng analyticsService để lấy dữ liệu thống kê
      const response = await analyticsService.getDashboardData();
      
      // Có thể sử dụng các API khác có tham số
      // const timeAnalysis = await analyticsService.getTimeAnalysis({
      //   timeRange: timeRange
      // });
      
      // Trong môi trường thực tế, chúng ta sẽ sử dụng dữ liệu từ API
      // Nếu API đã hoạt động, hãy bỏ comment dòng dưới đây
      // const transformedData = transformApiDataToStatistics(response.data);
      // setStatistics(transformedData);
      
      // Nhưng hiện tại, chúng ta vẫn sử dụng dữ liệu mẫu
      setStatistics(mockStatistics);
      message.success('Dữ liệu thống kê đã được cập nhật');
    } catch (error) {
      console.error('Error fetching statistics:', error);
      message.error('Không thể tải dữ liệu thống kê');
    } finally {
      setLoading(false);
    }
  };

  // Hàm để chuyển đổi dữ liệu từ API sang định dạng TicketStatistics
  const transformApiDataToStatistics = (apiData: DashboardData): TicketStatistics => {
    return {
      totalTickets: apiData.ticketsCount.total,
      ticketsByStatus: {
        [TicketStatus.NEW]: apiData.ticketsCount.new,
        [TicketStatus.OPEN]: apiData.ticketsCount.open,
        [TicketStatus.IN_PROGRESS]: apiData.ticketsCount.inProgress,
        [TicketStatus.PENDING]: apiData.ticketsCount.pending,
        [TicketStatus.RESOLVED]: apiData.ticketsCount.resolved,
        [TicketStatus.CLOSED]: apiData.ticketsCount.closed
      },
      ticketsByPriority: apiData.priorityDistribution.reduce((acc, item) => {
        acc[item.priority] = item.count;
        return acc;
      }, {} as Record<string, number>),
      ticketsByCategory: apiData.categoryDistribution.reduce((acc, item) => {
        acc[item.category] = item.count;
        return acc;
      }, {} as Record<string, number>),
      ticketsTrend: apiData.ticketsOverTime.map(item => ({
        date: item.date,
        count: item.created
      })),
      averageResolutionTime: 8.5, // Giả sử dữ liệu API không có trường này
      topAssignees: [
        { name: 'John Doe', count: 25 },
        { name: 'Jane Smith', count: 18 },
        { name: 'Bob Johnson', count: 15 }
      ]
    };
  };

  const handleTimeRangeChange = (value: string) => {
    setTimeRange(value);
  };

  const handleRefresh = () => {
    fetchStatistics();
  };

  const statusColumns = [
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={getStatusColor(status)}>
          {status.replace('_', ' ').toUpperCase()}
        </Tag>
      ),
    },
    {
      title: 'Count',
      dataIndex: 'count',
      key: 'count',
    },
    {
      title: 'Percentage',
      dataIndex: 'percentage',
      key: 'percentage',
      render: (percentage: number) => `${percentage.toFixed(1)}%`,
    },
  ];

  const statusData = Object.entries(statistics.ticketsByStatus).map(([status, count]) => ({
    status,
    count,
    percentage: (count / statistics.totalTickets) * 100,
  }));

  const priorityColumns = [
    {
      title: 'Priority',
      dataIndex: 'priority',
      key: 'priority',
      render: (priority: string) => (
        <Tag color={getPriorityColor(priority)}>
          {priority.toUpperCase()}
        </Tag>
      ),
    },
    {
      title: 'Count',
      dataIndex: 'count',
      key: 'count',
    },
    {
      title: 'Percentage',
      dataIndex: 'percentage',
      key: 'percentage',
      render: (percentage: number) => `${percentage.toFixed(1)}%`,
    },
  ];

  const priorityData = Object.entries(statistics.ticketsByPriority).map(([priority, count]) => ({
    priority,
    count,
    percentage: (count / statistics.totalTickets) * 100,
  }));

  const topAssigneesColumns = [
    {
      title: 'Assignee',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Tickets',
      dataIndex: 'count',
      key: 'count',
    },
    {
      title: 'Percentage',
      dataIndex: 'percentage',
      key: 'percentage',
      render: (percentage: number) => `${percentage.toFixed(1)}%`,
    },
  ];

  const topAssigneesData = statistics.topAssignees.map((assignee) => ({
    ...assignee,
    percentage: (assignee.count / statistics.totalTickets) * 100,
  }));

  return (
    <MainLayout>
      <div className="analytics-container">
        {/* Header */}
        <div className="analytics-header">
          <Title level={2}>Analytics Dashboard</Title>
          <div className="analytics-controls">
            <Select
              defaultValue="week"
              style={{ width: 120, marginRight: 16 }}
              onChange={handleTimeRangeChange}
            >
              <Option value="day">Today</Option>
              <Option value="week">This Week</Option>
              <Option value="month">This Month</Option>
              <Option value="quarter">This Quarter</Option>
              <Option value="year">This Year</Option>
            </Select>
            <Button
              icon={<ReloadOutlined />}
              onClick={handleRefresh}
              style={{ marginRight: 8 }}
            >
              Refresh
            </Button>
            <Button
              icon={<DownloadOutlined />}
              onClick={() => {/* Export report logic */}}
            >
              Export Report
            </Button>
          </div>
        </div>

        <Spin spinning={loading}>
          {/* Summary Cards */}
          <Row gutter={16} className="summary-cards">
            <Col xs={24} sm={12} md={6}>
              <Card>
                <Statistic
                  title="Total Tickets"
                  value={statistics.totalTickets}
                  prefix={<BarChartOutlined />}
                />
              </Card>
            </Col>
            <Col xs={24} sm={12} md={6}>
              <Card>
                <Statistic
                  title="Open Tickets"
                  value={
                    (statistics.ticketsByStatus[TicketStatus.NEW] || 0) +
                    (statistics.ticketsByStatus[TicketStatus.OPEN] || 0) +
                    (statistics.ticketsByStatus[TicketStatus.IN_PROGRESS] || 0)
                  }
                  prefix={<LineChartOutlined />}
                />
              </Card>
            </Col>
            <Col xs={24} sm={12} md={6}>
              <Card>
                <Statistic
                  title="Resolved Tickets"
                  value={statistics.ticketsByStatus[TicketStatus.RESOLVED] || 0}
                  prefix={<PieChartOutlined />}
                />
              </Card>
            </Col>
            <Col xs={24} sm={12} md={6}>
              <Card>
                <Statistic
                  title="Avg. Resolution Time"
                  value={statistics.averageResolutionTime}
                  suffix="hours"
                  precision={1}
                />
              </Card>
            </Col>
          </Row>

          {/* Status and Priority Distribution */}
          <Row gutter={16} className="data-tables">
            <Col xs={24} md={12}>
              <Card title="Status Distribution" className="table-card">
                <Table
                  columns={statusColumns}
                  dataSource={statusData}
                  rowKey="status"
                  pagination={false}
                  size="small"
                />
              </Card>
            </Col>
            <Col xs={24} md={12}>
              <Card title="Priority Distribution" className="table-card">
                <Table
                  columns={priorityColumns}
                  dataSource={priorityData}
                  rowKey="priority"
                  pagination={false}
                  size="small"
                />
              </Card>
            </Col>
          </Row>

          {/* Top Assignees */}
          <Row gutter={16} className="data-tables">
            <Col xs={24}>
              <Card title="Top Assignees" className="table-card">
                <Table
                  columns={topAssigneesColumns}
                  dataSource={topAssigneesData}
                  rowKey="name"
                  pagination={false}
                  size="small"
                />
              </Card>
            </Col>
          </Row>

          {/* Ticket Trend */}
          <Row gutter={16} className="data-tables">
            <Col xs={24} md={12}>
              <Card title="Ticket Trend">
                <div className="chart-container">
                  <Line
                    options={{
                      ...chartOptions,
                      plugins: {
                        ...chartOptions.plugins,
                        title: {
                          display: true,
                          text: 'Tickets theo thời gian'
                        }
                      }
                    }}
                    data={{
                      labels: statistics.ticketsTrend.map(item => {
                        const date = new Date(item.date);
                        return `${date.getDate()}/${date.getMonth() + 1}`;
                      }),
                      datasets: [
                        {
                          label: 'Số lượng ticket',
                          data: statistics.ticketsTrend.map(item => item.count),
                          borderColor: 'rgb(75, 192, 192)',
                          backgroundColor: 'rgba(75, 192, 192, 0.2)',
                          tension: 0.3,
                          fill: true,
                        }
                      ]
                    }}
                  />
                </div>
              </Card>
            </Col>
            <Col xs={24} md={12}>
              <Card title="Phân bố Ticket theo Ưu tiên">
                <div className="chart-container">
                  <Doughnut
                    options={{
                      ...chartOptions,
                      plugins: {
                        ...chartOptions.plugins,
                        title: {
                          display: true,
                          text: 'Phân bố theo mức độ ưu tiên'
                        }
                      }
                    }}
                    data={{
                      labels: Object.keys(statistics.ticketsByPriority).map(key => 
                        key.toUpperCase()
                      ),
                      datasets: [
                        {
                          data: Object.values(statistics.ticketsByPriority),
                          backgroundColor: [
                            'rgba(75, 192, 192, 0.6)',
                            'rgba(255, 159, 64, 0.6)',
                            'rgba(255, 99, 132, 0.6)',
                            'rgba(255, 0, 0, 0.6)',
                          ],
                          borderColor: [
                            'rgb(75, 192, 192)',
                            'rgb(255, 159, 64)',
                            'rgb(255, 99, 132)',
                            'rgb(255, 0, 0)',
                          ],
                          borderWidth: 1,
                        }
                      ]
                    }}
                  />
                </div>
              </Card>
            </Col>
          </Row>
          
          {/* Ticket Categories & Top Assignees */}
          <Row gutter={16} className="data-tables">
            <Col xs={24} md={12}>
              <Card title="Phân bố Ticket theo Danh mục">
                <div className="chart-container">
                  <Bar
                    options={{
                      ...chartOptions,
                      indexAxis: 'y' as const,
                      plugins: {
                        ...chartOptions.plugins,
                        title: {
                          display: true,
                          text: 'Số lượng ticket theo danh mục'
                        }
                      }
                    }}
                    data={{
                      labels: Object.keys(statistics.ticketsByCategory),
                      datasets: [
                        {
                          label: 'Số lượng',
                          data: Object.values(statistics.ticketsByCategory),
                          backgroundColor: 'rgba(54, 162, 235, 0.6)',
                          borderColor: 'rgb(54, 162, 235)',
                          borderWidth: 1,
                        }
                      ]
                    }}
                  />
                </div>
              </Card>
            </Col>
            <Col xs={24} md={12}>
              <Card title="Phân bố Ticket theo Trạng thái">
                <div className="chart-container">
                  <Pie
                    options={{
                      ...chartOptions,
                      plugins: {
                        ...chartOptions.plugins,
                        title: {
                          display: true,
                          text: 'Trạng thái ticket'
                        }
                      }
                    }}
                    data={{
                      labels: Object.keys(statistics.ticketsByStatus).map(key => 
                        key.replace('_', ' ').toUpperCase()
                      ),
                      datasets: [
                        {
                          data: Object.values(statistics.ticketsByStatus),
                          backgroundColor: [
                            'rgba(54, 162, 235, 0.6)', // new
                            'rgba(75, 192, 192, 0.6)', // open
                            'rgba(255, 206, 86, 0.6)', // in progress
                            'rgba(153, 102, 255, 0.6)', // pending
                            'rgba(75, 192, 192, 0.6)', // resolved
                            'rgba(201, 203, 207, 0.6)', // closed
                          ],
                          borderColor: [
                            'rgb(54, 162, 235)',
                            'rgb(75, 192, 192)',
                            'rgb(255, 206, 86)',
                            'rgb(153, 102, 255)',
                            'rgb(75, 192, 192)',
                            'rgb(201, 203, 207)',
                          ],
                          borderWidth: 1,
                        }
                      ]
                    }}
                  />
                </div>
              </Card>
            </Col>
          </Row>
        </Spin>
      </div>
    </MainLayout>
  );
};

export default AnalyticsDashboardPage;