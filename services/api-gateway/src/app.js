require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');

const { setupProxies } = require('./proxy');
const routes = require('./routes');
const { errorHandler } = require('./middleware/error-handler');
const { getConfig } = require('./config');

// Initialize Express app
const app = express();
const config = getConfig();

// Apply basic security middleware
app.use(helmet());
app.use(cors({
  origin: config.corsOrigins,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// Apply rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  standardHeaders: true,
  legacyHeaders: false
});
app.use(limiter);

// Logging
app.use(morgan('combined'));

// Parse JSON
app.use(express.json());

// Setup service proxies
setupProxies(app);

// Register routes
app.use('/api', routes);

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok', service: 'api-gateway' });
});

// Error handling middleware
app.use(errorHandler);

// Export app for testing
module.exports = app;