import sqlite3
import json
from datetime import datetime
from config import DATABASE_PATH

def init_db():
    """Initialize database with required tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            balance REAL DEFAULT 0,
            total_correct INTEGER DEFAULT 0,
            total_attempts INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Game history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            chat_id INTEGER,
            question TEXT,
            user_answer TEXT,
            correct_answer TEXT,
            is_correct BOOLEAN,
            time_taken REAL,
            reward REAL,
            difficulty TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Check codes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS check_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            code TEXT UNIQUE,
            null_amount REAL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            redeemed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Active questions in chats
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS active_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER UNIQUE,
            question TEXT,
            correct_answer TEXT,
            difficulty TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            answered_by TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def add_or_update_user(user_id, username=None, first_name=None, last_name=None):
    """Add or update user in database"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
        VALUES (?, ?, ?, ?)
    ''', (user_id, username, first_name, last_name))
    
    if username or first_name or last_name:
        cursor.execute('''
            UPDATE users 
            SET username = COALESCE(?, username),
                first_name = COALESCE(?, first_name),
                last_name = COALESCE(?, last_name),
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (username, first_name, last_name, user_id))
    
    conn.commit()
    conn.close()

def get_user_balance(user_id):
    """Get user's NULL balance"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else 0

def update_user_balance(user_id, amount):
    """Update user's NULL balance"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE users 
        SET balance = balance + ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
    ''', (amount, user_id))
    
    conn.commit()
    conn.close()

def add_game_record(user_id, chat_id, question, user_answer, correct_answer, is_correct, time_taken, reward, difficulty):
    """Record game attempt"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO game_history (user_id, chat_id, question, user_answer, correct_answer, is_correct, time_taken, reward, difficulty)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, chat_id, question, user_answer, correct_answer, is_correct, time_taken, reward, difficulty))
    
    # Update user stats
    cursor.execute('''
        UPDATE users 
        SET total_attempts = total_attempts + 1,
            total_correct = total_correct + ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
    ''', (1 if is_correct else 0, user_id))
    
    conn.commit()
    conn.close()

def get_user_stats(user_id):
    """Get user's game statistics"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT balance, total_correct, total_attempts
        FROM users 
        WHERE user_id = ?
    ''', (user_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        balance, correct, attempts = result
        accuracy = (correct / attempts * 100) if attempts > 0 else 0
        return {
            'balance': balance,
            'correct': correct,
            'attempts': attempts,
            'accuracy': accuracy
        }
    return None

def create_check_code(user_id, null_amount):
    """Create check code for NULL withdrawal"""
    import random
    import string
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Generate unique code
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    
    cursor.execute('''
        INSERT INTO check_codes (user_id, code, null_amount)
        VALUES (?, ?, ?)
    ''', (user_id, code, null_amount))
    
    conn.commit()
    conn.close()
    
    return code

def get_check_code_status(code):
    """Get check code status"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT user_id, null_amount, status, created_at, redeemed_at
        FROM check_codes 
        WHERE code = ?
    ''', (code,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            'user_id': result[0],
            'null_amount': result[1],
            'status': result[2],
            'created_at': result[3],
            'redeemed_at': result[4]
        }
    return None

def set_active_question(chat_id, question, correct_answer, difficulty):
    """Set active question in chat"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO active_questions (chat_id, question, correct_answer, difficulty)
        VALUES (?, ?, ?, ?)
    ''', (chat_id, question, correct_answer, difficulty))
    
    conn.commit()
    conn.close()

def get_active_question(chat_id):
    """Get active question in chat"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT question, correct_answer, difficulty, created_at
        FROM active_questions 
        WHERE chat_id = ?
    ''', (chat_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            'question': result[0],
            'correct_answer': str(result[1]),
            'difficulty': result[2],
            'created_at': datetime.fromisoformat(result[3])
        }
    return None

def get_user_history(user_id, limit=10):
    """Get user's game history"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT question, user_answer, correct_answer, is_correct, time_taken, reward, difficulty, created_at
        FROM game_history 
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    ''', (user_id, limit))
    
    results = cursor.fetchall()
    conn.close()
    
    history = []
    for row in results:
        history.append({
            'question': row[0],
            'user_answer': row[1],
            'correct_answer': row[2],
            'is_correct': bool(row[3]),
            'time_taken': row[4],
            'reward': row[5],
            'difficulty': row[6],
            'created_at': row[7]
        })
    
    return history

def get_leaderboard(limit=10):
    """Get top players by balance"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT user_id, username, first_name, balance, total_correct, total_attempts
        FROM users 
        ORDER BY balance DESC
        LIMIT ?
    ''', (limit,))
    
    results = cursor.fetchall()
    conn.close()
    
    leaderboard = []
    for i, row in enumerate(results, 1):
        accuracy = (row[4] / row[5] * 100) if row[5] > 0 else 0
        leaderboard.append({
            'position': i,
            'user_id': row[0],
            'username': row[1],
            'first_name': row[2],
            'balance': row[3],
            'correct': row[4],
            'attempts': row[5],
            'accuracy': accuracy
        })
    
    return leaderboard