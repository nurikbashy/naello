# 🎮 Naello - Mathematical Quiz Bot

A Telegram bot for playing mathematical quizzes and earning NULL tokens! Answer questions correctly and convert your earnings to checks.

## Features

✨ **Core Features:**
- 🎯 Mathematical questions in groups (addition, subtraction, multiplication, division)
- 💰 Earn NULL tokens based on answer speed
- 📊 Player profiles with statistics
- 🏆 Leaderboard with top 10 players
- 💳 Convert NULL to check codes for @utxa_bot
- 📜 Game history tracking
- 🎚️ Three difficulty levels: Easy, Medium, Hard

## 💰 Reward System

Questions are sent every 5 minutes to active group chats:

| Time | Reward |
|------|--------|
| 🚀 < 30 seconds | +0.3 NULL |
| ⚡ 30 seconds - 1 minute | +0.2 NULL |
| ✅ 1 - 5 minutes | +0.05 NULL |

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nurikbashy/naello.git
   cd naello
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```

4. **Configure `.env` file**
   ```env
   BOT_TOKEN=your_bot_token_here
   DATABASE_PATH=game.db
   QUIZ_INTERVAL=300
   UTXA_BOT_NAME=@utxa_bot
   ```

   Get your bot token from [@BotFather](https://t.me/botfather)

5. **Run the bot**
   ```bash
   python main.py
   ```

## 📝 Usage

### In Group Chats

1. **Add bot to group** - `/start`
2. **Get a question** - `/quiz` (or wait 5 minutes)
3. **Answer** - Just type the number
4. **Earn** - NULL tokens based on speed

### In Private Chat

| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/profile` | View your stats and balance |
| `/history` | See your recent 10 games |
| `/leaderboard` | Top 10 players |
| `/buy_check <amount>` | Convert NULL to check |
| `/help` | Show help message |

### Buying Checks

1. Use `/buy_check 2` to get a code for 1 check (2 NULL)
2. Go to [@utxa_bot](https://t.me/utxa_bot)
3. Send `/redeem <code>`
4. Receive 1 check (1,000,000,000,000,000 coins)

## 🗄️ Database Schema

### Users Table
- `user_id`: Telegram user ID
- `username`: Telegram username
- `first_name`: User's first name
- `balance`: Current NULL balance
- `total_correct`: Number of correct answers
- `total_attempts`: Total quiz attempts

### Game History
- Tracks every quiz attempt
- Records time taken and reward earned
- Stores difficulty level

### Check Codes
- Stores generated check codes
- Tracks redemption status
- Links NULL amount to codes

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Reward amounts
REWARD_FAST = 0.3      # < 30 seconds
REWARD_MEDIUM = 0.2    # 30s - 1min
REWARD_SLOW = 0.05     # 1-5 minutes

# Time thresholds
TIME_FAST = 30         # 30 seconds
TIME_MEDIUM = 60       # 1 minute
TIME_SLOW = 300        # 5 minutes

# Quiz interval
QUIZ_INTERVAL = 300    # 5 minutes in seconds

# NULL conversion
NULL_PER_CHECK = 2     # 2 NULL = 1 check
```

## 📋 Question Difficulties

### Easy 🟢
- Numbers: 1-100
- Basic arithmetic

### Medium 🟡
- Numbers: 1-1000
- Intermediate calculations

### Hard 🔴
- Numbers: 1-10000
- Complex calculations

## 🐳 Docker Support

Build and run with Docker:

```bash
docker-compose up --build
```

## 📊 Example Commands

**In Group:**
```
/start      - Show welcome message
/quiz       - Send next question immediately
/stop       - Stop the game
```

**In Private:**
```
/profile       - View stats
/buy_check 4   - Buy 2 checks (4 NULL)
/leaderboard   - Top players
```

## 🔗 Integration with @utxa_bot

1. Earn NULL in Naello
2. Generate check codes using `/buy_check`
3. Redeem in @utxa_bot with `/redeem <code>`
4. Receive checks worth 1,000,000,000,000,000 coins each

## 📈 Statistics

Your profile shows:
- 💰 Current NULL balance
- ✅ Total correct answers
- 📊 Answer accuracy percentage
- 📜 Full game history

## 🎯 Tips for Earning More

1. **Answer faster** - Get more NULL per question
2. **Play regularly** - Questions every 5 minutes
3. **Master harder difficulties** - Same rewards, harder questions
4. **Check leaderboard** - Compete with others

## 🐛 Troubleshooting

**Bot not responding:**
- Check bot token in `.env`
- Ensure bot is added to groups
- Check internet connection

**Database errors:**
- Delete `game.db` and restart
- Check write permissions in directory

**No questions appearing:**
- Make sure chat is enabled with `/start`
- Check `QUIZ_INTERVAL` setting
- Bot needs to be active thread

## 📝 File Structure

```
naello/
├── main.py           # Main bot logic
├── config.py         # Configuration
├── database.py       # Database operations
├── questions.py      # Quiz generator
├── utils.py          # Helper functions
├── requirements.txt  # Dependencies
├── .env.example      # Environment template
├── game.db          # SQLite database (auto-created)
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## 📄 License

MIT License - feel free to modify and distribute

## 🙏 Support

- Report issues on GitHub
- Contact [@support](https://t.me/support)
- Check `/help` in bot

## 🚀 Future Updates

- [ ] Multiplayer mode
- [ ] Custom question sets
- [ ] Achievements & badges
- [ ] Seasonal tournaments
- [ ] Mobile app

---

**Happy learning and earning!** 🎓💰