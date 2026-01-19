from flask import Flask, request, render_template, redirect, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
import threading
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'poc-secret-key-change-in-prod'  # Cambiar en producción

DB_FILE = 'chat.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
                 id INTEGER PRIMARY KEY,
                 user TEXT NOT NULL,
                 text TEXT NOT NULL,
                 time TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def load_messages():
    if not os.path.exists(DB_FILE):
        init_db()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT user, text, time FROM messages ORDER BY id DESC LIMIT 10')
    rows = c.fetchall()
    conn.close()
    return [{'user': row[0], 'text': row[1], 'time': row[2]} for row in rows]

def save_message(user, text, time_str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO messages (user, text, time) VALUES (?, ?, ?)', (user, text, time_str))
    conn.commit()
    conn.close()

messages = load_messages()
messages_lock = threading.Lock()

class LoginForm(FlaskForm):
    user = StringField('Nombre', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('ENTRAR')

class ComposeForm(FlaskForm):
    msg = TextAreaField('Mensaje', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('ENVIAR')



def get_device_info(ua):
    modern_os = ['android', 'iphone', 'ipad', 'windows nt', 'macintosh', 'linux']
    is_modern = any(os in ua.lower() for os in modern_os)
    if is_modern:
        container_style = "width:100%;max-width:600px"
        ua_label = "Modo: Extendido"
    else:
        container_style = "width:240px"
        ua_label = "Modo: Compacto"
    ua_info = f"{ua_label} ({ua[:15]}...)" if ua else "Dispositivo Genérico"
    return container_style, ua_info

@app.route('/')
def index():
    ua = request.headers.get('User-Agent', '')
    container_style, ua_info = get_device_info(ua)
    return render_template('view.html', 
                                 messages=messages, 
                                 container_style=container_style, 
                                 ua_info=ua_info)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['user'] = form.user.data.strip()
        return redirect('/compose')
    ua = request.headers.get('User-Agent', '')
    container_style, _ = get_device_info(ua)
    return render_template('login.html', form=form, container_style=container_style)

@app.route('/compose', methods=['GET', 'POST'])
def compose():
    if 'user' not in session:
        return redirect('/login')
    form = ComposeForm()
    if form.validate_on_submit():
        msg = form.msg.data.strip()
        user = session['user']
        if msg:
            from datetime import datetime
            now = datetime.now().strftime('%H:%M')
            with messages_lock:
                messages.insert(0, {'text': msg, 'time': now, 'user': user})
                while len(messages) > 10:
                    messages.pop()
            save_message(user, msg, now)
        return redirect('/')
    
    ua = request.headers.get('User-Agent', '')
    container_style, _ = get_device_info(ua)
    return render_template('compose.html', form=form, container_style=container_style)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
