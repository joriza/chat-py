from flask import Flask, request, render_template_string

app = Flask(__name__)

messages = []

# Plantilla para VER mensajes (con auto-refresh)
VIEW_TEMPLATE = """<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile Profile 1.0//EN" "http://www.wapforum.org/DTD/xhtml-mobile10.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>MiniChat - Ver</title>
    <meta http-equiv="refresh" content="15" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
</head>
<body style="font-family:sans-serif;background-color:#eee;padding:0;margin:0;font-size:12px;">
    <div style="{{ container_style }};margin:0 auto;background-color:#fff;border-left:1px solid #ccc;border-right:1px solid #ccc;">
        
        <div style="background-color:#333;color:#fff;padding:8px;text-align:center;">
            <strong style="font-size:14px;">MiniChat</strong><br/>
            <span style="font-size:9px;color:#ccc;">{{ ua_info }}</span>
        </div>
        
        <div style="padding:10px;text-align:center;border-bottom:1px solid #ddd;">
             <a href="/compose" style="background-color:#007bff;color:#fff;padding:5px 15px;text-decoration:none;font-weight:bold;border-radius:3px;display:inline-block;">+ ESCRIBIR</a>
        </div>

        <div style="padding:5px;">
            <ul style="list-style-type:none;padding:0;margin:0;">
                {% if not messages %}
                    <li style="color:#999;text-align:center;padding:20px;">Sin mensajes.</li>
                {% endif %}
                {% for msg in messages %}
                    <li style="border-bottom:1px solid #eee;padding:6px 0;word-wrap:break-word;">
                        <span style="color:#888;font-size:9px;">[{{ msg.time }}]</span>
                        <span style="color:#666;font-weight:bold;">&raquo;</span> {{ msg.text }}
                    </li>
                {% endfor %}
            </ul>   
        </div>
        
        <div style="font-size:10px;color:#999;text-align:center;padding:10px;border-top:1px solid #ddd;">
            Actualizando cada 15s... | Historial: 10
        </div>
    </div>
</body>
</html>
"""

# Plantilla para ESCRIBIR (sin auto-refresh)
COMPOSE_TEMPLATE = """<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile Profile 1.0//EN" "http://www.wapforum.org/DTD/xhtml-mobile10.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>MiniChat - Escribir</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
</head>
<body style="font-family:sans-serif;background-color:#eee;padding:0;margin:0;font-size:12px;">
    <div style="{{ container_style }};margin:0 auto;background-color:#fff;border-left:1px solid #ccc;border-right:1px solid #ccc;min-height:150px;">
        <div style="background-color:#333;color:#fff;padding:8px;text-align:center;">
            <strong style="font-size:14px;">Nuevo Mensaje</strong>
        </div>

        <form method="POST" action="/compose" style="margin:20px 10px;text-align:center;">
            <input name="msg" type="text" style="width:90%;font-size:16px;border:1px solid #999;padding:5px;" maxlength="100" />
            <div style="margin-top:15px;">
                <input type="submit" value="ENVIAR" style="font-size:14px;padding:8px 20px;background-color:#28a745;color:#fff;border:none;font-weight:bold;" />
                <br/><br/>
                <a href="/" style="color:#666;font-size:12px;">Cancelar y volver</a>
            </div>
        </form>
    </div>
</body>
</html>
"""

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
    return render_template_string(VIEW_TEMPLATE, 
                                 messages=messages, 
                                 container_style=container_style, 
                                 ua_info=ua_info)

@app.route('/compose', methods=['GET', 'POST'])
def compose():
    if request.method == 'POST':
        msg = request.form.get('msg', '').strip()
        if msg:
            from datetime import datetime
            now = datetime.now().strftime('%H:%M')
            messages.insert(0, {'text': msg, 'time': now})
            while len(messages) > 10:
                messages.pop()
        from flask import redirect
        return redirect('/')
    
    ua = request.headers.get('User-Agent', '')
    container_style, _ = get_device_info(ua)
    return render_template_string(COMPOSE_TEMPLATE, container_style=container_style)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
