# Traditional Matchmaking Telegram Bot

A culturally-sensitive semi-dating Telegram bot designed specifically for Saudi Arabia and GCC nationals, focusing on traditional values and respectful interactions.

## Features

- **Cultural Sensitivity**: Designed with respect for Saudi Arabian and GCC cultural norms and traditions
- **Bilingual Support**: Full Arabic and English language support
- **Personality Matching**: Integration of 16 personalities test for compatibility assessment
- **Horoscope Integration**: Optional astrological compatibility features
- **Religious Preferences**: Detailed religious preference settings (moderate, liberal, conservative)
- **Covering Options**: Preferences for different covering styles (niqab, hijab, etc.)
- **Family Involvement**: Options for family supervision of conversations
- **Privacy Controls**: Comprehensive privacy settings for user comfort
- **Mutual Matching**: Group creation only when both parties express interest
- **Legal Protection**: Comprehensive terms and conditions and privacy policy

## Installation and Deployment

### Prerequisites

- Python 3.8 or higher
- A Telegram Bot Token (obtained from BotFather)
- Internet-connected server or hosting environment

### Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/traditional-matchmaking-bot.git
cd traditional-matchmaking-bot
```

2. **Install dependencies**

```bash
pip install python-telegram-bot SQLAlchemy
```

3. **Set up environment variables**

Create a `.env` file in the root directory with the following content:

```
BOT_TOKEN=your_telegram_bot_token_here
```

Alternatively, you can edit the `config.py` file directly to add your bot token.

4. **Initialize the database**

```bash
mkdir -p data
python -c "from src.database import init_db; init_db()"
```

5. **Run the bot**

```bash
python run.py
```

### Deployment Options

#### Option 1: Local Server

Run the bot on a local server with internet access:

```bash
nohup python run.py > bot.log 2>&1 &
```

This will keep the bot running in the background even after you close the terminal.

#### Option 2: Cloud Hosting

Deploy the bot on a cloud platform like Heroku, AWS, or DigitalOcean:

1. **Heroku Deployment**

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login to Heroku
heroku login

# Create a new Heroku app
heroku create traditional-matchmaking-bot

# Add a Procfile
echo "worker: python run.py" > Procfile

# Push to Heroku
git push heroku main

# Scale the worker dyno
heroku ps:scale worker=1

# Set environment variables
heroku config:set BOT_TOKEN=your_telegram_bot_token_here
```

2. **Docker Deployment**

```bash
# Build Docker image
docker build -t traditional-matchmaking-bot .

# Run Docker container
docker run -d --name matchmaking-bot -e BOT_TOKEN=your_telegram_bot_token_here traditional-matchmaking-bot
```

## Bot Registration and Setup

1. **Create a new bot with BotFather**
   - Open Telegram and search for @BotFather
   - Send the command `/newbot`
   - Follow the instructions to create a new bot
   - Copy the API token provided by BotFather

2. **Configure bot settings with BotFather**
   - Set a profile picture: `/setuserpic`
   - Set bot description: `/setdescription`
   - Set about text: `/setabouttext`
   - Set commands list: `/setcommands`

3. **Suggested commands list for BotFather**

```
start - Start the bot and set up your profile
profile - View or edit your profile
matches - View potential matches
conversations - View your active conversations
settings - Adjust your preferences and settings
language - Change language (English/Arabic)
help - Get help and support
terms - View terms and conditions
privacy - View privacy policy
```

## Customization

### Language Settings

Edit the translation files in `src/translations` directory to modify or add languages.

### Matching Algorithm

Adjust the weights and compatibility calculations in `src/matching.py` to customize the matching algorithm.

### User Interface

Modify the conversation handlers in `src/bot.py` to customize the user interface and flow.

## Security Considerations

- The bot stores sensitive user information. Ensure your server has appropriate security measures.
- Regular database backups are recommended.
- Consider implementing additional encryption for message storage.
- Review and update the Terms and Conditions and Privacy Policy regularly.

## Legal Disclaimer

This bot includes comprehensive Terms and Conditions and Privacy Policy documents that:
- Establish data ownership and usage rights
- Limit liability for misuse or abuse
- Clarify the alpha/demo status of the service
- Protect against claims from family members or spouses
- Establish age restrictions (18+)

Ensure users accept these terms before using the service.

## Maintenance

### Regular Updates

- Check for updates to the python-telegram-bot library
- Monitor Telegram Bot API changes
- Update the matching algorithm based on user feedback

### Database Maintenance

- Periodically clean up old conversations and expired matches
- Optimize database performance
- Back up user data regularly

## Troubleshooting

### Common Issues

1. **Bot not responding**
   - Check if the bot process is running
   - Verify the bot token is correct
   - Ensure internet connectivity

2. **Database errors**
   - Check file permissions for the database file
   - Verify SQLAlchemy is properly installed
   - Check for database corruption

3. **Memory issues**
   - Monitor server resources
   - Implement pagination for large result sets
   - Clean up old data periodically

## Support

For support, please contact [your contact information].

## License

[Your license information]
