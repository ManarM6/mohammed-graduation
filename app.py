from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'mohammed-graduation-2025-super-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///messages.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_name = db.Column(db.String(100), nullable=False)
    message_text = db.Column(db.Text, nullable=False)
    relation = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/letters')
def letters():
    messages_raw = Message.query.order_by(Message.created_at).all()
    messages = [
        {
            'id': m.id,
            'sender_name': m.sender_name,
            'message_text': m.message_text,
            'relation': m.relation or ''
        }
        for m in messages_raw
    ]
    return render_template('letters.html', messages=messages)

@app.route('/finale')
def finale():
    return render_template('finale.html')

@app.route('/admin')
def admin():
    password = request.args.get('pw', '')
    if not password:
        return '<form action="/admin" method="get"><input name="pw" type="password" placeholder="الباسورد"><button>دخول</button></form>'
    if password != os.environ.get('ADMIN_PASSWORD', 'admin123'):
        return '<p>كلمة مرور خاطئة</p>'
    messages = Message.query.order_by(Message.created_at.desc()).all()
    rows = ''.join([f'<tr><td>{m.id}</td><td>{m.sender_name}</td><td>{m.message_text[:50]}</td><td><a href="/admin/delete/{m.id}?pw={password}">حذف</a></td></tr>' for m in messages])
    return f'<table border="1">{rows}</table><br><a href="/admin/delete-all?pw={password}">حذف الكل</a>'

@app.route('/admin/delete/<int:id>')
def delete_message(id):
    password = request.args.get('pw', '')
    if password != os.environ.get('ADMIN_PASSWORD', 'admin123'):
        return 'غير مصرح'
    Message.query.filter_by(id=id).delete()
    db.session.commit()
    return f'<meta http-equiv="refresh" content="0;url=/admin?pw={password}">'

@app.route('/admin/delete-all')
def delete_all():
    password = request.args.get('pw', '')
    if password != os.environ.get('ADMIN_PASSWORD', 'admin123'):
        return 'غير مصرح'
    Message.query.delete()
    db.session.commit()
    return f'<meta http-equiv="refresh" content="0;url=/admin?pw={password}">'
@app.route('/write')
def write():
    return render_template('write.html')

@app.route('/api/submit-message', methods=['POST'])
def submit_message():
    data = request.get_json()
    name = data.get('name', '').strip()
    text = data.get('message', '').strip()
    relation = data.get('relation', '').strip()
    if not name or not text:
        return jsonify({'success': False, 'error': 'الاسم والرسالة مطلوبين'})
    if len(text) > 1000:
        return jsonify({'success': False, 'error': 'الرسالة طويلة جداً'})
    msg = Message(sender_name=name, message_text=text, relation=relation)
    db.session.add(msg)
    db.session.commit()
    return jsonify({'success': True})

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
