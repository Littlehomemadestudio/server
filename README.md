# 🤖 Bale Military Strategy Bot

A Persian/Farsi Telegram bot for Bale messenger that simulates a military strategy game with country-specific units, economic systems, and 13-15 day progression timeline.

## 🚀 Quick Setup

### 1. Install Python
Make sure you have Python 3.7+ installed on your system.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get Your Bot Token
1. Go to [@BotFather](https://t.me/BotFather) on Telegram
2. Create a new bot with `/newbot`
3. Copy your bot token
4. Replace the token in `bale_bot.py`:

```python
TOKEN = "YOUR_BOT_TOKEN_HERE"
```

### 4. Run the Bot
```bash
python bale_bot.py
```

## 📱 How to Use

### For Players:
1. Start the bot: `/start`
2. View countries: `/countries`
3. Select country: `/select_country iran` (or usa, russia, etc.)
4. Collect income: `/income` (every hour)
5. Buy military assets: `/buy militia 10`
6. Research technology: `/research military_engineering`
7. View your army: `/military`
8. View technologies: `/tech`

### Available Countries:
- 🇺🇸 **USA** (usa) - Military superpower
- 🇷🇺 **Russia** (russia) - Nuclear technology
- 🇨🇳 **China** (china) - Manufacturing power
- 🇮🇷 **Iran** (iran) - Regional power with oil
- 🇩🇪 **Germany** (germany) - Engineering excellence
- 🇯🇵 **Japan** (japan) - Advanced technology
- 🇬🇧 **UK** (uk) - Financial power
- 🇫🇷 **France** (france) - Culture and luxury
- 🇮🇳 **India** (india) - IT services
- 🇰🇷 **South Korea** (south_korea) - Electronics
- 🇮🇱 **Israel** (israel) - Cybersecurity

## 🎮 Game Features

### Country-Specific Units
Each country has exclusive military units:

**Iran Examples:**
- Sejjil missile ($800K)
- Shahed-136 drone ($25K) 
- Karrar tank ($4.8M)
- Quds Force ($320K)

**USA Examples:**
- F-22 Raptor ($85M)
- Navy SEALs ($300K)
- Minuteman ICBM ($55M)

### Progression Timeline
- **Days 1-3**: Basic setup, select country
- **Days 4-7**: Mid-tier units, basic research
- **Days 8-12**: Advanced military, stealth tech
- **Days 13-15**: Nuclear weapons, future tech

### Economic System
- Hourly income collection
- Country-specific income sources
- Level and technology bonuses
- Balanced 13-15 day progression

## 🛠️ Technical Details

### File Structure
```
/workspace/
├── bale_bot.py          # Main bot file (simplified)
├── bot.py               # Full bot file (complete)
├── requirements.txt     # Dependencies
├── README.md           # This file
└── progression_analysis.md  # Detailed analysis
```

### Data Storage
- `group_data.json` - Group-specific data
- `global_user_data.json` - User progress (persistent across groups)

### Key Commands
```
/start - Start the bot
/countries - Show available countries
/select_country [code] - Select your country
/income - Collect hourly income
/buy [asset] [quantity] - Buy military assets
/research [tech] - Research technology
/military - View your army
/tech - View technology tree
/help - Show help
```

## 🔧 Customization

### Adding New Countries
Edit the `AVAILABLE_COUNTRIES` dictionary in `bale_bot.py`:

```python
"new_country": {
    "name": "🏳️ New Country",
    "description": "Description here",
    "starting_money": 600000,
    "income_methods": {
        "method1": {"name": "Income Source", "base_income": 200000, "multiplier": 1.5}
    },
    "bonus": "Special bonus +20%"
}
```

### Adding New Military Assets
Edit the `MILITARY_ASSETS` dictionary:

```python
"new_asset": {
    "cost": 1000000,
    "power": 50,
    "name": "Asset Name",
    "ability": "Special ability",
    "tech_required": "required_tech",
    "country_restricted": "country_code"  # or None for all countries
}
```

## 🐛 Troubleshooting

### Common Issues:

1. **"Module not found" error**
   ```bash
   pip install python-bale-bot
   ```

2. **Bot doesn't respond**
   - Check your bot token
   - Make sure bot is added to the group
   - Check console for errors

3. **Data not saving**
   - Check file permissions
   - Make sure the bot has write access

### Debug Mode
Add this to enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Game Balance

The bot is balanced for 13-15 day progression:
- Starting money: $450K-$800K
- Hourly income: $400K-$800K (with bonuses)
- Most expensive items: $120M+ (nuclear weapons)
- Daily income potential: $15M-$25M

## 🤝 Contributing

Feel free to:
- Add new countries
- Create new military units
- Improve game balance
- Add new features
- Fix bugs

## 📝 License

This project is open source. Feel free to modify and distribute.

## 🎯 Support

If you need help:
1. Check this README
2. Look at the code comments
3. Test with `/help` command
4. Check console output for errors

---

**Happy Gaming! 🎮**