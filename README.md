<div align="center">    
  
<img width="2048" height="807" alt="изображение" src="https://github.com/user-attachments/assets/9b454e3d-3c64-4e5e-9025-9f24b124ee41" />

</div>

###

<div align="center">

## 📌 Overview

</div>

###

---

## ✨ Features

### 🔍 **Cookie Checking**
- Full account statistics analysis
- Balance, pending Robux, RAP calculation
- Badges and gamepass verification
- Rare items detection (Headless, Korblox, etc.)
- Premium status and billing information
- Email verification status

### 🎮 **Game-Specific Checks**
- Support for 30+ popular Roblox games
- Game-specific badges and gamepass verification
- In-game donation tracking
- Playtime statistics
- Detailed game reports

### 🛠 **Cookie Management Tools**
- **Cookie Validator** – Quick validity checks
- **Cookie Refresher** – Mass cookie refresh using external API
- **Cookie Bypasser** – Mass cookie bypass functionality
- **Cookie Sorter** – Merge multiple files and remove duplicates
- **Cookie Splitter** – Split cookies into individual files

### 📊 **Advanced Features**
- Configurable check parameters
- Multiple output formats (ZIP/TXT)
- Queue system with VIP priority
- Proxy support for checking
- Referral system with bonus checks
- Admin panel with moderation tools
- Mass notifications and user management

## 🚀 Quick Start

### 1. **Prerequisites**
```bash
Python 3.8+
Required packages: aiogram, aiohttp, pytz
```

### 2. **Configuration**
```python
# Bot configuration
BOT_TOKEN = 'your_bot_token_here'
ADMINS = [admin_id_1, admin_id_2]  # Telegram admin IDs
CRYPTOBOT_API_KEY = 'your_cryptobot_key'  # For VIP payments
DISCORD_WEBHOOK_URL = 'your_webhook_url'  # For notifications
```

### 3. **Installation**
```bash
# Clone and install dependencies
git clone <repository_url>
cd simple-cookie
pip install -r requirements.txt

# Create necessary directories
mkdir Users filesforcookie

# Run the bot
python main.py
```

## 📁 Project Structure
```
simple-cookie/
├── Users/                 # User databases and configs
├── filesforcookie/        # Temporary cookie files
├── main.py               # Main bot file
├── proxies.txt           # Proxy list (optional)
└── README.md             # This file
```

## 🎮 Supported Games
The bot supports checking for over 30 popular Roblox games including:
- **Adopt Me**, **Blox Fruits**, **BedWars**, **Pet Simulator 99**
- **Jailbreak**, **Murder Mystery 2**, **Bee Swarm Simulator**
- **Anime Adventures**, **Tower Defense Simulator**, **Royal High**
- And many more with detailed badge and gamepass tracking

## 💰 VIP System
- **Priority queue** – VIP users skip the line
- **Unlimited checks** – No daily limits
- **Faster processing** – Priority processing
- **Payment methods**: Telegram Stars or CryptoBot (USDT)

## 🔧 Commands

### User Commands
- `/start` – Start the bot
- `/ref` – Referral program
- **Cookie Check** – Main checking interface
- **Check Game** – Game-specific checking
- **Profile** – User profile and statistics
- **Sorter** – Cookie merging tool
- **Valid Checker** – Quick validity checks
- **Cookie Refresh** – Mass refresh cookies
- **Cookie Bypass** – Mass bypass cookies
- **Cookie Splitter** – Split cookies into files

### Admin Commands
- `/ban` – Ban users
- `/unban` – Unban users
- `/restart` – Restart all checks
- `/setproxy` – Set proxy list
- `/listproxy` – Show proxy list
- `/post` – Mass notification
- `/soob` – Send personal message

## ⚙️ Technical Details

### Cookie Validation
- Multiple proxy support with rotation
- Concurrent checking (50 threads)
- Retry mechanism (5 attempts)
- Duplicate detection and removal

### Database Structure
```json
{
  "user_id": {
    "config": {
      "cookie_check_count": 0,
      "registration_date": "2024-01-01",
      "badges": [],
      "gamepasses": [],
      "check_params": {},
      "output_format": {},
      "game_settings": {},
      "playtime_settings": {},
      "is_vip": false,
      "referral_code": "ABC123",
      "bonus_checks": 0
    }
  }
}
```

### Queue System
- Priority-based queue (VIP > Regular)
- Real-time queue position updates
- Automatic retry on failure
- Progress tracking with notifications

## 🛡️ Security Features
- User ban system with reason tracking
- Cookie validation before processing
- Secure payment processing
- Admin-only commands
- Rate limiting on free checks

## 📈 Statistics Tracking
- Daily check limits (5 free checks/day)
- Referral bonuses (3 extra checks per referral)
- Total checks performed
- Valid/Invalid cookie statistics
- User activity tracking

## 🔄 API Integration
- **CryptoBot API** – For VIP payments
- **External refresh API** – For cookie refreshing
- **External bypass API** – For cookie bypassing
- **Discord Webhooks** – For notifications

## 🐛 Troubleshooting

### Common Issues
1. **"File not found"** – Ensure the file is in TXT format
2. **"Invalid cookie format"** – Check cookie structure
3. **"Queue full"** – Wait or purchase VIP for priority
4. **"API error"** – External service might be down

### Logs
Check `bot.log` for detailed error information:
```bash
tail -f bot.log
```

## 🤝 Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License
This project is for educational purposes only. Users are responsible for complying with Roblox's Terms of Service.

## ⚠️ Disclaimer
This tool is designed for educational and research purposes only. The developers are not responsible for any misuse of this software. Always ensure you have permission to check any cookies and comply with all applicable laws and terms of service.

## 🔗 Links
- **Developer**: [@oindc](https://t.me/oindc)

---

*Last updated: January 2024*
