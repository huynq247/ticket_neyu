const { createProxyMiddleware } = require('http-proxy-middleware');
const { getConfig } = require('./config');
const { authMiddleware } = require('./middleware/auth-middleware');

/**
 * Setup proxies for microservices
 * @param {Express} app - Express application
 */
const setupProxies = (app) => {
  const config = getConfig();
  const { services } = config;

  // Configure proxy middleware for each service
  if (services.user) {
    const userServiceProxy = createProxyMiddleware({
      target: services.user.url,
      changeOrigin: true,
      pathRewrite: {
        [`^/api/user`]: '/api/v1',
      },
      logLevel: 'debug'
    });
    
    // Apply authentication middleware to protected routes
    app.use('/api/user', authMiddleware, userServiceProxy);
    
    // Allow direct access to auth endpoints without authentication
    app.use('/api/auth', createProxyMiddleware({
      target: services.user.url,
      changeOrigin: true,
      pathRewrite: {
        [`^/api/auth`]: '/api/v1/auth',
      },
      logLevel: 'debug'
    }));
  }

  if (services.ticket) {
    const ticketServiceProxy = createProxyMiddleware({
      target: services.ticket.url,
      changeOrigin: true,
      pathRewrite: {
        [`^/api/ticket`]: '/api/v1',
      },
      logLevel: 'debug'
    });
    
    app.use('/api/ticket', authMiddleware, ticketServiceProxy);
  }

  if (services.file) {
    const fileServiceProxy = createProxyMiddleware({
      target: services.file.url,
      changeOrigin: true,
      pathRewrite: {
        [`^/api/file`]: '/api/v1',
      },
      logLevel: 'debug'
    });
    
    app.use('/api/file', authMiddleware, fileServiceProxy);
  }

  if (services.notification) {
    const notificationServiceProxy = createProxyMiddleware({
      target: services.notification.url,
      changeOrigin: true,
      pathRewrite: {
        [`^/api/notification`]: '/api/v1',
      },
      logLevel: 'debug'
    });
    
    app.use('/api/notification', authMiddleware, notificationServiceProxy);
  }

  // Add more services as needed
};

module.exports = { setupProxies };