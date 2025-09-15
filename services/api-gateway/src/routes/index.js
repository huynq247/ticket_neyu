const express = require('express');
const router = express.Router();

// Simple status route
router.get('/status', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    services: {
      user: process.env.USER_SERVICE_URL ? 'configured' : 'not configured',
      ticket: process.env.TICKET_SERVICE_URL ? 'configured' : 'not configured',
      file: process.env.FILE_SERVICE_URL ? 'configured' : 'not configured',
      notification: process.env.NOTIFICATION_SERVICE_URL ? 'configured' : 'not configured',
    }
  });
});

module.exports = router;