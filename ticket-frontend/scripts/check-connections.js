// check-connections.js
// Script kiểm tra kết nối đến tất cả các microservices

const axios = require('axios');
const dotenv = require('dotenv');
const path = require('path');
const fs = require('fs');

// Load biến môi trường từ file .env
const envPath = path.resolve(process.cwd(), '.env');
if (fs.existsSync(envPath)) {
  dotenv.config({ path: envPath });
} else {
  console.log('\x1b[33m%s\x1b[0m', 'Không tìm thấy file .env, sử dụng .env.example...');
  dotenv.config({ path: path.resolve(process.cwd(), '.env.example') });
}

// Danh sách services cần kiểm tra
const services = [
  { 
    name: 'API Gateway', 
    url: process.env.VITE_API_BASE_URL || 'http://localhost:8080',
    endpoint: '/health' 
  },
  { 
    name: 'User Service', 
    url: process.env.VITE_USER_SERVICE_URL || 'http://localhost:8000',
    endpoint: '/health' 
  },
  { 
    name: 'Ticket Service', 
    url: process.env.VITE_TICKET_SERVICE_URL || 'http://localhost:8001',
    endpoint: '/health' 
  },
  { 
    name: 'File Service', 
    url: process.env.VITE_FILE_SERVICE_URL || 'http://localhost:8002',
    endpoint: '/health' 
  },
  { 
    name: 'Notification Service', 
    url: process.env.VITE_NOTIFICATION_SERVICE_URL || 'http://localhost:8003',
    endpoint: '/health' 
  },
  { 
    name: 'Report Service', 
    url: process.env.VITE_REPORT_SERVICE_URL || 'http://localhost:8004',
    endpoint: '/health' 
  },
  { 
    name: 'Analytics Service', 
    url: process.env.VITE_ANALYTICS_SERVICE_URL || 'http://localhost:8005',
    endpoint: '/health' 
  }
];

// Kiểm tra kết nối
async function checkConnections() {
  console.log('\x1b[36m%s\x1b[0m', '============================================');
  console.log('\x1b[36m%s\x1b[0m', '   KIỂM TRA KẾT NỐI ĐẾN MICROSERVICES     ');
  console.log('\x1b[36m%s\x1b[0m', '============================================');
  console.log();

  let allSuccessful = true;
  const startTime = Date.now();

  for (const service of services) {
    process.stdout.write(`Kiểm tra ${service.name} (${service.url})... `);
    
    try {
      const response = await axios.get(`${service.url}${service.endpoint}`, {
        timeout: 5000,
        validateStatus: () => true
      });
      
      if (response.status >= 200 && response.status < 500) {
        console.log('\x1b[32m%s\x1b[0m', 'KẾT NỐI THÀNH CÔNG');
        console.log(`  Phản hồi: HTTP ${response.status} - ${JSON.stringify(response.data || {})}`);
      } else {
        console.log('\x1b[33m%s\x1b[0m', 'KẾT NỐI ĐƯỢC NHƯNG CÓ LỖI');
        console.log(`  Phản hồi: HTTP ${response.status}`);
        allSuccessful = false;
      }
    } catch (error) {
      console.log('\x1b[31m%s\x1b[0m', 'KHÔNG THỂ KẾT NỐI');
      console.log(`  Lỗi: ${error.message}`);
      allSuccessful = false;
    }
    
    console.log();
  }

  const duration = (Date.now() - startTime) / 1000;
  
  console.log('\x1b[36m%s\x1b[0m', '============================================');
  if (allSuccessful) {
    console.log('\x1b[32m%s\x1b[0m', 'TẤT CẢ CÁC MICROSERVICES ĐỀU HOẠT ĐỘNG TỐT!');
  } else {
    console.log('\x1b[33m%s\x1b[0m', 'MỘT SỐ MICROSERVICES KHÔNG HOẠT ĐỘNG ĐÚNG.');
    console.log('\x1b[33m%s\x1b[0m', 'Vui lòng kiểm tra xem các services đã được khởi động chưa.');
    console.log('\x1b[33m%s\x1b[0m', 'Sử dụng lệnh: .\\run_local_enhanced.ps1 start');
  }
  console.log('\x1b[36m%s\x1b[0m', `Thời gian kiểm tra: ${duration.toFixed(2)} giây`);
  console.log('\x1b[36m%s\x1b[0m', '============================================');
}

// Thực thi kiểm tra
checkConnections().catch(error => {
  console.error('Lỗi không mong muốn:', error);
  process.exit(1);
});