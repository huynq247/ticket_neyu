import React, { useState, useEffect } from 'react';
import { Button, Table, Space, Modal, Form, Input, Select, message, Card, Tabs } from 'antd';
import { EditOutlined, DeleteOutlined, PlusOutlined, UserOutlined, UserAddOutlined } from '@ant-design/icons';
import { getDepartments, createDepartment, updateDepartment, deleteDepartment, getDepartmentById } from '@/api/departmentService';
import { getUsers } from '@/api/userService';
import { User } from '@/types';

const { Option } = Select;
const { TabPane } = Tabs;
const { TextArea } = Input;

const DepartmentManagementPage: React.FC = () => {
  const [departments, setDepartments] = useState<any[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [modalVisible, setModalVisible] = useState<boolean>(false);
  const [form] = Form.useForm();
  const [currentDepartment, setCurrentDepartment] = useState<any>(null);
  const [departmentUsers, setDepartmentUsers] = useState<User[]>([]);
  const [selectedDepartmentId, setSelectedDepartmentId] = useState<string>('');

  const fetchData = async () => {
    setLoading(true);
    try {
      const [departmentsRes, usersRes] = await Promise.all([
        getDepartments(),
        getUsers()
      ]);
      
      setDepartments(departmentsRes.data.departments);
      setUsers(usersRes.data.users);
    } catch (error) {
      console.error('Error fetching data:', error);
      message.error('Failed to load departments and users');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const fetchDepartmentUsers = async (departmentId: string) => {
    if (!departmentId) return;
    
    try {
      const response = await getDepartmentById(departmentId);
      // Lấy danh sách ID thành viên từ department
      const memberIds = response.data.members || [];
      
      // Lọc danh sách user dựa trên các ID trong members
      const departmentUsersList = users.filter(user => memberIds.includes(user.id));
      setDepartmentUsers(departmentUsersList);
    } catch (error) {
      console.error('Error fetching department users:', error);
      message.error('Failed to load department users');
    }
  };

  const handleDepartmentSelect = (departmentId: string) => {
    setSelectedDepartmentId(departmentId);
    fetchDepartmentUsers(departmentId);
  };

  const handleCreate = () => {
    setCurrentDepartment(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (department: any) => {
    setCurrentDepartment(department);
    form.setFieldsValue({
      name: department.name,
      description: department.description,
      managerId: department.managerId,
    });
    setModalVisible(true);
  };

  const handleDelete = (departmentId: string) => {
    Modal.confirm({
      title: 'Are you sure you want to delete this department?',
      content: 'This action cannot be undone and may affect users assigned to this department.',
      okText: 'Yes',
      okType: 'danger',
      cancelText: 'No',
      onOk: async () => {
        try {
          await deleteDepartment(departmentId);
          message.success('Department deleted successfully');
          fetchData();
        } catch (error) {
          console.error('Error deleting department:', error);
          message.error('Failed to delete department');
        }
      },
    });
  };

  const handleModalOk = async () => {
    try {
      const values = await form.validateFields();
      
      if (currentDepartment) {
        // Update existing department
        await updateDepartment(currentDepartment.id, values);
        message.success('Department updated successfully');
      } else {
        // Create new department
        await createDepartment(values);
        message.success('Department created successfully');
      }
      
      setModalVisible(false);
      fetchData();
    } catch (error) {
      console.error('Error saving department:', error);
      message.error('Failed to save department');
    }
  };

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      render: (text: string, record: any) => (
        <a onClick={() => handleDepartmentSelect(record.id)}>{text}</a>
      ),
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
      render: (text: string) => text || 'No description',
    },
    {
      title: 'Manager',
      dataIndex: 'managerId',
      key: 'managerId',
      render: (managerId: string) => {
        const manager = users.find(user => user.id === managerId);
        return manager ? manager.fullName : 'Not assigned';
      },
    },
    {
      title: 'Created At',
      dataIndex: 'createdAt',
      key: 'createdAt',
      render: (date: string) => new Date(date).toLocaleDateString(),
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: any) => (
        <Space size="middle">
          <Button
            type="primary"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
            size="small"
          >
            Edit
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

  const userColumns = [
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
      title: 'Role',
      dataIndex: 'role',
      key: 'role',
    },
    {
      title: 'Status',
      dataIndex: 'isActive',
      key: 'isActive',
      render: (isActive: boolean) => (
        isActive ? 'Active' : 'Inactive'
      ),
    },
  ];

  return (
    <div className="department-management-page">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
        <h1>Department Management</h1>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={handleCreate}
        >
          Create Department
        </Button>
      </div>
      
      <div className="department-content" style={{ display: 'flex', gap: '24px' }}>
        <div style={{ flex: '1 1 60%' }}>
          <Card title="Departments">
            <Table
              columns={columns}
              dataSource={departments}
              rowKey="id"
              loading={loading}
            />
          </Card>
        </div>
        
        <div style={{ flex: '1 1 40%' }}>
          <Card 
            title={selectedDepartmentId ? `${departments.find(d => d.id === selectedDepartmentId)?.name} - Members` : 'Department Details'}
            extra={selectedDepartmentId && (
              <Button icon={<UserAddOutlined />} size="small">
                Add Member
              </Button>
            )}
          >
            {selectedDepartmentId ? (
              <Tabs defaultActiveKey="members">
                <TabPane tab="Members" key="members">
                  <Table
                    columns={userColumns}
                    dataSource={departmentUsers}
                    rowKey="id"
                    pagination={false}
                    size="small"
                  />
                </TabPane>
                <TabPane tab="Statistics" key="statistics">
                  <div style={{ padding: '20px', textAlign: 'center' }}>
                    <p>Total members: {departmentUsers.length}</p>
                    <p>Active tickets: 12</p>
                    <p>Average response time: 4.5 hours</p>
                  </div>
                </TabPane>
              </Tabs>
            ) : (
              <div style={{ padding: '20px', textAlign: 'center' }}>
                <p>Select a department to see details</p>
              </div>
            )}
          </Card>
        </div>
      </div>
      
      <Modal
        title={currentDepartment ? 'Edit Department' : 'Create Department'}
        open={modalVisible}
        onOk={handleModalOk}
        onCancel={() => setModalVisible(false)}
      >
        <Form
          form={form}
          layout="vertical"
        >
          <Form.Item
            name="name"
            label="Department Name"
            rules={[{ required: true, message: 'Please enter the department name' }]}
          >
            <Input prefix={<UserOutlined />} />
          </Form.Item>
          
          <Form.Item
            name="description"
            label="Description"
          >
            <TextArea rows={3} />
          </Form.Item>
          
          <Form.Item
            name="managerId"
            label="Department Manager"
          >
            <Select placeholder="Select manager">
              {users.map(user => (
                <Option key={user.id} value={user.id}>{user.fullName}</Option>
              ))}
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default DepartmentManagementPage;