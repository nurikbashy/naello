from datetime import datetime
from config import (
    REWARD_FAST, REWARD_MEDIUM, REWARD_SLOW,
    TIME_FAST, TIME_MEDIUM, TIME_SLOW,
    NULL_PER_CHECK
)

def calculate_reward(time_taken):
    """Calculate NULL reward based on time taken"""
    if time_taken <= TIME_FAST:
        return REWARD_FAST
    elif time_taken <= TIME_MEDIUM:
        return REWARD_MEDIUM
    elif time_taken <= TIME_SLOW:
        return REWARD_SLOW
    return 0

def get_reward_tier(time_taken):
    """Get reward tier name based on time taken"""
    if time_taken <= TIME_FAST:
        return f"🚀 Super Fast ({REWARD_FAST} NULL)"
    elif time_taken <= TIME_MEDIUM:
        return f"⚡ Fast ({REWARD_MEDIUM} NULL)"
    elif time_taken <= TIME_SLOW:
        return f"✅ Normal ({REWARD_SLOW} NULL)"
    return "❌ Too Late (0 NULL)"

def format_time(seconds):
    """Format seconds to readable time"""
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        return f"{seconds / 60:.1f}m"
    else:
        return f"{seconds / 3600:.1f}h"

def format_profile_text(stats):
    """Format user profile statistics"""
    if not stats:
        return "❌ No data found"
    
    text = f"""
📊 **Your Profile**

💰 Balance: `{stats['balance']:.2f} NULL`
✅ Correct answers: `{stats['correct']}/{stats['attempts']}`
📈 Accuracy: `{stats['accuracy']:.1f}%`

💡 **How to earn NULL:**
🚀 Answer in < 30s: +0.3 NULL
⚡ Answer in 30s-1m: +0.2 NULL
✅ Answer in 1-5m: +0.05 NULL

💳 **Buy check:**
Use `/buy_check <amount>` to convert NULL to check
`2 NULL = 1 Check (1,000,000,000,000,000 coins)`
Then use the code in @utxa_bot
"""
    return text.strip()

def format_leaderboard_text(leaderboard):
    """Format leaderboard text"""
    if not leaderboard:
        return "📊 No players yet"
    
    text = "🏆 **Top Players**\n\n"
    medals = ['🥇', '🥈', '🥉']
    
    for entry in leaderboard:
        medal = medals[entry['position'] - 1] if entry['position'] <= 3 else f"{entry['position']}."
        username = f"@{entry['username']}" if entry['username'] else entry['first_name']
        text += f"{medal} {username}\n"
        text += f"   💰 {entry['balance']:.2f} NULL | 📊 {entry['accuracy']:.0f}%\n"
    
    return text

def format_history_text(history):
    """Format game history text"""
    if not history:
        return "📜 No history yet"
    
    text = "📜 **Your Recent Games**\n\n"
    
    for i, game in enumerate(history, 1):
        status = "✅" if game['is_correct'] else "❌"
        difficulty_emoji = "🟢" if game['difficulty'] == 'easy' else "🟡" if game['difficulty'] == 'medium' else "🔴"
        
        text += f"{i}. {status} {game['question']}\n"
        text += f"   Your answer: `{game['user_answer']}` | Correct: `{game['correct_answer']}`\n"
        text += f"   {difficulty_emoji} {game['difficulty'].title()} | ⏱️ {format_time(game['time_taken'])} | 💰 {game['reward']} NULL\n\n"
    
    return text.strip()

def validate_null_amount(amount_str):
    """Validate NULL amount for check purchase"""
    try:
        amount = float(amount_str)
        if amount <= 0:
            return None, "Amount must be positive"
        if amount % NULL_PER_CHECK != 0:
            return None, f"Amount must be multiple of {NULL_PER_CHECK} NULL"
        return amount, None
    except ValueError:
        return None, "Invalid amount"

def get_check_amount(null_amount):
    """Calculate number of checks from NULL amount"""
    return int(null_amount / NULL_PER_CHECK)

def format_check_message(code, null_amount):
    """Format check code message"""
    check_amount = get_check_amount(null_amount)
    text = f"""
✅ **Check Generated**

💳 Check Code: `{code}`
💰 Amount: `{null_amount} NULL` = `{check_amount} Check(s)`

📝 **Instructions:**
1. Open @utxa_bot
2. Send: `/redeem {code}`
3. You'll receive {check_amount} check(s)

⚠️ Code valid for 24 hours
"""
    return text.strip()

def is_private_chat(message):
    """Check if message is from private chat"""
    return message.chat.type == 'private'

def is_group_chat(message):
    """Check if message is from group chat"""
    return message.chat.type in ['group', 'supergroup']

def get_user_display_name(user):
    """Get formatted user name"""
    if user.username:
        return f"@{user.username}"
    return f"{user.first_name} {user.last_name or ''}".strip()