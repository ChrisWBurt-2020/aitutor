import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class AITutor:
    def __init__(self):
        self.lessons = [
            "Introduction to Python",
            "Variables and Data Types",
            "Control Structures",
            "Functions",
            "Lists and Dictionaries",
            "Object-Oriented Programming",
            "File Handling",
            "Error Handling",
            "Modules and Packages",
            "Advanced Python Concepts"
        ]
        
        self.qa_pairs = {
            "What is Python?": "Python is a high-level, interpreted programming language known for its simplicity and readability.",
            "How do I declare a variable in Python?": "In Python, you can declare a variable by simply assigning a value to it. For example: x = 5",
            "What is a function in Python?": "A function in Python is a reusable block of code that performs a specific task. It is defined using the 'def' keyword.",
            "How do I create a list in Python?": "You can create a list in Python by enclosing comma-separated values in square brackets. For example: my_list = [1, 2, 3, 4]",
            "What is object-oriented programming?": "Object-oriented programming (OOP) is a programming paradigm based on the concept of 'objects', which can contain data and code."
        }
        self.vectorizer = TfidfVectorizer()
        self.vectorizer.fit(list(self.qa_pairs.keys()))

    def get_next_lesson(self, progress):
        progress = min(progress, len(self.lessons) - 1)
        return self.lessons[progress]

    # def update_progress(self, user_id):
    #     if user_id in self.user_progress:
    #         self.user_progress[user_id] = min(len(self.lessons) - 1, self.user_progress[user_id] + 1)

    def generate_practice_question(self, lesson):
        questions = {
            "Introduction to Python": "Write a Python script that prints 'Hello, World!'",
            "Variables and Data Types": "Create variables for an integer, float, and string. Print their types.",
            "Control Structures": "Write a for loop that prints the even numbers from 0 to 10.",
            "Functions": "Define a function that takes two parameters and returns their sum.",
            "Lists and Dictionaries": "Create a list of fruits and a dictionary of their colors. Print both.",
            "Object-Oriented Programming": "Define a simple class called 'Car' with attributes for make and model.",
            "File Handling": "Write a function that reads a text file and returns its content as a string.",
            "Error Handling": "Write a try-except block that handles a ZeroDivisionError.",
            "Modules and Packages": "Import the 'math' module and use its 'sqrt' function to calculate the square root of 16.",
            "Advanced Python Concepts": "Use a list comprehension to create a list of squares of even numbers from 0 to 10."
        }
        return questions.get(lesson, "Write a Python function related to the concept of " + lesson)

    def evaluate_code(self, code, lesson):
        try:
            # Basic syntax check
            compile(code, '<string>', 'exec')
            
            # Lesson-specific checks (simplified)
            if "Hello, World!" in code and lesson == "Introduction to Python":
                return "Great job! Your code correctly prints 'Hello, World!'."
            elif "def" in code and "return" in code and lesson == "Functions":
                return "Excellent work! You've defined a function with a return statement."
            elif "for" in code and "range" in code and lesson == "Control Structures":
                return "Good job! You've used a for loop with range()."
            elif "class" in code and lesson == "Object-Oriented Programming":
                return "Well done! You've defined a class, which is a key concept in OOP."
            else:
                return "Your code looks syntactically correct, but I can't fully evaluate its correctness for this lesson. Keep practicing!"
        except SyntaxError as e:
            return f"There's a syntax error in your code: {str(e)}"
        except Exception as e:
            return f"An error occurred while evaluating your code: {str(e)}"

    def answer_question(self, question):
        question_vector = self.vectorizer.transform([question])
        similarities = cosine_similarity(question_vector, self.vectorizer.transform(list(self.qa_pairs.keys())))
        most_similar_index = similarities.argmax()
        most_similar_question = list(self.qa_pairs.keys())[most_similar_index]
        
        if similarities[0][most_similar_index] > 0.5:  # Threshold for similarity
            return self.qa_pairs[most_similar_question]
        else:
            return "I'm sorry, I don't have enough information to answer that question accurately. Could you please rephrase or ask something related to Python basics?"

ai_tutor = AITutor()