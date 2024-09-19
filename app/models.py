from app import db
from datetime import datetime
from app.ai_engine import ai_tutor  # Import ai_tutor to access lessons

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    progress = db.Column(db.Integer, default=0)
    current_lesson = db.Column(db.String(100), default='Introduction to Python')
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    completed_lessons = db.Column(db.Text, default='')

    def __repr__(self):
        return f'<User {self.username}>'

    def update_progress(self):
        self.progress = min(self.progress + 1, len(ai_tutor.lessons) - 1)
        self.current_lesson = ai_tutor.get_next_lesson(self.progress)
        self.last_activity = datetime.utcnow()
        if self.completed_lessons:
            self.completed_lessons += f',{self.current_lesson}'
        else:
            self.completed_lessons = self.current_lesson

    def get_completed_lessons(self):
        return self.completed_lessons.split(',') if self.completed_lessons else []
