import React from 'react';
import { hasPermission, hasAnyPermission, hasAllPermissions } from '@/utils/permissionUtils';

interface PermissionControlProps {
  permissionId?: string;
  permissions?: string[];
  requireAll?: boolean;
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

/**
 * Component kiểm soát hiển thị dựa trên quyền
 * 
 * @param permissionId - ID của quyền cần kiểm tra (khi chỉ cần một quyền)
 * @param permissions - Danh sách các quyền cần kiểm tra (khi cần nhiều quyền)
 * @param requireAll - Nếu true, yêu cầu tất cả quyền. Nếu false, chỉ cần một quyền
 * @param children - Nội dung sẽ hiển thị nếu người dùng có quyền
 * @param fallback - Nội dung sẽ hiển thị nếu người dùng không có quyền (tuỳ chọn)
 */
const PermissionControl: React.FC<PermissionControlProps> = ({
  permissionId,
  permissions = [],
  requireAll = false,
  children,
  fallback = null,
}) => {
  // Kiểm tra quyền dựa trên các thuộc tính được cung cấp
  let hasAccess = false;

  if (permissionId) {
    // Nếu có permissionId riêng lẻ
    hasAccess = hasPermission(permissionId);
  } else if (permissions.length > 0) {
    // Nếu có danh sách permissions
    hasAccess = requireAll
      ? hasAllPermissions(permissions)
      : hasAnyPermission(permissions);
  } else {
    // Nếu không có yêu cầu quyền, cho phép truy cập
    hasAccess = true;
  }

  // Nếu có quyền, hiển thị nội dung con
  if (hasAccess) {
    return <>{children}</>;
  }

  // Nếu không có quyền, hiển thị fallback hoặc null
  return <>{fallback}</>;
};

export default PermissionControl;