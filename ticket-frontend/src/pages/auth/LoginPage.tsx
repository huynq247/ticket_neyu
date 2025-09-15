import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Layout, Row, Col, Card } from 'antd';
import LoginForm from '@/components/auth/LoginForm';
import { useAuth } from '@/context/AuthContext';

const { Content } = Layout;

const LoginPage: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    // If user is already authenticated, redirect to dashboard
    if (isAuthenticated) {
      navigate('/dashboard');
    }
  }, [isAuthenticated, navigate]);

  const handleLoginSuccess = () => {
    navigate('/dashboard');
  };

  return (
    <Layout className="login-page" style={{ minHeight: '100vh' }}>
      <Content>
        <Row justify="center" align="middle" style={{ minHeight: '100vh' }}>
          <Col xs={22} sm={16} md={12} lg={8} xl={6}>
            <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
              <h1 style={{ fontSize: '24px', margin: 0 }}>Ticket Management System</h1>
              <p>Sign in to your account</p>
            </div>
            <Card 
              bordered={false} 
              style={{ boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)' }}
            >
              <LoginForm onSuccess={handleLoginSuccess} />
            </Card>
          </Col>
        </Row>
      </Content>
    </Layout>
  );
};

export default LoginPage;