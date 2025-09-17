import React, { useState, useEffect } from 'react';
import { Button, Table, Space, Modal, message, Input } from 'antd';
import { EditOutlined, DeleteOutlined, PlusOutlined, SearchOutlined } from '@ant-design/icons';
import { getRoles, deleteRole } from '@/api/roleService';
import { Role } from '@/types';
import RoleFormModal from '@/components/users/RoleFormModal';

const RoleManagementPage: React.FC = () => {
  const [roles, setRoles] = useState<Role[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [isModalVisible, setIsModalVisible] = useState<boolean>(false);
  const [currentRole, setCurrentRole] = useState<Role | null>(null);
  const [searchText, setSearchText] = useState<string>('');

  const fetchRoles = async () => {
    try {
      setLoading(true);
      const response = await getRoles({ search: searchText });
      setRoles(response.data.roles);
    } catch (error) {
      console.error('Error fetching roles:', error);
      message.error('Failed to fetch roles');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRoles();
  }, [searchText]);

  const handleCreate = () => {
    setCurrentRole(null);
    setIsModalVisible(true);
  };

  const handleEdit = (role: Role) => {
    setCurrentRole(role);
    setIsModalVisible(true);
  };

  const handleDelete = (roleId: string) => {
    Modal.confirm({
      title: 'Are you sure you want to delete this role?',
      content: 'This action cannot be undone and may affect users with this role.',
      okText: 'Yes',
      okType: 'danger',
      cancelText: 'No',
      onOk: async () => {
        try {
          await deleteRole(roleId);
          message.success('Role deleted successfully');
          fetchRoles();
        } catch (error) {
          console.error('Error deleting role:', error);
          message.error('Failed to delete role');
        }
      },
    });
  };

  const handleModalClose = (refresh: boolean = false) => {
    setIsModalVisible(false);
    if (refresh) {
      fetchRoles();
    }
  };

  const handleSearch = (value: string) => {
    setSearchText(value);
  };

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      sorter: (a: Role, b: Role) => a.name.localeCompare(b.name),
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
      render: (text: string) => text || 'No description',
    },
    {
      title: 'Permissions',
      dataIndex: 'permissions',
      key: 'permissions',
      render: (permissions: any[]) => `${permissions?.length || 0} permissions`,
    },
    {
      title: 'Created At',
      dataIndex: 'createdAt',
      key: 'createdAt',
      render: (date: string) => new Date(date).toLocaleDateString(),
      sorter: (a: Role, b: Role) => new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime(),
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: Role) => (
        <Space size="middle">
          <Button
            type="primary"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
            size="small"
          >
            Edit
          </Button>
          <Button
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDelete(record.id)}
            size="small"
          >
            Delete
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div className="role-management-page">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
        <h1>Role Management</h1>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={handleCreate}
        >
          Create New Role
        </Button>
      </div>

      <div className="filters" style={{ marginBottom: 16 }}>
        <Input
          placeholder="Search roles..."
          value={searchText}
          onChange={(e) => handleSearch(e.target.value)}
          style={{ width: 300 }}
          prefix={<SearchOutlined />}
        />
      </div>

      <Table
        columns={columns}
        dataSource={roles}
        rowKey="id"
        loading={loading}
      />

      <RoleFormModal
        visible={isModalVisible}
        role={currentRole}
        onClose={handleModalClose}
      />
    </div>
  );
};

export default RoleManagementPage;