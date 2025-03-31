# Deployment Guide for Traditional Matchmaking Telegram Bot

This guide provides detailed instructions for deploying and maintaining the Traditional Matchmaking Telegram Bot.

## Server Requirements

- **Operating System**: Ubuntu 20.04 LTS or newer
- **RAM**: Minimum 1GB, recommended 2GB+
- **Storage**: Minimum 10GB available space
- **Python**: Version 3.8 or higher
- **Network**: Stable internet connection with outbound access to Telegram API servers

## Step-by-Step Deployment

### 1. Server Preparation

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required system dependencies
sudo apt install -y python3-pip python3-venv git

# Create a dedicated user for the bot (optional but recommended)
sudo adduser botuser
sudo usermod -aG sudo botuser
su - botuser
```

### 2. Bot Setup

```bash
# Clone the repository or upload your files
git clone https://github.com/yourusername/traditional-matchmaking-bot.git
cd traditional-matchmaking-bot

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
# If requirements.txt is not available, install the core dependencies:
pip install python-telegram-bot SQLAlchemy
```

### 3. Configuration

```bash
# Create data directory
mkdir -p data

# Set up environment variables
echo 'export BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"' >> ~/.bashrc
source ~/.bashrc

# Alternatively, create a .env file
echo "BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN" > .env
```

Edit the `src/config.py` file to customize settings:

```python
# Example configuration changes
MAX_DAILY_MATCHES = 10  # Increase daily match limit
DEFAULT_LANGUAGE = "ar"  # Set Arabic as default language
```

### 4. Database Initialization

```bash
# Initialize the database
python -c "from src.database import init_db; init_db()"
```

### 5. Test Run

```bash
# Run the bot in test mode
python run.py
```

Verify the bot is working by sending a `/start` command to your bot on Telegram.

### 6. Production Deployment

#### Option A: Systemd Service (Recommended)

Create a systemd service file for reliable operation:

```bash
sudo nano /etc/systemd/system/matchmaking-bot.service
```

Add the following content:

```
[Unit]
Description=Traditional Matchmaking Telegram Bot
After=network.target

[Service]
User=botuser
Group=botuser
WorkingDirectory=/home/botuser/traditional-matchmaking-bot
ExecStart=/home/botuser/traditional-matchmaking-bot/venv/bin/python run.py
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=matchmaking-bot
Environment="BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN"

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable matchmaking-bot.service
sudo systemctl start matchmaking-bot.service
sudo systemctl status matchmaking-bot.service
```

#### Option B: Screen Session

For simpler deployments, use screen:

```bash
sudo apt install screen
screen -S matchmaking-bot
source venv/bin/activate
python run.py

# Press Ctrl+A, then D to detach from the screen session
# To reattach later:
screen -r matchmaking-bot
```

#### Option C: Docker Deployment

If you prefer Docker:

1. Create a Dockerfile:

```
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run.py"]
```

2. Build and run the Docker container:

```bash
docker build -t matchmaking-bot .
docker run -d --name matchmaking-bot -e BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN matchmaking-bot
```

### 7. Monitoring and Logging

Set up logging to monitor bot activity:

```bash
# View systemd service logs
sudo journalctl -u matchmaking-bot.service -f

# Set up log rotation
sudo nano /etc/logrotate.d/matchmaking-bot
```

Add the following content:

```
/var/log/matchmaking-bot.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 640 botuser botuser
}
```

## Backup and Recovery

### Regular Backups

Set up a cron job for daily database backups:

```bash
crontab -e
```

Add the following line:

```
0 2 * * * cd /home/botuser/traditional-matchmaking-bot && sqlite3 data/matchmaking.db .dump > /home/botuser/backups/matchmaking_$(date +\%Y\%m\%d).sql
```

### Recovery Procedure

To restore from a backup:

```bash
cd /home/botuser/traditional-matchmaking-bot
sqlite3 data/matchmaking.db < /home/botuser/backups/matchmaking_YYYYMMDD.sql
```

## Security Hardening

1. **Firewall Configuration**:

```bash
sudo ufw allow ssh
sudo ufw allow 443/tcp
sudo ufw enable
```

2. **Secure the Database**:

```bash
# Set proper permissions
chmod 600 data/matchmaking.db
```

3. **Regular Updates**:

```bash
# Set up automatic security updates
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

## Scaling Considerations

As your user base grows:

1. **Database Migration**: Consider migrating from SQLite to PostgreSQL for better performance with many users.

2. **Load Balancing**: For very large deployments, implement multiple bot instances with a load balancer.

3. **Caching**: Implement Redis caching for frequently accessed data.

## Troubleshooting

### Common Issues and Solutions

1. **Bot Not Responding**:
   - Check service status: `sudo systemctl status matchmaking-bot.service`
   - Verify internet connectivity: `ping api.telegram.org`
   - Check logs for errors: `sudo journalctl -u matchmaking-bot.service -n 100`

2. **Database Errors**:
   - Check file permissions: `ls -la data/matchmaking.db`
   - Verify database integrity: `sqlite3 data/matchmaking.db "PRAGMA integrity_check;"`

3. **Memory Issues**:
   - Check memory usage: `free -m`
   - Monitor process resources: `top -u botuser`

## Maintenance Schedule

Recommended maintenance routine:

- **Daily**: Check logs for errors
- **Weekly**: Verify backups are working
- **Monthly**: Update dependencies and apply security patches
- **Quarterly**: Review and optimize database performance

## Contact and Support

For technical support or questions about deployment, please contact:

[Your Contact Information]
