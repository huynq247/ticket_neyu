import React, { useState, useEffect } from 'react';
import { Form, Input, Button, Select, Checkbox, message, Card } from 'antd';
import { UserOutlined, LockOutlined, MailOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { getRoles } from '@/api/roleService';
import { getDepartments } from '@/api/departmentService';
import { Role } from '@/types';

const { Option } = Select;

const UserCreatePage: React.FC = () => {
  const [form] = Form.useForm();
  const navigate = useNavigate();
  const [loading, setLoading] = useState<boolean>(false);
  const [roles, setRoles] = useState<Role[]>([]);
  const [departments, setDepartments] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [rolesResponse, departmentsResponse] = await Promise.all([
          getRoles(),
          getDepartments()
        ]);
        
        setRoles(rolesResponse.data.roles);
        setDepartments(departmentsResponse.data.departments);
      } catch (error) {
        console.error('Error fetching data:', error);
        message.error('Failed to load roles and departments');
      }
    };

    fetchData();
  }, []);

  const handleSubmit = async (values: any) => {
    try {
      setLoading(true);
      
      // TODO: Implement API call to create user
      console.log('Creating user with values:', values);
      
      message.success('User created successfully');
      navigate('/users');
    } catch (error) {
      console.error('Error creating user:', error);
      message.error('Failed to create user');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="user-create-page">
      <h1>Create New User</h1>
      
      <Card>
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
        >
          <Form.Item
            name="username"
            label="Username"
            rules={[{ required: true, message: 'Please enter a username' }]}
          >
            <Input prefix={<UserOutlined />} placeholder="Username" />
          </Form.Item>
          
          <Form.Item
            name="email"
            label="Email"
            rules={[
              { required: true, message: 'Please enter an email' },
              { type: 'email', message: 'Please enter a valid email' }
            ]}
          >
            <Input prefix={<MailOutlined />} placeholder="Email" />
          </Form.Item>
          
          <Form.Item
            name="password"
            label="Password"
            rules={[
              { required: true, message: 'Please enter a password' },
              { min: 8, message: 'Password must be at least 8 characters' }
            ]}
          >
            <Input.Password prefix={<LockOutlined />} placeholder="Password" />
          </Form.Item>
          
          <Form.Item
            name="confirmPassword"
            label="Confirm Password"
            dependencies={['password']}
            rules={[
              { required: true, message: 'Please confirm the password' },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || getFieldValue('password') === value) {
                    return Promise.resolve();
                  }
                  return Promise.reject(new Error('The two passwords do not match'));
                },
              }),
            ]}
          >
            <Input.Password prefix={<LockOutlined />} placeholder="Confirm password" />
          </Form.Item>
          
          <Form.Item
            name="fullName"
            label="Full Name"
            rules={[{ required: true, message: 'Please enter the full name' }]}
          >
            <Input placeholder="Full name" />
          </Form.Item>
          
          <Form.Item
            name="roles"
            label="Roles"
            rules={[{ required: true, message: 'Please select at least one role' }]}
          >
            <Select
              mode="multiple"
              placeholder="Select roles"
            >
              {roles.map(role => (
                <Option key={role.id} value={role.id}>{role.name}</Option>
              ))}
            </Select>
          </Form.Item>
          
          <Form.Item
            name="department"
            label="Department"
          >
            <Select placeholder="Select department">
              {departments.map(dept => (
                <Option key={dept.id} value={dept.id}>{dept.name}</Option>
              ))}
            </Select>
          </Form.Item>
          
          <Form.Item
            name="isActive"
            valuePropName="checked"
            initialValue={true}
          >
            <Checkbox>Account is active</Checkbox>
          </Form.Item>
          
          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading}>
              Create User
            </Button>
            <Button style={{ marginLeft: 8 }} onClick={() => navigate('/users')}>
              Cancel
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default UserCreatePage;