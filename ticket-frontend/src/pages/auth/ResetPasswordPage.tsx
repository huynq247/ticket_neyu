import React, { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Layout, Row, Col, Card, Alert } from 'antd';
import ResetPasswordForm from '@/components/auth/ResetPasswordForm';
import { useAuth } from '@/context/AuthContext';

const { Content } = Layout;

const ResetPasswordPage: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');

  useEffect(() => {
    // If user is already authenticated, redirect to dashboard
    if (isAuthenticated) {
      navigate('/dashboard');
    }
  }, [isAuthenticated, navigate]);

  const handleResetSuccess = () => {
    navigate('/login');
  };

  if (!token) {
    return (
      <Layout className="reset-password-page" style={{ minHeight: '100vh' }}>
        <Content>
          <Row justify="center" align="middle" style={{ minHeight: '100vh' }}>
            <Col xs={22} sm={16} md={12} lg={8} xl={6}>
              <Card 
                bordered={false} 
                style={{ boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)' }}
              >
                <Alert
                  message="Invalid Reset Link"
                  description="The password reset link is invalid or has expired. Please request a new password reset link."
                  type="error"
                  showIcon
                  style={{ marginBottom: 20 }}
                  action={
                    <a href="/forgot-password">
                      Request New Link
                    </a>
                  }
                />
              </Card>
            </Col>
          </Row>
        </Content>
      </Layout>
    );
  }

  return (
    <Layout className="reset-password-page" style={{ minHeight: '100vh' }}>
      <Content>
        <Row justify="center" align="middle" style={{ minHeight: '100vh' }}>
          <Col xs={22} sm={16} md={12} lg={8} xl={6}>
            <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
              <h1 style={{ fontSize: '24px', margin: 0 }}>Ticket Management System</h1>
            </div>
            <Card 
              bordered={false} 
              style={{ boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)' }}
            >
              <ResetPasswordForm token={token} onSuccess={handleResetSuccess} />
            </Card>
          </Col>
        </Row>
      </Content>
    </Layout>
  );
};

export default ResetPasswordPage;