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

with app.app_context():
    db.create_all()
    if Message.query.count() == 0:
        samples = [
            Message(sender_name="أمك", message_text="محمد يا قلبي، من أول ما شفتك طفل صغير وأنا أحلم بهذا اليوم. تخرجك أسعد أيامي. فخورة فيك كل ثانية. ربي يحقق لك كل أحلامك ويسعدك دائماً 💛", relation="أم"),
            Message(sender_name="أبوك", message_text="ابني محمد، التخرج مجرد بداية لمسيرة عظيمة. عرفتك من صغرك إنسان طموح وإنسان أصيل. أفتخر فيك أمام الكل. وفقك الله وسدد خطاك.", relation="أب"),
            Message(sender_name="أخوك", message_text="أخوي محمد! ما تعرف كم أنا فخور فيك. شفتك تتعب وتسهر وتحاول، واليوم جاء ثمر تعبك. مبروك من كل قلبي 🤝", relation="أخ"),
        ]
        for s in samples:
            db.session.add(s)
        db.session.commit()

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

if __name__ == '__main__':
    app.run(debug=True)
