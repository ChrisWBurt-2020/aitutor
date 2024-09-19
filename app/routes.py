from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from functools import wraps
from app import db
from app.models import User
from app.ai_engine import ai_tutor

from functools import wraps

main = Blueprint('main', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        session['user_id'] = user.id
        flash(f'Welcome, {username}!', 'success')
        return redirect(url_for('main.learn'))
    return render_template('login.html')

@main.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@main.route('/learn')
@login_required
def learn():
    user = User.query.get(session['user_id'])
    current_lesson = ai_tutor.get_next_lesson(user.progress)
    user.current_lesson = current_lesson
    db.session.commit()
    return render_template('learn.html', lesson=current_lesson, user=user)

@main.route('/practice')
@login_required
def practice():
    user = User.query.get(session['user_id'])
    current_lesson = ai_tutor.get_next_lesson(user.progress)
    practice_question = ai_tutor.generate_practice_question(current_lesson)
    return render_template('practice.html', question=practice_question, user=user)

@main.route('/submit_code', methods=['POST'])
@login_required
def submit_code():
    code = request.json['code']
    user = User.query.get(session['user_id'])
    current_lesson = ai_tutor.get_next_lesson(user.progress)
    feedback = ai_tutor.evaluate_code(code, current_lesson)
    if 'Great job' in feedback or 'Excellent work' in feedback:
        user.update_progress()
        db.session.commit()
    return jsonify({'feedback': feedback})


@main.route('/progress')
@login_required
def progress():
    user = User.query.get(session['user_id'])
    completed_lessons = user.get_completed_lessons()
    return render_template('progress.html', user=user, completed_lessons=completed_lessons)