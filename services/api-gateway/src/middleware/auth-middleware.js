const jwt = require('jsonwebtoken');
const { getConfig } = require('../config');

/**
 * Authentication middleware
 * Validates JWT token from Authorization header
 */
const authMiddleware = (req, res, next) => {
  const config = getConfig();
  
  // Skip auth for OPTIONS requests (CORS preflight)
  if (req.method === 'OPTIONS') {
    return next();
  }

  // Get token from Authorization header
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'No token provided' });
  }

  const token = authHeader.split(' ')[1];
  
  try {
    // Verify token
    const decoded = jwt.verify(token, config.jwtSecret);
    
    // Add user info to request object
    req.user = decoded;
    
    next();
  } catch (error) {
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({ error: 'Token expired' });
    }
    
    return res.status(401).json({ error: 'Invalid token' });
  }
};

module.exports = { authMiddleware };