from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    priority = db.Column(db.String(20), default='Medium')
    is_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def create_app(config_name=None):
    app = Flask(__name__)
    
    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        # SPEC.md 5절: 최신 등록순 정렬
        todos = Todo.query.order_by(Todo.created_at.desc()).all()
        return render_template('index.html', todos=todos)

    @app.route('/add', methods=['POST'])
    def add_todo():
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority')
        due_date_str = request.form.get('due_date')
        
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        if title:
            new_todo = Todo(
                title=title,
                description=description,
                priority=priority,
                due_date=due_date
            )
            db.session.add(new_todo)
            db.session.commit()
        
        return redirect(url_for('index'))

    @app.route('/toggle/<int:todo_id>', methods=['POST'])
    def toggle_todo(todo_id):
        todo = Todo.query.get_or_404(todo_id)
        todo.is_completed = not todo.is_completed
        db.session.commit()
        return redirect(url_for('index'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
