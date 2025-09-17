import React, { useState, useEffect } from 'react';
import { Modal, Form, Input, Button, message, Divider, Collapse, Typography, Spin, Space, Tag, Checkbox } from 'antd';
import { createRole, updateRole, getPermissions } from '@/api/roleService';
import { Role } from '@/types';

const { TextArea } = Input;
const { Text } = Typography;
const { Panel } = Collapse;

interface RoleFormModalProps {
  visible: boolean;
  role: Role | null;
  onClose: (refresh?: boolean) => void;
}

// Interface for API permission which might not have all fields
interface ApiPermission {
  id: string;
  name: string;
  description?: string;
  category: string;
}

const RoleFormModal: React.FC<RoleFormModalProps> = ({ visible, role, onClose }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState<boolean>(false);
  const [permissionsByCategory, setPermissionsByCategory] = useState<Record<string, ApiPermission[]>>({});
  const [loadingPermissions, setLoadingPermissions] = useState<boolean>(false);

  const isEditing = !!role;
  const title = isEditing ? 'Edit Role' : 'Create New Role';

  useEffect(() => {
    if (visible) {
      // Reset form when modal opens
      form.resetFields();
      
      // If editing, set form values
      if (isEditing && role) {
        form.setFieldsValue({
          name: role.name,
          description: role.description,
          permissions: role.permissions.map(p => typeof p === 'string' ? p : p.id),
        });
      }
      
      // Fetch permissions
      fetchPermissions();
    }
  }, [visible, isEditing, role]);

  const fetchPermissions = async () => {
    try {
      setLoadingPermissions(true);
      const response = await getPermissions();
      const fetchedPermissions = response.data.permissions as ApiPermission[];
      
      // Group permissions by category
      const groupedPermissions = fetchedPermissions.reduce((acc, permission) => {
        const category = permission.category || 'Other';
        if (!acc[category]) {
          acc[category] = [];
        }
        acc[category].push(permission);
        return acc;
      }, {} as Record<string, ApiPermission[]>);
      
      setPermissionsByCategory(groupedPermissions);
    } catch (error) {
      console.error('Error fetching permissions:', error);
      message.error('Failed to load permissions');
    } finally {
      setLoadingPermissions(false);
    }
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);
      
      if (isEditing && role) {
        // Update existing role
        await updateRole(role.id, values);
        message.success('Role updated successfully');
      } else {
        // Create new role
        await createRole(values);
        message.success('Role created successfully');
      }
      
      onClose(true); // Close modal and refresh list
    } catch (error: any) {
      console.error('Error saving role:', error);
      let errorMessage = 'Failed to save role';
      
      // Check for specific error messages from the API
      if (error.response && error.response.data && error.response.data.detail) {
        errorMessage = `Error: ${error.response.data.detail}`;
      }
      
      message.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    onClose();
  };

  // Function to select all permissions in a category
  const selectAllInCategory = (category: string) => {
    const permissionsInCategory = permissionsByCategory[category] || [];
    const permissionIds = permissionsInCategory.map(p => p.id);
    
    // Get current selected permissions
    const currentSelected = form.getFieldValue('permissions') || [];
    
    // Add all permissions from this category
    const newSelected = [...new Set([...currentSelected, ...permissionIds])];
    
    form.setFieldsValue({ permissions: newSelected });
  };

  // Function to clear all permissions in a category
  const clearAllInCategory = (category: string) => {
    const permissionsInCategory = permissionsByCategory[category] || [];
    const permissionIds = permissionsInCategory.map(p => p.id);
    
    // Get current selected permissions
    const currentSelected = form.getFieldValue('permissions') || [];
    
    // Remove all permissions from this category
    const newSelected = currentSelected.filter((id: string) => !permissionIds.includes(id));
    
    form.setFieldsValue({ permissions: newSelected });
  };

  return (
    <Modal
      title={title}
      open={visible}
      onCancel={handleCancel}
      width={700}
      footer={[
        <Button key="cancel" onClick={handleCancel}>
          Cancel
        </Button>,
        <Button 
          key="submit" 
          type="primary" 
          loading={loading} 
          onClick={handleSubmit}
        >
          {isEditing ? 'Update' : 'Create'}
        </Button>,
      ]}
    >
      <Form
        form={form}
        layout="vertical"
      >
        <Form.Item
          name="name"
          label="Role Name"
          rules={[{ required: true, message: 'Please enter the role name' }]}
        >
          <Input />
        </Form.Item>
        
        <Form.Item
          name="description"
          label="Description"
        >
          <TextArea rows={3} />
        </Form.Item>
        
        <Divider orientation="left">Permissions</Divider>
        
        {loadingPermissions ? (
          <div style={{ textAlign: 'center', padding: '20px' }}>
            <Spin tip="Loading permissions..." />
          </div>
        ) : (
          <Form.Item
            name="permissions"
            rules={[{ required: true, message: 'Please select at least one permission' }]}
          >
            <Collapse>
              {Object.keys(permissionsByCategory).map(category => (
                <Panel 
                  header={
                    <Space>
                      <Text strong>{category}</Text>
                      <Tag color="blue">{permissionsByCategory[category].length} permissions</Tag>
                      <Button 
                        size="small" 
                        onClick={(e) => {
                          e.stopPropagation();
                          selectAllInCategory(category);
                        }}
                      >
                        Select All
                      </Button>
                      <Button 
                        size="small" 
                        onClick={(e) => {
                          e.stopPropagation();
                          clearAllInCategory(category);
                        }}
                      >
                        Clear
                      </Button>
                    </Space>
                  } 
                  key={category}
                >
                  <Checkbox.Group>
                    {permissionsByCategory[category].map(permission => (
                      <div key={permission.id} style={{ marginBottom: 8 }}>
                        <Form.Item 
                          name={['permissions']} 
                          valuePropName="checked" 
                          noStyle
                        >
                          <Checkbox value={permission.id}>
                            <Space direction="vertical" size={0}>
                              <Text strong>{permission.name}</Text>
                              <Text type="secondary">{permission.description}</Text>
                            </Space>
                          </Checkbox>
                        </Form.Item>
                      </div>
                    ))}
                  </Checkbox.Group>
                </Panel>
              ))}
            </Collapse>
          </Form.Item>
        )}
      </Form>
    </Modal>
  );
};

export default RoleFormModal;