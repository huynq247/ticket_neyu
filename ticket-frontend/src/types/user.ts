import { Role } from './role';

export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  fullName?: string; // Thêm fullName
  roles: Role[];
  isActive: boolean;
  phoneNumber?: string;
  department?: string;
  position?: string;
  avatar?: string; // Thêm avatar
  createdAt: string;
  updatedAt: string;
}