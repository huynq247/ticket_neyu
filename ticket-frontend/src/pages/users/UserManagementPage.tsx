import React, { useState, useEffect } from 'react';
import { Button, Table, Space, Tag, Modal, message, Input, Select, Pagination } from 'antd';
import { EditOutlined, DeleteOutlined, UserAddOutlined, SearchOutlined } from '@ant-design/icons';
import { getUsers, toggleUserStatus } from '@/api/userService';
import { User, UserRole } from '@/types';
import { useNavigate } from 'react-router-dom';

const { Option } = Select;

const UserManagementPage: React.FC = () => {
  const navigate = useNavigate();
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [total, setTotal] = useState<number>(0);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [pageSize, setPageSize] = useState<number>(10);
  const [searchText, setSearchText] = useState<string>('');
  const [selectedRole, setSelectedRole] = useState<string>('');
  const [selectedDepartment, setSelectedDepartment] = useState<string>('');

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const response = await getUsers({
        search: searchText,
        role: selectedRole,
        department: selectedDepartment,
        page: currentPage,
        limit: pageSize,
      });
      setUsers(response.data.users);
      setTotal(response.data.total);
    } catch (error) {
      console.error('Error fetching users:', error);
      message.error('Failed to fetch users');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, [currentPage, pageSize, searchText, selectedRole, selectedDepartment]);

  const handleEdit = (userId: string) => {
    navigate(`/users/${userId}/edit`);
  };

  const handleDelete = (userId: string) => {
    Modal.confirm({
      title: 'Are you sure you want to delete this user?',
      content: 'This action cannot be undone.',
      okText: 'Yes',
      okType: 'danger',
      cancelText: 'No',
      onOk: () => {
        // Implement user deletion logic here
        message.success('User deleted successfully');
        fetchUsers();
      },
    });
  };

  const handleToggleStatus = async (userId: string, isActive: boolean) => {
    try {
      await toggleUserStatus(userId, !isActive);
      message.success(`User ${isActive ? 'deactivated' : 'activated'} successfully`);
      fetchUsers();
    } catch (error) {
      console.error('Error toggling user status:', error);
      message.error('Failed to update user status');
    }
  };

  const handleSearch = (value: string) => {
    setSearchText(value);
    setCurrentPage(1);
  };

  const handleRoleFilter = (value: string) => {
    setSelectedRole(value);
    setCurrentPage(1);
  };

  const handleDepartmentFilter = (value: string) => {
    setSelectedDepartment(value);
    setCurrentPage(1);
  };

  const handlePageChange = (page: number, pageSize?: number) => {
    setCurrentPage(page);
    if (pageSize) {
      setPageSize(pageSize);
    }
  };

  const columns = [
    {
      title: 'Name',
      dataIndex: 'fullName',
      key: 'fullName',
      render: (text: string, record: User) => (
        <div>
          <div>{text}</div>
          <div style={{ fontSize: '0.8em', color: '#888' }}>{record.email}</div>
        </div>
      ),
    },
    {
      title: 'Username',
      dataIndex: 'username',
      key: 'username',
    },
    {
      title: 'Role',
      dataIndex: 'role',
      key: 'role',
      render: (role: UserRole) => {
        let color = 'default';
        switch (role) {
          case UserRole.ADMIN:
            color = 'red';
            break;
          case UserRole.MANAGER:
            color = 'green';
            break;
          case UserRole.AGENT:
            color = 'blue';
            break;
          case UserRole.DISPATCHER:
            color = 'purple';
            break;
          case UserRole.COORDINATOR:
            color = 'orange';
            break;
          default:
            color = 'default';
        }
        return <Tag color={color}>{role.toUpperCase()}</Tag>;
      },
    },
    {
      title: 'Department',
      dataIndex: 'department',
      key: 'department',
      render: (department: string) => department || 'N/A',
    },
    {
      title: 'Status',
      dataIndex: 'isActive',
      key: 'isActive',
      render: (isActive: boolean) => (
        <Tag color={isActive ? 'green' : 'red'}>
          {isActive ? 'Active' : 'Inactive'}
        </Tag>
      ),
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: User) => (
        <Space size="middle">
          <Button
            type="primary"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record.id)}
            size="small"
          >
            Edit
          </Button>
          <Button
            type={record.isActive ? 'default' : 'primary'}
            onClick={() => handleToggleStatus(record.id, record.isActive)}
            size="small"
          >
            {record.isActive ? 'Deactivate' : 'Activate'}
          </Button>
          <Button
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDelete(record.id)}
            size="small"
          >
            Delete
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div className="user-management-page">
      <div className="page-header">
        <h1>User Management</h1>
        <Button
          type="primary"
          icon={<UserAddOutlined />}
          onClick={() => navigate('/users/create')}
        >
          Add New User
        </Button>
      </div>

      <div className="filters" style={{ marginBottom: 16 }}>
        <Input
          placeholder="Search users..."
          value={searchText}
          onChange={(e) => handleSearch(e.target.value)}
          style={{ width: 200, marginRight: 16 }}
          prefix={<SearchOutlined />}
        />
        <Select
          placeholder="Filter by role"
          style={{ width: 150, marginRight: 16 }}
          onChange={handleRoleFilter}
          value={selectedRole || undefined}
          allowClear
        >
          <Option value="admin">Admin</Option>
          <Option value="manager">Manager</Option>
          <Option value="agent">Agent</Option>
          <Option value="customer">Customer</Option>
          <Option value="dispatcher">Dispatcher</Option>
          <Option value="coordinator">Coordinator</Option>
        </Select>
        <Select
          placeholder="Filter by department"
          style={{ width: 180 }}
          onChange={handleDepartmentFilter}
          value={selectedDepartment || undefined}
          allowClear
        >
          <Option value="it">IT Department</Option>
          <Option value="hr">HR Department</Option>
          <Option value="sales">Sales Department</Option>
          <Option value="support">Support Department</Option>
        </Select>
      </div>

      <Table
        columns={columns}
        dataSource={users}
        rowKey="id"
        loading={loading}
        pagination={false}
      />

      <div className="pagination" style={{ marginTop: 16, textAlign: 'right' }}>
        <Pagination
          current={currentPage}
          pageSize={pageSize}
          total={total}
          onChange={handlePageChange}
          showSizeChanger
          showTotal={(total) => `Total ${total} users`}
        />
      </div>
    </div>
  );
};

export default UserManagementPage;