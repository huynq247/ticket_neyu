import { DEFAULT_PERMISSIONS } from './permissionData';
import { Permission, Role } from '@/types';

// Interface để lưu trữ quyền được cache
interface PermissionCache {
  permissions: string[];
  timestamp: number;
}

// Định nghĩa cấu trúc AuthState tối thiểu mà chúng ta cần
interface AuthState {
  user?: {
    roles?: Role[];
  };
  token?: string;
}

// Cache quyền của người dùng để tránh truy vấn nhiều lần
let userPermissionCache: PermissionCache | null = null;
// Thời gian cache hợp lệ (15 phút)
const CACHE_VALID_TIME = 15 * 60 * 1000;

/**
 * Lấy trạng thái xác thực hiện tại
 */
export const getAuthState = (): AuthState => {
  // Lấy token từ localStorage
  const token = localStorage.getItem('token') || undefined;
  
  // Thử lấy thông tin user từ localStorage nếu có
  let user = undefined;
  const userJson = localStorage.getItem('user');
  if (userJson) {
    try {
      user = JSON.parse(userJson);
    } catch (e) {
      console.error('Failed to parse user from localStorage');
    }
  }
  
  return { user, token };
};

/**
 * Lấy tất cả quyền của người dùng hiện tại
 * @returns Danh sách các permission id của người dùng
 */
export const getUserPermissions = (): string[] => {
  const authState = getAuthState();
  
  // Nếu không có user hoặc token, không có quyền nào
  if (!authState || !authState.user || !authState.token) {
    return [];
  }

  // Kiểm tra cache
  const currentTime = Date.now();
  if (
    userPermissionCache &&
    currentTime - userPermissionCache.timestamp < CACHE_VALID_TIME
  ) {
    return userPermissionCache.permissions;
  }

  // Lấy danh sách quyền từ user
  const permissions: string[] = [];
  
  // Duyệt qua tất cả vai trò của người dùng
  if (authState.user.roles && authState.user.roles.length > 0) {
    authState.user.roles.forEach((role: Role) => {
      // Thêm tất cả quyền từ vai trò vào danh sách
      if (role.permissions && role.permissions.length > 0) {
        role.permissions.forEach((permission: Permission | string) => {
          if (typeof permission === 'string') {
            permissions.push(permission);
          } else if (permission.id) {
            permissions.push(permission.id);
          }
        });
      }
    });
  }

  // Cache lại kết quả
  userPermissionCache = {
    permissions: [...new Set(permissions)], // Loại bỏ các quyền trùng lặp
    timestamp: currentTime,
  };

  return userPermissionCache.permissions;
};

/**
 * Kiểm tra xem người dùng có quyền cụ thể không
 * @param permissionId ID của quyền cần kiểm tra
 * @returns true nếu có quyền, false nếu không
 */
export const hasPermission = (permissionId: string): boolean => {
  // Admin luôn có tất cả quyền
  if (isAdmin()) {
    return true;
  }
  
  // Manager có quyền xem analytics và các quyền liên quan đến ticket
  if (isManager() && (
    permissionId.startsWith('analytics:') || 
    permissionId.startsWith('ticket:')
  )) {
    return true;
  }
  
  const userPermissions = getUserPermissions();
  return userPermissions.includes(permissionId);
};

/**
 * Kiểm tra xem người dùng có ít nhất một trong các quyền được chỉ định không
 * @param permissionIds Danh sách các quyền cần kiểm tra
 * @returns true nếu có ít nhất một quyền, false nếu không
 */
export const hasAnyPermission = (permissionIds: string[]): boolean => {
  // Admin luôn có tất cả quyền
  if (isAdmin()) {
    return true;
  }
  
  // Manager có quyền xem analytics và các quyền liên quan đến ticket
  if (isManager() && permissionIds.some(id => 
    id.startsWith('analytics:') || 
    id.startsWith('ticket:')
  )) {
    return true;
  }
  
  const userPermissions = getUserPermissions();
  return permissionIds.some(id => userPermissions.includes(id));
};

/**
 * Kiểm tra xem người dùng có tất cả các quyền được chỉ định không
 * @param permissionIds Danh sách các quyền cần kiểm tra
 * @returns true nếu có tất cả quyền, false nếu không
 */
export const hasAllPermissions = (permissionIds: string[]): boolean => {
  // Admin luôn có tất cả quyền
  if (isAdmin()) {
    return true;
  }
  
  // Manager có quyền xem analytics và các quyền liên quan đến ticket
  if (isManager() && permissionIds.every(id => 
    id.startsWith('analytics:') || 
    id.startsWith('ticket:')
  )) {
    return true;
  }
  
  const userPermissions = getUserPermissions();
  return permissionIds.every(id => userPermissions.includes(id));
};

/**
 * Kiểm tra xem người dùng có phải là admin không
 * @returns true nếu là admin, false nếu không
 */
export const isAdmin = (): boolean => {
  const authState = getAuthState();
  
  if (!authState || !authState.user || !authState.user.roles) {
    return false;
  }
  
  // Kiểm tra xem người dùng có vai trò admin không
  return authState.user.roles.some((role: Role) => 
    role.name.toLowerCase() === 'admin' || 
    role.name.toLowerCase() === 'administrator'
  );
};

/**
 * Kiểm tra xem người dùng có phải là manager không
 * @returns true nếu là manager, false nếu không
 */
export const isManager = (): boolean => {
  const authState = getAuthState();
  
  if (!authState || !authState.user || !authState.user.roles) {
    return false;
  }
  
  // Kiểm tra xem người dùng có vai trò manager không
  return authState.user.roles.some((role: Role) => 
    role.name.toLowerCase() === 'manager'
  );
};

/**
 * Reset cache quyền của người dùng
 * Gọi hàm này khi người dùng đăng nhập, đăng xuất, hoặc vai trò/quyền của họ thay đổi
 */
export const resetPermissionCache = (): void => {
  userPermissionCache = null;
};

/**
 * Lấy mô tả chi tiết của một quyền từ ID
 * @param permissionId ID của quyền
 * @returns Thông tin chi tiết về quyền, hoặc undefined nếu không tìm thấy
 */
export const getPermissionDetails = (permissionId: string): Permission | undefined => {
  return DEFAULT_PERMISSIONS.find(p => p.id === permissionId) as Permission | undefined;
};

/**
 * Kiểm tra xem người dùng có quyền truy cập tính năng không
 * @param featurePermissions Danh sách các quyền cần thiết cho tính năng
 * @param requireAll Nếu true, yêu cầu tất cả quyền. Nếu false, chỉ cần một quyền
 * @returns true nếu có quyền truy cập, false nếu không
 */
export const canAccessFeature = (
  featurePermissions: string[],
  requireAll: boolean = false
): boolean => {
  return requireAll
    ? hasAllPermissions(featurePermissions)
    : hasAnyPermission(featurePermissions);
};