import React, { useState, useEffect } from 'react';
import { Button, Table, Space, Tabs, Tag, Select, message, Modal } from 'antd';
import { UserAddOutlined, DeleteOutlined } from '@ant-design/icons';
import { getDispatchers, getCoordinators, getDepartmentDispatchers, addDispatcherToDepartment, removeDispatcherFromDepartment } from '@/api/coordinatorService';
import { getDepartments } from '@/api/departmentService';
import { getUsers } from '@/api/userService';
import { User, UserRole } from '@/types';

const { TabPane } = Tabs;
const { Option } = Select;

const CoordinatorManagementPage: React.FC = () => {
  const [dispatchers, setDispatchers] = useState<User[]>([]);
  const [coordinators, setCoordinators] = useState<User[]>([]);
  const [departments, setDepartments] = useState<any[]>([]);
  const [selectedDepartment, setSelectedDepartment] = useState<string>('');
  const [departmentDispatchers, setDepartmentDispatchers] = useState<User[]>([]);
  const [availableUsers, setAvailableUsers] = useState<User[]>([]);
  const [selectedUser, setSelectedUser] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<string>('dispatchers');

  useEffect(() => {
    fetchDepartments();
    fetchData();
  }, []);

  useEffect(() => {
    if (selectedDepartment) {
      fetchDepartmentDispatchers();
    }
  }, [selectedDepartment]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [dispatchersRes, coordinatorsRes, usersRes] = await Promise.all([
        getDispatchers(),
        getCoordinators(),
        getUsers()
      ]);
      
      setDispatchers(dispatchersRes.data.dispatchers);
      setCoordinators(coordinatorsRes.data.coordinators);
      setAvailableUsers(usersRes.data.users);
    } catch (error) {
      console.error('Error fetching data:', error);
      message.error('Failed to load coordinators and dispatchers');
    } finally {
      setLoading(false);
    }
  };

  const fetchDepartments = async () => {
    try {
      const response = await getDepartments();
      setDepartments(response.data.departments);
    } catch (error) {
      console.error('Error fetching departments:', error);
      message.error('Failed to load departments');
    }
  };

  const fetchDepartmentDispatchers = async () => {
    if (!selectedDepartment) return;
    
    try {
      const response = await getDepartmentDispatchers(selectedDepartment);
      setDepartmentDispatchers(response.data.dispatchers);
    } catch (error) {
      console.error('Error fetching department dispatchers:', error);
      message.error('Failed to load department dispatchers');
    }
  };

  const handleAddDispatcher = async () => {
    if (!selectedDepartment || !selectedUser) {
      message.error('Please select both department and user');
      return;
    }
    
    try {
      await addDispatcherToDepartment(selectedDepartment, selectedUser);
      message.success('Dispatcher added to department successfully');
      fetchDepartmentDispatchers();
      setSelectedUser('');
    } catch (error) {
      console.error('Error adding dispatcher:', error);
      message.error('Failed to add dispatcher to department');
    }
  };

  const handleRemoveDispatcher = (userId: string) => {
    if (!selectedDepartment) return;
    
    Modal.confirm({
      title: 'Are you sure you want to remove this dispatcher from the department?',
      content: 'This action will remove the dispatcher role for this user in this department.',
      okText: 'Yes',
      okType: 'danger',
      cancelText: 'No',
      onOk: async () => {
        try {
          await removeDispatcherFromDepartment(selectedDepartment, userId);
          message.success('Dispatcher removed from department successfully');
          fetchDepartmentDispatchers();
        } catch (error) {
          console.error('Error removing dispatcher:', error);
          message.error('Failed to remove dispatcher from department');
        }
      }
    });
  };

  const handleTabChange = (key: string) => {
    setActiveTab(key);
  };

  const dispatcherColumns = [
    {
      title: 'Name',
      dataIndex: 'fullName',
      key: 'fullName',
    },
    {
      title: 'Email',
      dataIndex: 'email',
      key: 'email',
    },
    {
      title: 'Username',
      dataIndex: 'username',
      key: 'username',
    },
    {
      title: 'Department',
      dataIndex: 'department',
      key: 'department',
      render: (text: string) => text || 'N/A',
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
  ];

  const departmentDispatchersColumns = [
    ...dispatcherColumns,
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: User) => (
        <Button
          danger
          icon={<DeleteOutlined />}
          onClick={() => handleRemoveDispatcher(record.id)}
          size="small"
        >
          Remove
        </Button>
      ),
    },
  ];

  return (
    <div className="coordinator-management-page">
      <h1>Dispatcher/Coordinator Management</h1>
      
      <Tabs activeKey={activeTab} onChange={handleTabChange}>
        <TabPane tab="Dispatchers" key="dispatchers">
          <div className="department-section" style={{ marginBottom: 24, padding: 16, border: '1px solid #f0f0f0', borderRadius: 4 }}>
            <h3>Department Dispatchers</h3>
            
            <div style={{ display: 'flex', marginBottom: 16 }}>
              <Select
                placeholder="Select Department"
                style={{ width: 250, marginRight: 16 }}
                value={selectedDepartment || undefined}
                onChange={setSelectedDepartment}
              >
                {departments.map(dept => (
                  <Option key={dept.id} value={dept.id}>{dept.name}</Option>
                ))}
              </Select>
              
              <Select
                placeholder="Select User to Add"
                style={{ width: 250, marginRight: 16 }}
                value={selectedUser || undefined}
                onChange={setSelectedUser}
                disabled={!selectedDepartment}
              >
                {availableUsers
                  .filter(user => !departmentDispatchers.some(d => d.id === user.id))
                  .map(user => (
                    <Option key={user.id} value={user.id}>{user.fullName} ({user.email})</Option>
                  ))}
              </Select>
              
              <Button
                type="primary"
                icon={<UserAddOutlined />}
                onClick={handleAddDispatcher}
                disabled={!selectedDepartment || !selectedUser}
              >
                Add Dispatcher
              </Button>
            </div>
            
            <Table
              columns={departmentDispatchersColumns}
              dataSource={departmentDispatchers}
              rowKey="id"
              loading={loading && selectedDepartment !== ''}
              pagination={false}
            />
          </div>
          
          <div className="all-dispatchers-section">
            <h3>All Dispatchers</h3>
            <Table
              columns={dispatcherColumns}
              dataSource={dispatchers}
              rowKey="id"
              loading={loading}
            />
          </div>
        </TabPane>
        
        <TabPane tab="Coordinators" key="coordinators">
          <div className="coordinators-section">
            <h3>All Coordinators</h3>
            <Table
              columns={dispatcherColumns}
              dataSource={coordinators}
              rowKey="id"
              loading={loading}
            />
          </div>
        </TabPane>
      </Tabs>
    </div>
  );
};

export default CoordinatorManagementPage;