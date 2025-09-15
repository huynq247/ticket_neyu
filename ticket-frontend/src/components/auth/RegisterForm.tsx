import React, { useState } from 'react';
import { Button, Form, Input, Typography, Alert } from 'antd';
import { UserOutlined, LockOutlined, MailOutlined, UserAddOutlined } from '@ant-design/icons';
import authService from '@/api/authService';
import './RegisterForm.css';

const { Title, Text } = Typography;

interface RegisterFormProps {
  onSuccess?: () => void;
}

const RegisterForm: React.FC<RegisterFormProps> = ({ onSuccess }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  
  const onFinish = async (values: {
    username: string;
    email: string;
    password: string;
    confirmPassword: string;
    fullName: string;
  }) => {
    // Validation - Make sure passwords match
    if (values.password !== values.confirmPassword) {
      setError("Passwords don't match");
      return;
    }

    setIsLoading(true);
    setError(null);
    
    try {
      const { confirmPassword, ...registerData } = values;
      await authService.register(registerData);
      setSuccess(true);
      
      if (onSuccess) {
        onSuccess();
      }
    } catch (err: any) {
      let errorMessage = 'Registration failed. Please try again.';
      
      if (err.response && err.response.data && err.response.data.message) {
        errorMessage = err.response.data.message;
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="register-form-container">
      <div className="register-form-content">
        <div className="register-form-header">
          <Title level={2}>Create an Account</Title>
          <Text type="secondary">Fill in your details to get started</Text>
        </div>
        
        {success ? (
          <Alert
            message="Registration Successful"
            description="Your account has been created successfully. You can now login with your credentials."
            type="success"
            showIcon
            style={{ marginBottom: 20 }}
          />
        ) : (
          <Form
            name="register"
            className="register-form"
            initialValues={{ remember: true }}
            onFinish={onFinish}
            layout="vertical"
            size="large"
          >
            <Form.Item
              name="fullName"
              rules={[{ required: true, message: 'Please input your full name!' }]}
            >
              <Input
                prefix={<UserOutlined className="site-form-item-icon" />}
                placeholder="Full Name"
              />
            </Form.Item>
            
            <Form.Item
              name="username"
              rules={[
                { required: true, message: 'Please input your username!' },
                { min: 3, message: 'Username must be at least 3 characters' },
              ]}
            >
              <Input
                prefix={<UserAddOutlined className="site-form-item-icon" />}
                placeholder="Username"
              />
            </Form.Item>
            
            <Form.Item
              name="email"
              rules={[
                { required: true, message: 'Please input your email!' },
                { type: 'email', message: 'Please enter a valid email address!' },
              ]}
            >
              <Input
                prefix={<MailOutlined className="site-form-item-icon" />}
                placeholder="Email"
              />
            </Form.Item>
            
            <Form.Item
              name="password"
              rules={[
                { required: true, message: 'Please input your password!' },
                { min: 6, message: 'Password must be at least 6 characters' },
              ]}
            >
              <Input.Password
                prefix={<LockOutlined className="site-form-item-icon" />}
                placeholder="Password"
              />
            </Form.Item>
            
            <Form.Item
              name="confirmPassword"
              dependencies={['password']}
              rules={[
                { required: true, message: 'Please confirm your password!' },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue('password') === value) {
                      return Promise.resolve();
                    }
                    return Promise.reject(new Error('The two passwords do not match!'));
                  },
                }),
              ]}
            >
              <Input.Password
                prefix={<LockOutlined className="site-form-item-icon" />}
                placeholder="Confirm Password"
              />
            </Form.Item>
            
            {error && (
              <div className="register-form-error">
                <Text type="danger">{error}</Text>
              </div>
            )}
            
            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                className="register-form-button"
                loading={isLoading}
                block
              >
                Register
              </Button>
            </Form.Item>
            
            <div className="register-form-links">
              <Text type="secondary">Already have an account?</Text>
              <a href="/login">Sign in</a>
            </div>
          </Form>
        )}
      </div>
    </div>
  );
};

export default RegisterForm;