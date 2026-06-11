#!/usr/bin/env python3
"""
Naello - Mathematical Quiz Bot for Telegram
Earn NULL tokens by answering math questions correctly!
"""

import telebot
import threading
import time
from datetime import datetime, timedelta
from collections import defaultdict

from config import (
    BOT_TOKEN, QUIZ_INTERVAL, NULL_PER_CHECK, UTXA_BOT_NAME,
    REWARD_FAST, REWARD_MEDIUM, REWARD_SLOW,
    TIME_FAST, TIME_MEDIUM, TIME_SLOW
)
from database import (
    init_db, add_or_update_user, get_user_balance, update_user_balance,
    add_game_record, get_user_stats, create_check_code, get_check_code_status,
    set_active_question, get_active_question, get_user_history, get_leaderboard
)
from questions import QuizGenerator
from utils import (
    calculate_reward, get_reward_tier, format_profile_text, format_leaderboard_text,
    format_history_text, validate_null_amount, get_check_amount, format_check_message,
    is_private_chat, is_group_chat, get_user_display_name
)

# Initialize bot and database
bot = telebot.TeleBot(BOT_TOKEN)
init_db()

# Store active chats and question timers
active_chats = set()
question_timers = {}
question_times = {}  # Store when question was asked

# Markup helpers
def get_start_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add('📊 Profile', '💳 Buy Check')
    markup.add('📜 History', '🏆 Leaderboard')
    markup.add('❓ Help')
    return markup

# ===================== GROUP COMMANDS =====================

@bot.message_handler(commands=['start', 'help'], func=is_group_chat)
def start_group(message):
    """Start game in group"""
    chat_id = message.chat.id
    
    if chat_id in active_chats:
        bot.reply_to(message, "🎮 Game already active in this chat!\n\nQuestions come every 5 minutes.", 
                     parse_mode='Markdown')
        return
    
    text = """
🎮 **Naello Quiz Bot**

Answer math questions and earn NULL tokens!

⏰ Questions every 5 minutes
💰 Earn NULL based on speed:
   🚀 < 30s: +0.3 NULL
   ⚡ 30s-1m: +0.2 NULL
   ✅ 1-5m: +0.05 NULL

Just type your answer as a number to respond!
Open PM for profile, stats, and check purchasing.

/quiz - Send next question now
/stop - Stop the game
"""
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['quiz'], func=is_group_chat)
def send_quiz(message):
    """Send quiz question to group"""
    chat_id = message.chat.id
    
    if chat_id not in active_chats:
        active_chats.add(chat_id)
    
    send_question_to_group(chat_id)
    bot.send_message(chat_id, "✅ Question sent! You have up to 5 minutes to answer.")

@bot.message_handler(commands=['stop'], func=is_group_chat)
def stop_game(message):
    """Stop game in group"""
    chat_id = message.chat.id
    
    if chat_id in active_chats:
        active_chats.discard(chat_id)
        if chat_id in question_timers:
            question_timers[chat_id].cancel()
            del question_timers[chat_id]
        bot.reply_to(message, "⏹️ Game stopped in this chat.")
    else:
        bot.reply_to(message, "❌ No active game in this chat.")

# ===================== PRIVATE COMMANDS =====================

@bot.message_handler(commands=['start'], func=is_private_chat)
def start_private(message):
    """Start in private chat"""
    user = message.from_user
    add_or_update_user(user.id, user.username, user.first_name, user.last_name)
    
    text = """
🎮 **Welcome to Naello!**

Answer math questions in groups to earn NULL tokens.
Use this private chat for:
- 📊 Profile & Statistics
- 💳 Buy & redeem checks
- 📜 Game history
- 🏆 Leaderboard

Join a group and use /quiz to start!
"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown', 
                    reply_markup=get_start_markup())

@bot.message_handler(commands=['profile'], func=is_private_chat)
def show_profile(message):
    """Show user profile"""
    user_id = message.from_user.id
    stats = get_user_stats(user_id)
    
    text = format_profile_text(stats)
    bot.send_message(message.chat.id, text, parse_mode='Markdown',
                    reply_markup=get_start_markup())

@bot.message_handler(commands=['history'], func=is_private_chat)
def show_history(message):
    """Show game history"""
    user_id = message.from_user.id
    history = get_user_history(user_id, limit=10)
    
    text = format_history_text(history)
    bot.send_message(message.chat.id, text, parse_mode='Markdown',
                    reply_markup=get_start_markup())

@bot.message_handler(commands=['leaderboard'], func=is_private_chat)
def show_leaderboard(message):
    """Show top players"""
    leaderboard = get_leaderboard(limit=10)
    text = format_leaderboard_text(leaderboard)
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown',
                    reply_markup=get_start_markup())

@bot.message_handler(commands=['buy_check'], func=is_private_chat)
def buy_check_command(message):
    """Buy check command"""
    user_id = message.from_user.id
    balance = get_user_balance(user_id)
    
    text = f"""
💳 **Buy Check**

Current balance: `{balance:.2f} NULL`
Price: `2 NULL = 1 Check (1,000,000,000,000,000 coins)`

Usage: `/buy_check <amount>`

Example: `/buy_check 2` - Buy 1 check
Example: `/buy_check 4` - Buy 2 checks

Min amount: 2 NULL
"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['help'], func=is_private_chat)
def help_command(message):
    """Show help"""
    text = """
📖 **Naello Bot - Help**

🎮 **How to Play:**
1. Add bot to your group
2. Use /quiz to get a math question
3. Answer with the correct number
4. Earn NULL based on speed!

⏱️ **Reward System:**
🚀 Answer in < 30s: +0.3 NULL
⚡ Answer in 30s-1m: +0.2 NULL
✅ Answer in 1-5m: +0.05 NULL

📊 **Commands (in Private Chat):**
/profile - View your stats
/history - See your recent games
/leaderboard - Top 10 players
/buy_check - Convert NULL to checks

💳 **Withdrawing NULL:**
1. Use /buy_check to generate a code
2. Open @utxa_bot
3. Send /redeem <code>

⚠️ **Rules:**
- Only 1 answer per question per user
- Questions appear every 5 minutes
- Accuracy matters for leaderboard!

❓ Issues? Contact @support
"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

# ===================== TEXT MESSAGE HANDLERS =====================

@bot.message_handler(func=lambda m: m.text == '📊 Profile', content_types=['text'])
def button_profile(message):
    show_profile(message)

@bot.message_handler(func=lambda m: m.text == '💳 Buy Check', content_types=['text'])
def button_buy_check(message):
    buy_check_command(message)

@bot.message_handler(func=lambda m: m.text == '📜 History', content_types=['text'])
def button_history(message):
    show_history(message)

@bot.message_handler(func=lambda m: m.text == '🏆 Leaderboard', content_types=['text'])
def button_leaderboard(message):
    show_leaderboard(message)

@bot.message_handler(func=lambda m: m.text == '❓ Help', content_types=['text'])
def button_help(message):
    help_command(message)

# ===================== QUIZ ANSWER HANDLER =====================

@bot.message_handler(func=lambda m: is_group_chat(m) and m.text.isdigit(), content_types=['text'])
def handle_answer(message):
    """Handle quiz answer in group"""
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Check if there's an active question
    active_q = get_active_question(chat_id)
    if not active_q:
        return
    
    # Get time taken
    time_taken = (datetime.now() - active_q['created_at']).total_seconds()
    
    # Validate answer
    user_input = message.text.strip()
    is_correct, user_answer = QuizGenerator.validate_answer(user_input, active_q['correct_answer'])
    
    # Add user to database
    add_or_update_user(user_id, message.from_user.username, 
                      message.from_user.first_name, message.from_user.last_name)
    
    # Calculate reward
    reward = calculate_reward(time_taken) if is_correct else 0
    
    # Record game
    add_game_record(
        user_id, chat_id,
        active_q['question'],
        user_answer,
        active_q['correct_answer'],
        is_correct,
        time_taken,
        reward,
        active_q['difficulty']
    )
    
    # Update balance
    if is_correct:
        update_user_balance(user_id, reward)
    
    # Send response
    user_name = get_user_display_name(message.from_user)
    difficulty_emoji = QuizGenerator.get_difficulty_emoji(active_q['difficulty'])
    
    if is_correct:
        reward_tier = get_reward_tier(time_taken)
        response = f"""
✅ **Correct!**

User: {user_name}
Question: {active_q['question']}
Answer: `{user_answer}`
Time: ⏱️ {time_taken:.1f}s
Reward: {reward_tier}
{difficulty_emoji} {active_q['difficulty'].title()}
"""
    else:
        response = f"""
❌ **Incorrect**

User: {user_name}
Question: {active_q['question']}
Your answer: `{user_answer}`
Correct answer: `{active_q['correct_answer']}`
Time: ⏱️ {time_taken:.1f}s
{difficulty_emoji} {active_q['difficulty'].title()}
"""
    
    bot.send_message(chat_id, response, parse_mode='Markdown')

# ===================== BUY CHECK HANDLER =====================

@bot.message_handler(func=lambda m: is_private_chat(m) and m.text.startswith('/buy_check '))
def process_buy_check(message):
    """Process check purchase"""
    user_id = message.from_user.id
    
    try:
        amount_str = message.text.split('/buy_check ', 1)[1].strip()
        amount, error = validate_null_amount(amount_str)
        
        if error:
            bot.send_message(message.chat.id, f"❌ Error: {error}")
            return
        
        balance = get_user_balance(user_id)
        
        if balance < amount:
            bot.send_message(message.chat.id, 
                           f"❌ Insufficient balance!\n\nYou have: `{balance:.2f} NULL`\nNeeded: `{amount:.2f} NULL`",
                           parse_mode='Markdown')
            return
        
        # Create check code
        code = create_check_code(user_id, amount)
        
        # Deduct balance
        update_user_balance(user_id, -amount)
        
        # Send check message
        check_msg = format_check_message(code, amount)
        bot.send_message(message.chat.id, check_msg, parse_mode='Markdown')
        
    except IndexError:
        bot.send_message(message.chat.id, "Usage: `/buy_check <amount>`\nExample: `/buy_check 2`",
                        parse_mode='Markdown')

# ===================== QUIZ SENDER =====================

def send_question_to_group(chat_id):
    """Send math question to group"""
    try:
        quiz_data = QuizGenerator.generate_question()
        
        # Store question in database
        set_active_question(
            chat_id,
            quiz_data['question'],
            quiz_data['correct_answer'],
            quiz_data['difficulty']
        )
        
        # Store time
        question_times[chat_id] = datetime.now()
        
        # Create message
        difficulty_emoji = QuizGenerator.get_difficulty_emoji(quiz_data['difficulty'])
        message_text = f"""
{difficulty_emoji} **Math Quiz Question**

❓ What is: `{quiz_data['question']}?`

⏰ Time limit: 5 minutes
💰 Rewards based on speed:
  🚀 < 30s: +0.3 NULL
  ⚡ 30s-1m: +0.2 NULL
  ✅ 1-5m: +0.05 NULL

Just reply with the number!
"""
        
        sent = bot.send_message(chat_id, message_text, parse_mode='Markdown')
        
    except Exception as e:
        print(f"Error sending question to {chat_id}: {e}")

def quiz_scheduler():
    """Background task to send questions to active chats"""
    while True:
        time.sleep(QUIZ_INTERVAL)
        
        active_chats_copy = list(active_chats)
        for chat_id in active_chats_copy:
            send_question_to_group(chat_id)

# ===================== MAIN =====================

if __name__ == '__main__':
    print("🤖 Naello Bot is starting...")
    print(f"✅ Bot token loaded")
    print(f"✅ Database initialized")
    print(f"✅ Quiz interval: {QUIZ_INTERVAL} seconds")
    
    # Start quiz scheduler in background
    scheduler_thread = threading.Thread(target=quiz_scheduler, daemon=True)
    scheduler_thread.start()
    print("✅ Quiz scheduler started")
    
    print("🚀 Bot is running... Press Ctrl+C to stop")
    
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        print("\n⏹️ Bot stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Retrying in 10 seconds...")
        time.sleep(10)