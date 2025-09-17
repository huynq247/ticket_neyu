import React from 'react';
import { Navigate } from 'react-router-dom';
import { hasPermission, hasAnyPermission, hasAllPermissions } from '@/utils/permissionUtils';

interface PermissionGuardProps {
  permissionId?: string;
  permissions?: string[];
  requireAll?: boolean;
  children: React.ReactNode;
  fallback?: React.ReactNode;
  redirectTo?: string;
}

/**
 * Component bảo vệ (Guard) dựa trên quyền người dùng
 * 
 * @param permissionId - ID của quyền cần kiểm tra (khi chỉ cần một quyền)
 * @param permissions - Danh sách các quyền cần kiểm tra (khi cần nhiều quyền)
 * @param requireAll - Nếu true, yêu cầu tất cả quyền. Nếu false, chỉ cần một quyền
 * @param children - Nội dung sẽ hiển thị nếu người dùng có quyền
 * @param fallback - Nội dung sẽ hiển thị nếu người dùng không có quyền (tuỳ chọn)
 * @param redirectTo - Đường dẫn sẽ chuyển hướng đến nếu người dùng không có quyền (tuỳ chọn)
 */
const PermissionGuard: React.FC<PermissionGuardProps> = ({
  permissionId,
  permissions = [],
  requireAll = false,
  children,
  fallback,
  redirectTo = '/unauthorized',
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

  // Nếu không có quyền
  if (fallback) {
    // Hiển thị fallback nếu được cung cấp
    return <>{fallback}</>;
  }

  // Chuyển hướng nếu không có fallback
  return <Navigate to={redirectTo} replace />;
};

export default PermissionGuard;