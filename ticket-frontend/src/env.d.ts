/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string;
  readonly VITE_API_TIMEOUT: string;
  readonly VITE_USER_SERVICE_URL: string;
  readonly VITE_TICKET_SERVICE_URL: string;
  readonly VITE_FILE_SERVICE_URL: string;
  readonly VITE_NOTIFICATION_SERVICE_URL: string;
  readonly VITE_REPORT_SERVICE_URL: string;
  readonly VITE_ANALYTICS_SERVICE_URL: string;
  readonly VITE_AUTH_STORAGE_KEY: string;
  readonly VITE_AUTH_EXPIRY_DAYS: string;
  readonly VITE_ENABLE_SOCKET_NOTIFICATIONS: string;
  readonly VITE_ENABLE_ANALYTICS: string;
  readonly VITE_DEV_SERVER_PORT: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}