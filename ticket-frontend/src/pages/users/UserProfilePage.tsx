import React, { useState, useEffect } from 'react';
import { Card, Tabs, Form, Input, Button, Upload, message, Spin, Avatar, Space, Descriptions } from 'antd';
import { UserOutlined, UploadOutlined, LockOutlined } from '@ant-design/icons';
import type { RcFile, UploadFile, UploadProps } from 'antd/es/upload/interface';
import { useAuth } from '@/context/AuthContext';
import { getUserById, updateUser, changePassword, updateAvatar } from '@/api/userService';
import { User } from '@/types';

const { TabPane } = Tabs;

const UserProfilePage: React.FC = () => {
  const { user: authUser } = useAuth();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [updating, setUpdating] = useState<boolean>(false);
  const [profileForm] = Form.useForm();
  const [passwordForm] = Form.useForm();
  const [fileList, setFileList] = useState<UploadFile[]>([]);

  useEffect(() => {
    if (authUser?.id) {
      fetchUserData();
    }
  }, [authUser]);

  const fetchUserData = async () => {
    if (!authUser?.id) return;
    
    try {
      setLoading(true);
      const response = await getUserById(authUser.id);
      setUser(response.data);
      
      // Set form values
      profileForm.setFieldsValue({
        firstName: response.data.firstName,
        lastName: response.data.lastName,
        email: response.data.email,
      });
      
      // If user has avatar, add it to file list
      if (response.data.avatar) {
        setFileList([
          {
            uid: '-1',
            name: 'avatar',
            status: 'done',
            url: response.data.avatar,
          },
        ]);
      }
    } catch (error) {
      console.error('Error fetching user data:', error);
      message.error('Failed to load user profile');
    } finally {
      setLoading(false);
    }
  };

  const handleProfileUpdate = async (values: any) => {
    if (!authUser?.id) return;
    
    try {
      setUpdating(true);
      await updateUser(authUser.id, values);
      message.success('Profile updated successfully');
      fetchUserData(); // Refresh user data
    } catch (error) {
      console.error('Error updating profile:', error);
      message.error('Failed to update profile');
    } finally {
      setUpdating(false);
    }
  };

  const handlePasswordChange = async (values: any) => {
    if (!authUser?.id) return;
    
    try {
      setUpdating(true);
      await changePassword(authUser.id, values.oldPassword, values.newPassword);
      message.success('Password changed successfully');
      passwordForm.resetFields();
    } catch (error) {
      console.error('Error changing password:', error);
      message.error('Failed to change password');
    } finally {
      setUpdating(false);
    }
  };

  const handleAvatarUpload: UploadProps['onChange'] = async ({ file }) => {
    if (!authUser?.id || !file) return;
    
    const rcFile = file as RcFile;
    
    // Check file size and type
    const isJpgOrPng = rcFile.type === 'image/jpeg' || rcFile.type === 'image/png';
    if (!isJpgOrPng) {
      message.error('You can only upload JPG/PNG file!');
      return;
    }
    
    const isLt2M = rcFile.size / 1024 / 1024 < 2;
    if (!isLt2M) {
      message.error('Image must be smaller than 2MB!');
      return;
    }
    
    try {
      setUpdating(true);
      await updateAvatar(authUser.id, rcFile);
      message.success('Avatar updated successfully');
      fetchUserData(); // Refresh user data
    } catch (error) {
      console.error('Error updating avatar:', error);
      message.error('Failed to update avatar');
    } finally {
      setUpdating(false);
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
    <div className="user-profile-page">
      <h1>My Profile</h1>
      
      <div className="profile-header" style={{ marginBottom: 24 }}>
        <Space size="large" align="center">
          <Avatar 
            size={96} 
            src={user?.avatar} 
            icon={!user?.avatar && <UserOutlined />} 
          />
          <div>
            <h2>{user?.firstName} {user?.lastName}</h2>
            <p>{user?.email}</p>
            <p>Roles: {user?.roles?.map(role => role.name).join(', ') || 'No roles assigned'}</p>
          </div>
        </Space>
      </div>
      
      <Tabs defaultActiveKey="profile">
        <TabPane tab="Profile Information" key="profile">
          <Card>
            <Descriptions title="User Information" bordered>
              <Descriptions.Item label="First Name">{user?.firstName}</Descriptions.Item>
              <Descriptions.Item label="Last Name">{user?.lastName}</Descriptions.Item>
              <Descriptions.Item label="Email">{user?.email}</Descriptions.Item>
              <Descriptions.Item label="Roles">{user?.roles?.map(role => role.name).join(', ') || 'No roles assigned'}</Descriptions.Item>
              <Descriptions.Item label="Department">{user?.department || 'Not assigned'}</Descriptions.Item>
              <Descriptions.Item label="Status">{user?.isActive ? 'Active' : 'Inactive'}</Descriptions.Item>
              <Descriptions.Item label="Member Since">{new Date(user?.createdAt || '').toLocaleDateString()}</Descriptions.Item>
            </Descriptions>
            
            <div style={{ marginTop: 24 }}>
              <h3>Edit Profile</h3>
              <Form
                form={profileForm}
                layout="vertical"
                onFinish={handleProfileUpdate}
              >
                <Form.Item
                  name="firstName"
                  label="First Name"
                  rules={[{ required: true, message: 'Please enter your first name' }]}
                >
                  <Input prefix={<UserOutlined />} />
                </Form.Item>
                
                <Form.Item
                  name="lastName"
                  label="Last Name"
                  rules={[{ required: true, message: 'Please enter your last name' }]}
                >
                  <Input prefix={<UserOutlined />} />
                </Form.Item>
                
                <Form.Item
                  name="email"
                  label="Email"
                  rules={[
                    { required: true, message: 'Please enter your email' },
                    { type: 'email', message: 'Please enter a valid email' }
                  ]}
                >
                  <Input />
                </Form.Item>
                
                <Form.Item>
                  <Button type="primary" htmlType="submit" loading={updating}>
                    Update Profile
                  </Button>
                </Form.Item>
              </Form>
            </div>
          </Card>
        </TabPane>
        
        <TabPane tab="Change Password" key="password">
          <Card>
            <Form
              form={passwordForm}
              layout="vertical"
              onFinish={handlePasswordChange}
            >
              <Form.Item
                name="oldPassword"
                label="Current Password"
                rules={[{ required: true, message: 'Please enter your current password' }]}
              >
                <Input.Password prefix={<LockOutlined />} />
              </Form.Item>
              
              <Form.Item
                name="newPassword"
                label="New Password"
                rules={[
                  { required: true, message: 'Please enter your new password' },
                  { min: 8, message: 'Password must be at least 8 characters' }
                ]}
              >
                <Input.Password prefix={<LockOutlined />} />
              </Form.Item>
              
              <Form.Item
                name="confirmPassword"
                label="Confirm New Password"
                dependencies={['newPassword']}
                rules={[
                  { required: true, message: 'Please confirm your new password' },
                  ({ getFieldValue }) => ({
                    validator(_, value) {
                      if (!value || getFieldValue('newPassword') === value) {
                        return Promise.resolve();
                      }
                      return Promise.reject(new Error('The two passwords do not match'));
                    },
                  }),
                ]}
              >
                <Input.Password prefix={<LockOutlined />} />
              </Form.Item>
              
              <Form.Item>
                <Button type="primary" htmlType="submit" loading={updating}>
                  Change Password
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </TabPane>
        
        <TabPane tab="Profile Picture" key="avatar">
          <Card>
            <div style={{ textAlign: 'center', marginBottom: 24 }}>
              <Avatar 
                size={128} 
                src={user?.avatar} 
                icon={!user?.avatar && <UserOutlined />} 
              />
            </div>
            
            <Upload
              fileList={fileList}
              onChange={handleAvatarUpload}
              maxCount={1}
              beforeUpload={() => false}
            >
              <Button icon={<UploadOutlined />}>Upload New Avatar</Button>
            </Upload>
            
            <p style={{ marginTop: 16 }}>
              Supported formats: JPG, PNG. Maximum file size: 2MB.
            </p>
          </Card>
        </TabPane>
      </Tabs>
    </div>
  );
};

export default UserProfilePage;