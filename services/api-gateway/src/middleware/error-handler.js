/**
 * Global error handler middleware
 */
const errorHandler = (err, req, res, next) => {
  console.error('Error:', err);
  
  // Default error message
  const statusCode = err.statusCode || 500;
  const message = err.message || 'Internal Server Error';
  
  // Customize response based on error type
  if (err.name === 'ProxyError') {
    return res.status(502).json({
      error: 'Bad Gateway',
      message: 'Service is temporarily unavailable'
    });
  }
  
  return res.status(statusCode).json({
    error: statusCode >= 500 ? 'Internal Server Error' : message
  });
};

module.exports = { errorHandler };