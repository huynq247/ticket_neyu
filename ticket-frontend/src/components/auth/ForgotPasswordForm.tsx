import React, { useState } from 'react';
import { Button, Form, Input, Typography, Alert } from 'antd';
import { MailOutlined } from '@ant-design/icons';
import authService from '@/api/authService';
import './ForgotPasswordForm.css';

const { Title, Text } = Typography;

interface ForgotPasswordFormProps {
  onBack?: () => void;
}

const ForgotPasswordForm: React.FC<ForgotPasswordFormProps> = ({ onBack }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  
  const onFinish = async (values: { email: string }) => {
    setIsLoading(true);
    setError(null);
    
    try {
      await authService.forgotPassword(values.email);
      setSuccess(true);
    } catch (err: any) {
      let errorMessage = 'Failed to process your request. Please try again.';
      
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
    <div className="forgot-password-form-container">
      <div className="forgot-password-form-content">
        <div className="forgot-password-form-header">
          <Title level={2}>Forgot Password</Title>
          <Text type="secondary">Enter your email to reset your password</Text>
        </div>
        
        {success ? (
          <Alert
            message="Reset Email Sent"
            description="If an account exists with this email, you will receive a password reset link shortly."
            type="success"
            showIcon
            style={{ marginBottom: 20 }}
          />
        ) : (
          <Form
            name="forgotPassword"
            className="forgot-password-form"
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
                prefix={<MailOutlined className="site-form-item-icon" />}
                placeholder="Email"
              />
            </Form.Item>
            
            {error && (
              <div className="forgot-password-form-error">
                <Text type="danger">{error}</Text>
              </div>
            )}
            
            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                className="forgot-password-form-button"
                loading={isLoading}
                block
              >
                Send Reset Link
              </Button>
            </Form.Item>
            
            <div className="forgot-password-form-links">
              <Button type="link" onClick={onBack}>
                Back to Login
              </Button>
            </div>
          </Form>
        )}
      </div>
    </div>
  );
};

export default ForgotPasswordForm;