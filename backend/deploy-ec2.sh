#!/bin/bash

# HostelConnect Backend Deployment Script for AWS EC2
# Run this script on your EC2 instance

set -e

echo "🚀 Starting HostelConnect Backend Deployment..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python 3.11 and pip
echo "🐍 Installing Python 3.11..."
sudo apt install -y python3.11 python3.11-venv python3-pip

# Install MySQL client (for database connections)
echo "🗄️ Installing MySQL client..."
sudo apt install -y mysql-client

# Install Nginx
echo "🌐 Installing Nginx..."
sudo apt install -y nginx

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /var/www/hostelconnect
sudo chown -R ubuntu:ubuntu /var/www/hostelconnect

# Clone or copy your application code here
# Replace with your actual deployment method
echo "📋 Copy your application code to /var/www/hostelconnect"
echo "For example: git clone https://github.com/your-repo/hostelconnect.git /var/www/hostelconnect"

# Navigate to application directory
cd /var/www/hostelconnect/backend

# Create virtual environment
echo "🔧 Creating Python virtual environment..."
python3.11 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file (replace with your actual values)
echo "⚙️ Creating environment configuration..."
cat > .env << EOF
# Database Configuration (AWS RDS)
DB_HOST=your-rds-endpoint.rds.amazonaws.com
DB_USER=your-db-username
DB_PASSWORD=your-db-password
DB_NAME=hostelconnect_db

# Flask Secret Key
SECRET_KEY=your-very-secure-secret-key-here

# Email Configuration (SMTP)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# CORS Configuration
FRONTEND_URL=https://your-vercel-app.vercel.app

# Production Settings
LOG_LEVEL=INFO
EOF

# Create systemd service for the application
echo "🔄 Creating systemd service..."
sudo tee /etc/systemd/system/hostelconnect.service > /dev/null <<EOF
[Unit]
Description=HostelConnect Flask Application
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/var/www/hostelconnect/backend
Environment="PATH=/var/www/hostelconnect/backend/venv/bin"
ExecStart=/var/www/hostelconnect/backend/venv/bin/gunicorn --bind 127.0.0.1:8000 --workers 3 --threads 2 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
echo "🌐 Configuring Nginx..."
sudo cp nginx.conf /etc/nginx/sites-available/hostelconnect
sudo ln -sf /etc/nginx/sites-available/hostelconnect /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Start and enable services
echo "▶️ Starting services..."
sudo systemctl daemon-reload
sudo systemctl start hostelconnect
sudo systemctl enable hostelconnect
sudo systemctl start nginx
sudo systemctl enable nginx

# Configure firewall
echo "🔥 Configuring firewall..."
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

# Create log rotation
echo "📝 Setting up log rotation..."
sudo tee /etc/logrotate.d/hostelconnect > /dev/null <<EOF
/var/www/hostelconnect/backend/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 ubuntu ubuntu
    postrotate
        systemctl reload hostelconnect
    endscript
}
EOF

echo "✅ Deployment completed successfully!"
echo ""
echo "🔍 Next steps:"
echo "1. Update the .env file with your actual credentials"
echo "2. Test the application: curl http://localhost/health"
echo "3. Check logs: sudo journalctl -u hostelconnect -f"
echo "4. Set up SSL certificate with Let's Encrypt (optional)"
echo ""
echo "🌐 Your application should be available at:"
echo "   http://your-ec2-public-ip"
echo "   (Replace with your actual EC2 public IP)"