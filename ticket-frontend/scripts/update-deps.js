#!/usr/bin/env node

/**
 * Cập nhật dependencies cho dự án
 * Script này sẽ kiểm tra và cập nhật các dependencies trong package.json
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Màu sắc cho console
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
};

// Đường dẫn đến file package.json
const packageJsonPath = path.resolve(process.cwd(), 'package.json');

// Kiểm tra xem file package.json có tồn tại không
if (!fs.existsSync(packageJsonPath)) {
  console.error(`${colors.red}Không tìm thấy file package.json!${colors.reset}`);
  process.exit(1);
}

// Đọc file package.json
const packageJson = require(packageJsonPath);

console.log(`${colors.cyan}${colors.bright}=== KIỂM TRA VÀ CẬP NHẬT DEPENDENCIES ===${colors.reset}\n`);

// Kiểm tra outdated packages
console.log(`${colors.yellow}Đang kiểm tra các packages đã cũ...${colors.reset}`);
try {
  const outdatedOutput = execSync('npm outdated --json', { encoding: 'utf8' });
  const outdatedPackages = JSON.parse(outdatedOutput || '{}');
  
  if (Object.keys(outdatedPackages).length === 0) {
    console.log(`${colors.green}Tất cả các packages đều đã cập nhật mới nhất!${colors.reset}\n`);
  } else {
    console.log(`${colors.yellow}Các packages cần cập nhật:${colors.reset}\n`);
    
    console.log(`${colors.bright}Tên package\t\tPhiên bản hiện tại\tPhiên bản mới nhất${colors.reset}`);
    console.log(`${colors.dim}--------------------------------------------------------${colors.reset}`);
    
    for (const packageName in outdatedPackages) {
      const packageInfo = outdatedPackages[packageName];
      console.log(`${packageName}\t\t${packageInfo.current}\t\t${packageInfo.latest}`);
    }
    
    console.log('\n');
    
    rl.question(`${colors.yellow}Bạn có muốn cập nhật tất cả các packages không? (y/n) ${colors.reset}`, (answer) => {
      if (answer.toLowerCase() === 'y') {
        console.log(`${colors.cyan}Đang cập nhật các packages...${colors.reset}`);
        try {
          execSync('npm update', { stdio: 'inherit' });
          console.log(`${colors.green}Cập nhật thành công!${colors.reset}`);
        } catch (error) {
          console.error(`${colors.red}Lỗi khi cập nhật: ${error.message}${colors.reset}`);
        }
      } else {
        console.log(`${colors.yellow}Đã hủy cập nhật.${colors.reset}`);
      }
      rl.close();
    });
  }
} catch (error) {
  console.error(`${colors.red}Lỗi khi kiểm tra packages: ${error.message}${colors.reset}`);
  process.exit(1);
}