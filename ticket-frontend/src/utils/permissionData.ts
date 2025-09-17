/**
 * Danh sách mặc định các permission trong hệ thống
 * Được sử dụng khi API không trả về hoặc chưa có dữ liệu
 */

export const DEFAULT_PERMISSIONS = [
  // Ticket Permissions
  {
    id: 'ticket:view',
    name: 'View Tickets',
    description: 'Xem danh sách và chi tiết ticket',
    category: 'Ticket'
  },
  {
    id: 'ticket:create',
    name: 'Create Tickets',
    description: 'Tạo ticket mới',
    category: 'Ticket'
  },
  {
    id: 'ticket:update',
    name: 'Update Tickets',
    description: 'Cập nhật thông tin ticket',
    category: 'Ticket'
  },
  {
    id: 'ticket:delete',
    name: 'Delete Tickets',
    description: 'Xóa ticket',
    category: 'Ticket'
  },
  {
    id: 'ticket:assign',
    name: 'Assign Tickets',
    description: 'Phân công ticket cho người dùng khác',
    category: 'Ticket'
  },
  {
    id: 'ticket:comment',
    name: 'Comment on Tickets',
    description: 'Thêm bình luận vào ticket',
    category: 'Ticket'
  },
  {
    id: 'ticket:change-status',
    name: 'Change Ticket Status',
    description: 'Thay đổi trạng thái của ticket',
    category: 'Ticket'
  },
  {
    id: 'ticket:view-all',
    name: 'View All Tickets',
    description: 'Xem tất cả ticket trong hệ thống (không giới hạn bởi phòng ban)',
    category: 'Ticket'
  },
  
  // User Permissions
  {
    id: 'user:view',
    name: 'View Users',
    description: 'Xem danh sách và thông tin người dùng',
    category: 'User'
  },
  {
    id: 'user:create',
    name: 'Create Users',
    description: 'Tạo người dùng mới',
    category: 'User'
  },
  {
    id: 'user:update',
    name: 'Update Users',
    description: 'Cập nhật thông tin người dùng',
    category: 'User'
  },
  {
    id: 'user:delete',
    name: 'Delete Users',
    description: 'Xóa người dùng',
    category: 'User'
  },
  
  // Role Permissions
  {
    id: 'role:view',
    name: 'View Roles',
    description: 'Xem danh sách và chi tiết vai trò',
    category: 'Role'
  },
  {
    id: 'role:create',
    name: 'Create Roles',
    description: 'Tạo vai trò mới',
    category: 'Role'
  },
  {
    id: 'role:update',
    name: 'Update Roles',
    description: 'Cập nhật thông tin vai trò',
    category: 'Role'
  },
  {
    id: 'role:delete',
    name: 'Delete Roles',
    description: 'Xóa vai trò',
    category: 'Role'
  },
  {
    id: 'role:assign',
    name: 'Assign Roles',
    description: 'Gán vai trò cho người dùng',
    category: 'Role'
  },
  
  // Department Permissions
  {
    id: 'department:view',
    name: 'View Departments',
    description: 'Xem danh sách và chi tiết phòng ban',
    category: 'Department'
  },
  {
    id: 'department:create',
    name: 'Create Departments',
    description: 'Tạo phòng ban mới',
    category: 'Department'
  },
  {
    id: 'department:update',
    name: 'Update Departments',
    description: 'Cập nhật thông tin phòng ban',
    category: 'Department'
  },
  {
    id: 'department:delete',
    name: 'Delete Departments',
    description: 'Xóa phòng ban',
    category: 'Department'
  },
  {
    id: 'department:manage-members',
    name: 'Manage Department Members',
    description: 'Thêm/xóa thành viên của phòng ban',
    category: 'Department'
  },
  
  // Dispatcher/Coordinator Permissions
  {
    id: 'dispatcher:assign',
    name: 'Assign as Dispatcher',
    description: 'Chỉ định người dùng làm Dispatcher',
    category: 'Dispatcher'
  },
  {
    id: 'dispatcher:remove',
    name: 'Remove Dispatcher',
    description: 'Xóa vai trò Dispatcher của người dùng',
    category: 'Dispatcher'
  },
  {
    id: 'coordinator:assign',
    name: 'Assign as Coordinator',
    description: 'Chỉ định người dùng làm Coordinator',
    category: 'Coordinator'
  },
  {
    id: 'coordinator:remove',
    name: 'Remove Coordinator',
    description: 'Xóa vai trò Coordinator của người dùng',
    category: 'Coordinator'
  },
  
  // Report Permissions
  {
    id: 'report:view',
    name: 'View Reports',
    description: 'Xem báo cáo',
    category: 'Report'
  },
  {
    id: 'report:create',
    name: 'Create Reports',
    description: 'Tạo báo cáo mới',
    category: 'Report'
  },
  {
    id: 'report:export',
    name: 'Export Reports',
    description: 'Xuất báo cáo ra file',
    category: 'Report'
  },
  
  // Analytics Permissions
  {
    id: 'analytics:view',
    name: 'View Analytics',
    description: 'Xem dữ liệu phân tích',
    category: 'Analytics'
  },
  {
    id: 'analytics:advanced',
    name: 'Advanced Analytics',
    description: 'Sử dụng tính năng phân tích nâng cao',
    category: 'Analytics'
  },
  
  // System Permissions
  {
    id: 'system:settings',
    name: 'Manage System Settings',
    description: 'Quản lý cài đặt hệ thống',
    category: 'System'
  },
  {
    id: 'system:logs',
    name: 'View System Logs',
    description: 'Xem nhật ký hệ thống',
    category: 'System'
  },
  {
    id: 'system:backup',
    name: 'Backup & Restore',
    description: 'Sao lưu và khôi phục dữ liệu',
    category: 'System'
  },
  
  // Project Permissions
  {
    id: 'project:view',
    name: 'View Projects',
    description: 'Xem danh sách và chi tiết dự án',
    category: 'Project'
  },
  {
    id: 'project:create',
    name: 'Create Projects',
    description: 'Tạo dự án mới',
    category: 'Project'
  },
  {
    id: 'project:update',
    name: 'Update Projects',
    description: 'Cập nhật thông tin dự án',
    category: 'Project'
  },
  {
    id: 'project:delete',
    name: 'Delete Projects',
    description: 'Xóa dự án',
    category: 'Project'
  },
  {
    id: 'project:manage-members',
    name: 'Manage Project Members',
    description: 'Thêm/xóa thành viên dự án',
    category: 'Project'
  }
];