from flask import Flask, request, render_template_string

app = Flask(__name__)

messages = []

HTML_TEMPLATE = """<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile Profile 1.0//EN" "http://www.wapforum.org/DTD/xhtml-mobile10.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>MiniChat</title>
    <meta http-equiv="refresh" content="15" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
</head>
<body style="font-family:sans-serif;background-color:#eee;padding:0;margin:0;font-size:12px;">
    <div style="{{ container_style }};margin:0 auto;background-color:#fff;border-left:1px solid #ccc;border-right:1px solid #ccc;">
        
        <div style="background-color:#333;color:#fff;padding:8px;text-align:center;">
            <strong style="font-size:14px;">MiniChat</strong><br/>
            <span style="font-size:9px;color:#ccc;">{{ ua_info }}</span>
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

        <form method="POST" action="/" style="margin:10px 0;text-align:center;border-top:1px solid #ddd;padding-top:10px;">
            <input name="msg" type="text" style="width:65%;font-size:14px;border:1px solid #999;" maxlength="100" />
            <input type="submit" value="Enviar" style="font-size:14px;padding:2px 10px;background-color:#eee;" />
        </form>
        
        <div style="font-size:10px;color:#999;text-align:center;padding-bottom:10px;">
            Auto-refresh: 15s | Historial: 10
        </div>
    </div>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.form.get('msg', '').strip()
        if msg:
            from datetime import datetime
            now = datetime.now().strftime('%H:%M')
            messages.insert(0, {'text': msg, 'time': now})
            while len(messages) > 10:
                messages.pop()

    
    ua = request.headers.get('User-Agent', '')
    
    # Identificar dispositivos modernos (Android, iPhone, Desktop)
    # Si no encuentra estas marcas, se asume dispositivo limitado (240px)
    modern_os = ['android', 'iphone', 'ipad', 'windows nt', 'macintosh', 'linux']
    is_modern = any(os in ua.lower() for os in modern_os)
    
    if is_modern:
        # Para modernos: ancho completo pero con un límite de lectura cómodo (600px)
        container_style = "width:100%;max-width:600px"
        ua_label = "Modo: Extendido"
    else:
        # Para feature phones: ancho fijo para evitar errores de renderizado en microservers
        container_style = "width:240px"
        ua_label = "Modo: Compacto"
    
    # Info simplificada para el header
    ua_info = f"{ua_label} ({ua[:15]}...)" if ua else "Dispositivo Genérico"

    return render_template_string(HTML_TEMPLATE, 
                                 messages=messages, 
                                 container_style=container_style, 
                                 ua_info=ua_info)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
