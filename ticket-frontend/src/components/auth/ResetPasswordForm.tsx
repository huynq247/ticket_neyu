import React, { useState } from 'react';
import { Button, Form, Input, Typography, Alert } from 'antd';
import { LockOutlined } from '@ant-design/icons';
import authService from '@/api/authService';
import './ResetPasswordForm.css';

const { Title, Text } = Typography;

interface ResetPasswordFormProps {
  token: string;
  onSuccess?: () => void;
}

const ResetPasswordForm: React.FC<ResetPasswordFormProps> = ({ token, onSuccess }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  
  const onFinish = async (values: { password: string; confirmPassword: string }) => {
    // Validation - Make sure passwords match
    if (values.password !== values.confirmPassword) {
      setError("Passwords don't match");
      return;
    }

    setIsLoading(true);
    setError(null);
    
    try {
      await authService.resetPassword(token, values.password);
      setSuccess(true);
      
      if (onSuccess) {
        onSuccess();
      }
    } catch (err: any) {
      let errorMessage = 'Failed to reset password. Please try again.';
      
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
    <div className="reset-password-form-container">
      <div className="reset-password-form-content">
        <div className="reset-password-form-header">
          <Title level={2}>Reset Password</Title>
          <Text type="secondary">Enter your new password</Text>
        </div>
        
        {success ? (
          <Alert
            message="Password Reset Successful"
            description="Your password has been reset successfully. You can now login with your new password."
            type="success"
            showIcon
            style={{ marginBottom: 20 }}
            action={
              <Button size="small" type="primary" onClick={onSuccess}>
                Go to Login
              </Button>
            }
          />
        ) : (
          <Form
            name="resetPassword"
            className="reset-password-form"
            initialValues={{ remember: true }}
            onFinish={onFinish}
            layout="vertical"
            size="large"
          >
            <Form.Item
              name="password"
              rules={[
                { required: true, message: 'Please input your new password!' },
                { min: 6, message: 'Password must be at least 6 characters' },
              ]}
            >
              <Input.Password
                prefix={<LockOutlined className="site-form-item-icon" />}
                placeholder="New Password"
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
              <div className="reset-password-form-error">
                <Text type="danger">{error}</Text>
              </div>
            )}
            
            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                className="reset-password-form-button"
                loading={isLoading}
                block
              >
                Reset Password
              </Button>
            </Form.Item>
          </Form>
        )}
      </div>
    </div>
  );
};

export default ResetPasswordForm;