import React from 'react';
import { Button, Form, Input, Typography } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { useAuth } from '@/context/AuthContext';
import './LoginForm.css';

const { Title, Text } = Typography;

interface LoginFormProps {
  onSuccess?: () => void;
}

const LoginForm: React.FC<LoginFormProps> = ({ onSuccess }) => {
  const { login, isLoading, error } = useAuth();
  
  const onFinish = async (values: { email: string; password: string }) => {
    try {
      await login(values.email, values.password);
      if (onSuccess) {
        onSuccess();
      }
    } catch (err) {
      // Error is already handled in the auth context
    }
  };
  
  return (
    <div className="login-form-container">
      <div className="login-form-content">
        <div className="login-form-header">
          <Title level={2}>Welcome Back</Title>
          <Text type="secondary">Sign in to your account to continue</Text>
        </div>
        
        <Form
          name="login"
          className="login-form"
          initialValues={{ remember: true }}
          onFinish={onFinish}
          layout="vertical"
          size="large"
        >
          <Form.Item
            name="email"
            rules={[
              { required: true, message: 'Please input your email!' },
              { type: 'email', message: 'Please enter a valid email address!' },
            ]}
          >
            <Input
              prefix={<UserOutlined className="site-form-item-icon" />}
              placeholder="Email"
              autoComplete="email"
            />
          </Form.Item>
          
          <Form.Item
            name="password"
            rules={[{ required: true, message: 'Please input your password!' }]}
          >
            <Input.Password
              prefix={<LockOutlined className="site-form-item-icon" />}
              placeholder="Password"
              autoComplete="current-password"
            />
          </Form.Item>
          
          {error && (
            <div className="login-form-error">
              <Text type="danger">{error}</Text>
            </div>
          )}
          
          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              className="login-form-button"
              loading={isLoading}
              block
            >
              Sign In
            </Button>
          </Form.Item>
          
          <div className="login-form-links">
            <a href="/forgot-password">Forgot password?</a>
            <span className="separator">|</span>
            <a href="/register">Create an account</a>
          </div>
        </Form>
      </div>
    </div>
  );
};

export default LoginForm;