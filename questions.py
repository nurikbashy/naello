import random

class QuizGenerator:
    """Generate mathematical quiz questions"""
    
    # Easy difficulty (numbers 1-100)
    EASY_MIN = 1
    EASY_MAX = 100
    
    # Medium difficulty (numbers 1-1000)
    MEDIUM_MIN = 1
    MEDIUM_MAX = 1000
    
    # Hard difficulty (numbers 1-10000)
    HARD_MIN = 1
    HARD_MAX = 10000
    
    OPERATORS = ['+', '-', '*', '/']
    DIFFICULTIES = ['easy', 'medium', 'hard']
    
    @staticmethod
    def generate_question():
        """Generate a random math question with appropriate difficulty"""
        difficulty = random.choice(QuizGenerator.DIFFICULTIES)
        
        if difficulty == 'easy':
            num_min = QuizGenerator.EASY_MIN
            num_max = QuizGenerator.EASY_MAX
        elif difficulty == 'medium':
            num_min = QuizGenerator.MEDIUM_MIN
            num_max = QuizGenerator.MEDIUM_MAX
        else:  # hard
            num_min = QuizGenerator.HARD_MIN
            num_max = QuizGenerator.HARD_MAX
        
        operator = random.choice(QuizGenerator.OPERATORS)
        
        # Generate valid numbers
        num1 = random.randint(num_min, num_max)
        num2 = random.randint(num_min, num_max)
        
        # Ensure division results in whole numbers only
        if operator == '/':
            num2 = random.randint(1, max(1, num_max // 10))  # Keep divisor smaller
            num1 = num2 * random.randint(1, num_max // num2)  # Make num1 divisible by num2
        
        # Ensure subtraction doesn't give negative results
        if operator == '-' and num1 < num2:
            num1, num2 = num2, num1
        
        question = f"{num1} {operator} {num2}"
        
        # Calculate correct answer
        if operator == '+':
            correct_answer = num1 + num2
        elif operator == '-':
            correct_answer = num1 - num2
        elif operator == '*':
            correct_answer = num1 * num2
        else:  # division
            correct_answer = int(num1 / num2)
        
        return {
            'question': question,
            'correct_answer': correct_answer,
            'difficulty': difficulty
        }
    
    @staticmethod
    def validate_answer(user_input, correct_answer):
        """Validate user's answer"""
        try:
            user_answer = int(user_input.strip())
            return user_answer == correct_answer, user_answer
        except ValueError:
            return False, None
    
    @staticmethod
    def get_difficulty_emoji(difficulty):
        """Get emoji for difficulty level"""
        emojis = {
            'easy': '🟢',
            'medium': '🟡',
            'hard': '🔴'
        }
        return emojis.get(difficulty, '❓')