import React, { useState } from 'react';
import { Layout, Menu, Button, Avatar, Dropdown, theme } from 'antd';
import type { MenuProps } from 'antd';
import {
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  DashboardOutlined,
  FileOutlined,
  TeamOutlined,
  SettingOutlined,
  UserOutlined,
  LogoutOutlined,
  BarChartOutlined,
  UsergroupAddOutlined,
  ApartmentOutlined,
  ApiOutlined,
} from '@ant-design/icons';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import NotificationCenter from '@/components/NotificationCenter';
import PermissionControl from '@/components/common/PermissionControl';
import './MainLayout.css';

const { Header, Sider, Content } = Layout;

interface MainLayoutProps {
  children: React.ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const [collapsed, setCollapsed] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const { token } = theme.useToken();

  const handleMenuClick = (key: string) => {
    navigate(key);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const userMenuItems: MenuProps['items'] = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: 'My Profile',
      onClick: () => navigate('/profile'),
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: 'Settings',
      onClick: () => navigate('/settings'),
    },
    {
      key: 'divider1',
      type: 'divider',
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: 'Logout',
      onClick: handleLogout,
    },
  ];

  const notificationItems: MenuProps['items'] = [
    {
      key: '1',
      label: 'New ticket assigned to you',
      onClick: () => navigate('/tickets/123'),
    },
    {
      key: '2',
      label: 'Comment on ticket #456',
      onClick: () => navigate('/tickets/456'),
    },
    {
      key: '3',
      label: 'Ticket #789 status updated',
      onClick: () => navigate('/tickets/789'),
    },
    {
      key: 'divider1',
      type: 'divider',
    },
    {
      key: 'all',
      label: 'View all notifications',
      onClick: () => navigate('/notifications'),
    },
  ];

  const menuItems = [
    {
      key: '/dashboard',
      icon: <DashboardOutlined />,
      label: 'Dashboard',
    },
    {
      key: '/tickets',
      icon: <FileOutlined />,
      label: 'Tickets',
      permission: 'ticket:view',
    },
    {
      key: '/analytics',
      icon: <BarChartOutlined />,
      label: 'Analytics',
      permission: 'analytics:view',
    },
    {
      key: 'user-management',
      icon: <TeamOutlined />,
      label: 'User Management',
      children: [
        {
          key: '/users',
          icon: <UserOutlined />,
          label: 'Users',
          permission: 'user:view',
        },
        {
          key: '/roles',
          icon: <ApiOutlined />,
          label: 'Roles & Permissions',
          permission: 'role:view',
        },
        {
          key: '/departments',
          icon: <ApartmentOutlined />,
          label: 'Departments',
          permission: 'department:view',
        },
        {
          key: '/coordinators',
          icon: <UsergroupAddOutlined />,
          label: 'Dispatchers/Coordinators',
          permissions: ['dispatcher:assign', 'coordinator:assign'],
        },
      ],
    },
    {
      key: '/settings',
      icon: <SettingOutlined />,
      label: 'Settings',
      permission: 'system:settings',
    },
  ];

  return (
    <Layout className="main-layout">
      <Sider
        trigger={null}
        collapsible
        collapsed={collapsed}
        width={250}
        style={{
          overflow: 'auto',
          height: '100vh',
          position: 'fixed',
          left: 0,
          top: 0,
          bottom: 0,
          backgroundColor: token.colorBgContainer,
        }}
        theme="light"
      >
        <div className="logo-container">
          {collapsed ? 'TMS' : 'Ticket Management'}
        </div>
        <Menu
          mode="inline"
          selectedKeys={[location.pathname]}
          style={{ borderRight: 0 }}
          items={menuItems}
          onClick={({ key }) => handleMenuClick(key as string)}
        />
      </Sider>
      <Layout style={{ marginLeft: collapsed ? 80 : 250, transition: 'all 0.2s' }}>
        <Header style={{ 
          padding: 0, 
          backgroundColor: token.colorBgContainer,
          boxShadow: '0 1px 4px rgba(0,21,41,.08)',
          position: 'sticky',
          top: 0,
          zIndex: 1,
          width: '100%',
        }}>
          <div className="header-content">
            <Button
              type="text"
              icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
              onClick={() => setCollapsed(!collapsed)}
              className="trigger-button"
            />
            <div className="header-right">
              <Dropdown
                menu={{ items: notificationItems }}
                placement="bottomRight"
                arrow
                trigger={['click']}
              >
                <div className="notification-wrapper">
                  <NotificationCenter />
                </div>
              </Dropdown>
              <Dropdown
                menu={{ items: userMenuItems }}
                placement="bottomRight"
                arrow
                trigger={['click']}
              >
                <div className="user-info">
                  <Avatar
                    icon={<UserOutlined />}
                    src={user?.avatar}
                    style={{ marginRight: 8 }}
                  />
                  {!collapsed && (
                    <span className="username">{user?.fullName}</span>
                  )}
                </div>
              </Dropdown>
            </div>
          </div>
        </Header>
        <Content className="main-content">
          <div className="content-container">
            {children}
          </div>
        </Content>
      </Layout>
    </Layout>
  );
};

export default MainLayout;