export interface Role {
  id: string;
  name: string;
  description?: string;
  permissions: Permission[] | string[];
  createdAt: string;
  updatedAt: string;
}

export interface Permission {
  id: string;
  name: string;
  description?: string;
  category: string;
  createdAt?: string;
  updatedAt?: string;
}