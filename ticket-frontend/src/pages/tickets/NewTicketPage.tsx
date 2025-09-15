import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Typography,
  Card,
  Form,
  Input,
  Select,
  DatePicker,
  Button,
  message,
  Space,
  Upload,
  Row,
  Col,
  Divider,
  Spin
} from 'antd';
import {
  UploadOutlined,
  SaveOutlined,
  CloseOutlined,
} from '@ant-design/icons';
import MainLayout from '@/components/layout/MainLayout';
import { TicketPriority, TicketCreateRequest } from '@/types';
import ticketService from '@/api/ticketService';
import './NewTicketPage.css';

const { Title } = Typography;
const { Option } = Select;
const { TextArea } = Input;

const NewTicketPage: React.FC = () => {
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const [fileList, setFileList] = useState<any[]>([]);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (values: any) => {
    try {
      setSubmitting(true);
      
      // Prepare the request object
      const ticketData: TicketCreateRequest = {
        title: values.title,
        description: values.description,
        priority: values.priority,
        category: values.category,
        dueDate: values.dueDate?.toISOString(),
        tags: values.tags,
        assignedTo: values.assignedTo,
      };

      // Convert fileList to proper File[] for attachments
      if (fileList.length > 0) {
        const files = fileList.map((file) => file.originFileObj);
        ticketData.attachments = files;
      }

      // Submit the ticket through the API
      await ticketService.createTicket(ticketData);
      
      message.success('Ticket created successfully');
      navigate('/tickets');
    } catch (error) {
      console.error('Error creating ticket:', error);
      message.error('Failed to create ticket');
    } finally {
      setSubmitting(false);
    }
  };

  const handleCancel = () => {
    navigate('/tickets');
  };

  const handleFileChange = ({ fileList }: any) => {
    setFileList(fileList);
  };

  return (
    <MainLayout>
      <div className="new-ticket-container">
        {/* Header */}
        <div className="new-ticket-header">
          <Title level={2}>Create New Ticket</Title>
        </div>

        {/* Ticket Form */}
        <Card className="new-ticket-form-card">
          <Spin spinning={submitting}>
            <Form
              form={form}
              layout="vertical"
              onFinish={handleSubmit}
              initialValues={{
                priority: TicketPriority.MEDIUM,
              }}
            >
            <Row gutter={16}>
              <Col span={24}>
                <Form.Item
                  name="title"
                  label="Title"
                  rules={[{ required: true, message: 'Please enter the ticket title' }]}
                >
                  <Input placeholder="Enter a descriptive title" />
                </Form.Item>
              </Col>
            </Row>

            <Row gutter={16}>
              <Col span={24}>
                <Form.Item
                  name="description"
                  label="Description"
                  rules={[{ required: true, message: 'Please enter a description' }]}
                >
                  <TextArea
                    rows={6}
                    placeholder="Describe the issue or request in detail"
                  />
                </Form.Item>
              </Col>
            </Row>

            <Row gutter={16}>
              <Col xs={24} sm={12}>
                <Form.Item
                  name="category"
                  label="Category"
                  rules={[{ required: true, message: 'Please select a category' }]}
                >
                  <Select placeholder="Select a category">
                    <Option value="Bug">Bug</Option>
                    <Option value="Feature Request">Feature Request</Option>
                    <Option value="Enhancement">Enhancement</Option>
                    <Option value="Support">Support</Option>
                  </Select>
                </Form.Item>
              </Col>
              <Col xs={24} sm={12}>
                <Form.Item
                  name="priority"
                  label="Priority"
                  rules={[{ required: true, message: 'Please select a priority' }]}
                >
                  <Select placeholder="Select priority">
                    {Object.values(TicketPriority).map((priority) => (
                      <Option key={priority} value={priority}>
                        {priority.toUpperCase()}
                      </Option>
                    ))}
                  </Select>
                </Form.Item>
              </Col>
            </Row>

            <Row gutter={16}>
              <Col xs={24} sm={12}>
                <Form.Item
                  name="assignedTo"
                  label="Assigned To"
                >
                  <Select placeholder="Select assignee (optional)">
                    <Option value="John Doe">John Doe</Option>
                    <Option value="Jane Smith">Jane Smith</Option>
                    <Option value="Alice Johnson">Alice Johnson</Option>
                  </Select>
                </Form.Item>
              </Col>
              <Col xs={24} sm={12}>
                <Form.Item
                  name="dueDate"
                  label="Due Date"
                >
                  <DatePicker style={{ width: '100%' }} />
                </Form.Item>
              </Col>
            </Row>

            <Row gutter={16}>
              <Col span={24}>
                <Form.Item
                  name="tags"
                  label="Tags"
                >
                  <Select
                    mode="tags"
                    style={{ width: '100%' }}
                    placeholder="Add tags (press Enter after each tag)"
                    tokenSeparators={[',']}
                  />
                </Form.Item>
              </Col>
            </Row>

            <Divider />

            <Row gutter={16}>
              <Col span={24}>
                <Form.Item
                  name="attachments"
                  label="Attachments"
                >
                  <Upload
                    listType="text"
                    fileList={fileList}
                    onChange={handleFileChange}
                    beforeUpload={() => false} // Prevent auto upload
                  >
                    <Button icon={<UploadOutlined />}>Attach Files</Button>
                  </Upload>
                </Form.Item>
              </Col>
            </Row>

            <Divider />

            <div className="form-actions">
              <Space>
                <Button
                  type="primary"
                  htmlType="submit"
                  icon={<SaveOutlined />}
                  loading={submitting}
                >
                  Create Ticket
                </Button>
                <Button
                  icon={<CloseOutlined />}
                  onClick={handleCancel}
                >
                  Cancel
                </Button>
              </Space>
            </div>
          </Form>
          </Spin>
        </Card>
      </div>
    </MainLayout>
  );
};

export default NewTicketPage;