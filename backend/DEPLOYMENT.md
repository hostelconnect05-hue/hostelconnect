# HostelConnect Backend - AWS Deployment Guide

## Overview

This backend is configured for production deployment on AWS EC2 with RDS MySQL and Cloudinary for file storage.

## Prerequisites

- AWS EC2 instance (Ubuntu 22.04 recommended)
- AWS RDS MySQL database
- Cloudinary account for file storage
- Domain name (optional, for production)

## Environment Variables

Copy `.env.example` to `.env` and fill in your actual values:

```bash
cp .env.example .env
nano .env
```

Required variables:
- `DB_HOST`: Your RDS endpoint
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_NAME`: Database name
- `SECRET_KEY`: Flask secret key (generate a secure random string)
- `SMTP_EMAIL` & `SMTP_PASSWORD`: For email functionality
- `CLOUDINARY_*`: Cloudinary credentials
- `FRONTEND_URL`: Your Vercel frontend URL

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

## Production Deployment

### Option 1: Manual EC2 Setup

1. Launch EC2 instance (Ubuntu 22.04, t3.micro or larger)
2. SSH into your instance
3. Run the deployment script:

```bash
# Upload deploy-ec2.sh to your EC2 instance
chmod +x deploy-ec2.sh
sudo ./deploy-ec2.sh
```

4. Update the `.env` file with your actual credentials
5. Restart the service:

```bash
sudo systemctl restart hostelconnect
```

### Option 2: Docker Deployment

```bash
# Build and run with Docker
docker build -t hostelconnect-backend .
docker run -d -p 8000:8000 --env-file .env hostelconnect-backend
```

## Database Setup

1. Create RDS MySQL instance
2. Run the database schema:

```bash
mysql -h your-rds-endpoint -u username -p database_name < database_schema.sql
```

3. Optionally run seed data:

```bash
python seed_optional_data.py
```

## Cloudinary Setup

1. Sign up at [Cloudinary](https://cloudinary.com)
2. Get your cloud name, API key, and API secret
3. Configure in `.env` file

## Nginx Configuration

The included `nginx.conf` provides:
- Reverse proxy to Flask app
- SSL-ready configuration
- Security headers
- Gzip compression
- Static file serving

## Monitoring

Check application status:
```bash
sudo systemctl status hostelconnect
sudo journalctl -u hostelconnect -f
```

Health check endpoint: `GET /health`

## Security Considerations

- Use strong, unique passwords
- Enable RDS encryption
- Configure security groups properly
- Use HTTPS in production
- Regularly update dependencies
- Monitor logs for suspicious activity

## Troubleshooting

### Common Issues

1. **Database connection fails**
   - Check RDS security group allows EC2 instance
   - Verify credentials in `.env`

2. **Cloudinary uploads fail**
   - Verify API credentials
   - Check quota limits

3. **CORS errors**
   - Ensure `FRONTEND_URL` matches your Vercel domain
   - Include protocol (https://)

4. **Memory issues**
   - Monitor with `htop` or `free -h`
   - Adjust Gunicorn workers if needed

### Logs

Application logs:
```bash
sudo journalctl -u hostelconnect -f
```

Nginx logs:
```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

## Performance Tuning

- Adjust Gunicorn workers based on CPU cores
- Configure RDS instance size appropriately
- Use Cloudinary transformations for image optimization
- Implement caching if needed

## Backup Strategy

- RDS automated backups
- Regular database exports
- Cloudinary asset backups (if critical)
- EC2 instance snapshots