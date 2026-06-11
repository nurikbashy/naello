import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', '8888106643:AAHpWqGBR8KnEeoMNiuI5iU54zuCK-Zk5FM')
DATABASE_PATH = os.getenv('DATABASE_PATH', 'game.db')
QUIZ_INTERVAL = int(os.getenv('QUIZ_INTERVAL', 300))  # 5 minutes in seconds
UTXA_BOT_NAME = os.getenv('UTXA_BOT_NAME', '@utxa_bot')

# NULL Token Configuration
NULL_PER_CHECK = 2  # 2 NULL = 1 check (1,000,000,000,000,000 coins in @utxa_bot)

# Reward Configuration (in NULL tokens)
REWARD_FAST = 0.3      # Less than 30 seconds
REWARD_MEDIUM = 0.2    # 30 seconds to 1 minute
REWARD_SLOW = 0.05     # 1 to 5 minutes

# Time Thresholds (in seconds)
TIME_FAST = 30         # 30 seconds
TIME_MEDIUM = 60       # 1 minute
TIME_SLOW = 300        # 5 minutes

# Database Constants
DB_VERSION = 1