/**
 * Get configuration based on environment
 * @returns {Object} Configuration object
 */
const getConfig = () => {
  // Default configuration for development
  const config = {
    port: process.env.PORT || 3000,
    corsOrigins: process.env.CORS_ORIGINS ? process.env.CORS_ORIGINS.split(',') : ['http://localhost:3000', 'http://localhost:8080'],
    jwtSecret: process.env.JWT_SECRET || 'your-secret-key-for-jwt',
    services: {
      user: {
        url: process.env.USER_SERVICE_URL || 'http://localhost:8000',
        timeout: parseInt(process.env.USER_SERVICE_TIMEOUT || '5000'),
      },
      ticket: {
        url: process.env.TICKET_SERVICE_URL || 'http://localhost:8001',
        timeout: parseInt(process.env.TICKET_SERVICE_TIMEOUT || '5000'),
      },
      file: {
        url: process.env.FILE_SERVICE_URL || 'http://localhost:8002',
        timeout: parseInt(process.env.FILE_SERVICE_TIMEOUT || '5000'),
      },
      notification: {
        url: process.env.NOTIFICATION_SERVICE_URL || 'http://localhost:8003',
        timeout: parseInt(process.env.NOTIFICATION_SERVICE_TIMEOUT || '5000'),
      },
      // Add more services as needed
    }
  };

  // Override with production settings if in production
  if (process.env.NODE_ENV === 'production') {
    // Production-specific overrides
    config.corsOrigins = process.env.CORS_ORIGINS ? process.env.CORS_ORIGINS.split(',') : ['https://yourproductionapp.com'];
    
    // Make sure to use proper secret in production
    if (!process.env.JWT_SECRET) {
      console.warn('WARNING: JWT_SECRET not set in production environment!');
    }
  }

  return config;
};

module.exports = { getConfig };