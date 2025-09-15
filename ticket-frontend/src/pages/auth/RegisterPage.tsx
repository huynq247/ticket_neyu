import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Layout, Row, Col, Card } from 'antd';
import RegisterForm from '@/components/auth/RegisterForm';
import { useAuth } from '@/context/AuthContext';

const { Content } = Layout;

const RegisterPage: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    // If user is already authenticated, redirect to dashboard
    if (isAuthenticated) {
      navigate('/dashboard');
    }
  }, [isAuthenticated, navigate]);

  const handleRegisterSuccess = () => {
    // Redirect to login page after successful registration
    navigate('/login', { state: { registrationSuccess: true } });
  };

  return (
    <Layout className="register-page" style={{ minHeight: '100vh' }}>
      <Content>
        <Row justify="center" align="middle" style={{ minHeight: '100vh' }}>
          <Col xs={22} sm={18} md={14} lg={10} xl={8}>
            <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
              <h1 style={{ fontSize: '24px', margin: 0 }}>Ticket Management System</h1>
              <p>Create a new account to get started</p>
            </div>
            <Card 
              bordered={false} 
              style={{ boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)' }}
            >
              <RegisterForm onSuccess={handleRegisterSuccess} />
            </Card>
          </Col>
        </Row>
      </Content>
    </Layout>
  );
};

export default RegisterPage;