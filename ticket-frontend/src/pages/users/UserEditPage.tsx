import React, { useState, useEffect } from 'react';
import { Form, Input, Button, Select, Checkbox, Upload, message, Spin, Card } from 'antd';
import { UploadOutlined, UserOutlined } from '@ant-design/icons';
import { useParams, useNavigate } from 'react-router-dom';
import { getUserById, updateUser } from '@/api/userService';
import { getRoles, getUserRoles, assignRoleToUser, removeRoleFromUser } from '@/api/roleService';
import { getDepartments } from '@/api/departmentService';
import { User, Role } from '@/types';

const { Option } = Select;

const UserEditPage: React.FC = () => {
  const { userId } = useParams<{ userId: string }>();
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const [loading, setLoading] = useState<boolean>(true);
  const [saving, setSaving] = useState<boolean>(false);
  const [user, setUser] = useState<User | null>(null);
  const [roles, setRoles] = useState<Role[]>([]);
  const [departments, setDepartments] = useState<any[]>([]);
  const [userRoles, setUserRoles] = useState<string[]>([]);

  const fetchUserData = async () => {
    if (!userId) return;
    
    try {
      setLoading(true);
      const [userResponse, rolesResponse, departmentsResponse, userRolesResponse] = await Promise.all([
        getUserById(userId),
        getRoles(),
        getDepartments(),
        getUserRoles(userId)
      ]);
      
      setUser(userResponse.data);
      setRoles(rolesResponse.data.roles);
      setDepartments(departmentsResponse.data.departments);
      setUserRoles(userRolesResponse.data.roles.map((role: Role) => role.id));
      
      // Set form values
      form.setFieldsValue({
        firstName: userResponse.data.firstName,
        lastName: userResponse.data.lastName,
        email: userResponse.data.email,
        department: userResponse.data.department,
        isActive: userResponse.data.isActive,
      });
    } catch (error) {
      console.error('Error fetching user data:', error);
      message.error('Failed to load user data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUserData();
  }, [userId]);

  const handleRoleChange = async (newRoles: string[]) => {
    if (!userId) return;
    
    try {
      // Find roles to add
      const rolesToAdd = newRoles.filter(role => !userRoles.includes(role));
      // Find roles to remove
      const rolesToRemove = userRoles.filter(role => !newRoles.includes(role));
      
      // Add new roles
      for (const roleId of rolesToAdd) {
        await assignRoleToUser(userId, roleId);
      }
      
      // Remove old roles
      for (const roleId of rolesToRemove) {
        await removeRoleFromUser(userId, roleId);
      }
      
      setUserRoles(newRoles);
      message.success('User roles updated successfully');
    } catch (error) {
      console.error('Error updating user roles:', error);
      message.error('Failed to update user roles');
    }
  };

  const handleSubmit = async (values: any) => {
    if (!userId) return;
    
    try {
      setSaving(true);
      await updateUser(userId, values);
      message.success('User updated successfully');
      navigate('/users');
    } catch (error) {
      console.error('Error updating user:', error);
      message.error('Failed to update user');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
        <Spin size="large" />
      </div>
    );
  }

  return (
    <div className="user-edit-page">
      <h1>Edit User</h1>
      
      <div className="user-edit-container" style={{ display: 'flex', gap: '24px' }}>
        <Card title="Basic Information" style={{ flex: 1 }}>
          <Form
            form={form}
            layout="vertical"
            onFinish={handleSubmit}
          >
            <Form.Item
              name="firstName"
              label="First Name"
              rules={[{ required: true, message: 'Please enter the first name' }]}
            >
              <Input prefix={<UserOutlined />} />
            </Form.Item>
            
            <Form.Item
              name="lastName"
              label="Last Name"
              rules={[{ required: true, message: 'Please enter the last name' }]}
            >
              <Input prefix={<UserOutlined />} />
            </Form.Item>
            
            <Form.Item
              name="email"
              label="Email"
              rules={[
                { required: true, message: 'Please enter an email' },
                { type: 'email', message: 'Please enter a valid email' }
              ]}
            >
              <Input />
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
            >
              <Checkbox>Account is active</Checkbox>
            </Form.Item>
            
            <Form.Item>
              <Button type="primary" htmlType="submit" loading={saving}>
                Update User
              </Button>
              <Button style={{ marginLeft: 8 }} onClick={() => navigate('/users')}>
                Cancel
              </Button>
            </Form.Item>
          </Form>
        </Card>
        
        <Card title="Roles and Permissions" style={{ flex: 1 }}>
          <div className="user-roles">
            <h3>Assigned Roles</h3>
            <Select
              mode="multiple"
              style={{ width: '100%' }}
              placeholder="Select roles"
              value={userRoles}
              onChange={handleRoleChange}
            >
              {roles.map(role => (
                <Option key={role.id} value={role.id}>{role.name}</Option>
              ))}
            </Select>
          </div>
          
          <div className="user-avatar" style={{ marginTop: 24 }}>
            <h3>User Avatar</h3>
            <Upload
              name="avatar"
              listType="picture-card"
              className="avatar-uploader"
              showUploadList={false}
              beforeUpload={() => false}
            >
              {user?.avatar ? (
                <img src={user.avatar} alt="avatar" style={{ width: '100%' }} />
              ) : (
                <div>
                  <UploadOutlined />
                  <div style={{ marginTop: 8 }}>Upload</div>
                </div>
              )}
            </Upload>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default UserEditPage;