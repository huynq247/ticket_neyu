import React, { useState, useEffect } from 'react';
import { Button, Card, Typography, Space, List, Tag, Divider } from 'antd';
import MainLayout from '@/components/layout/MainLayout';
import { getUserPermissions, resetPermissionCache } from '@/utils/permissionUtils';
import { useAuth } from '@/context/AuthContext';

const { Title, Text, Paragraph } = Typography;

const DebugPage: React.FC = () => {
  const [userPermissions, setUserPermissions] = useState<string[]>([]);
  const [savedToken, setSavedToken] = useState<string | null>(null);
  const [savedUser, setSavedUser] = useState<any>(null);
  const { user, logout } = useAuth();

  useEffect(() => {
    // Lấy quyền của người dùng
    const permissions = getUserPermissions();
    setUserPermissions(permissions);

    // Lấy token từ localStorage
    const token = localStorage.getItem('auth_token');
    setSavedToken(token);

    // Lấy thông tin người dùng từ localStorage
    const userJson = localStorage.getItem('user');
    if (userJson) {
      try {
        setSavedUser(JSON.parse(userJson));
      } catch (e) {
        console.error('Failed to parse user from localStorage');
      }
    }
  }, []);

  const handleResetCache = () => {
    resetPermissionCache();
    alert('Đã xóa cache quyền thành công! Trang sẽ tải lại...');
    window.location.reload();
  };

  const handleLogout = () => {
    logout();
    window.location.href = '/login';
  };

  return (
    <MainLayout>
      <div style={{ padding: '24px' }}>
        <Title level={2}>Debug Auth & Permissions</Title>
        <Paragraph>
          Trang này hiển thị thông tin về trạng thái xác thực và quyền của người dùng hiện tại.
        </Paragraph>

        <Space direction="vertical" style={{ width: '100%' }} size="large">
          <Card title="Thông tin xác thực" bordered>
            <Paragraph>
              <Text strong>Token trong localStorage:</Text> {savedToken ? <Tag color="green">Có</Tag> : <Tag color="red">Không</Tag>}
            </Paragraph>
            {savedToken && (
              <Paragraph>
                <Text strong>Token:</Text> {savedToken}
              </Paragraph>
            )}
          </Card>

          <Card title="Thông tin người dùng (từ context)" bordered>
            {user ? (
              <>
                <Paragraph>
                  <Text strong>ID:</Text> {user.id}
                </Paragraph>
                <Paragraph>
                  <Text strong>Email:</Text> {user.email}
                </Paragraph>
                <Paragraph>
                  <Text strong>Tên:</Text> {user.fullName || `${user.firstName} ${user.lastName}`}
                </Paragraph>
                <Paragraph>
                  <Text strong>Vai trò:</Text>
                  <List
                    size="small"
                    dataSource={user.roles || []}
                    renderItem={(role) => (
                      <List.Item>
                        <Text>
                          {role.name} - {role.description}
                        </Text>
                      </List.Item>
                    )}
                  />
                </Paragraph>
              </>
            ) : (
              <Text type="danger">Không có thông tin người dùng trong context</Text>
            )}
          </Card>

          <Card title="Thông tin người dùng (từ localStorage)" bordered>
            {savedUser ? (
              <>
                <Paragraph>
                  <Text strong>ID:</Text> {savedUser.id}
                </Paragraph>
                <Paragraph>
                  <Text strong>Email:</Text> {savedUser.email}
                </Paragraph>
                <Paragraph>
                  <Text strong>Tên:</Text> {savedUser.fullName || `${savedUser.firstName} ${savedUser.lastName}`}
                </Paragraph>
                <Paragraph>
                  <Text strong>Vai trò:</Text>
                  <List
                    size="small"
                    dataSource={savedUser.roles || []}
                    renderItem={(role: any) => (
                      <List.Item>
                        <Text>
                          {role.name} - {role.description}
                        </Text>
                      </List.Item>
                    )}
                  />
                </Paragraph>
              </>
            ) : (
              <Text type="danger">Không có thông tin người dùng trong localStorage</Text>
            )}
          </Card>

          <Card title="Quyền người dùng" bordered>
            {userPermissions.length > 0 ? (
              <List
                size="small"
                dataSource={userPermissions}
                renderItem={(permission) => (
                  <List.Item>
                    <Tag color="blue">{permission}</Tag>
                  </List.Item>
                )}
              />
            ) : (
              <Text type="danger">Không có quyền nào</Text>
            )}
          </Card>

          <Divider />

          <Space>
            <Button type="primary" onClick={handleResetCache}>
              Xóa cache quyền
            </Button>
            <Button danger onClick={handleLogout}>
              Đăng xuất
            </Button>
          </Space>
        </Space>
      </div>
    </MainLayout>
  );
};

export default DebugPage;