from flask import Flask, request, render_template_string

app = Flask(__name__)

# Almacenamiento en memoria para los mensajes
messages = []

# Plantilla HTML compatible con XHTML Mobile Profile 1.0 / HTML 3.2
# Sin scripts, sin CSS externo, solo estilos en línea básicos.
HTML_TEMPLATE = """<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile Profile 1.0//EN" "http://www.wapforum.org/DTD/xhtml-mobile10.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>MiniChat</title>
    <meta http-equiv="refresh" content="15">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family:sans-serif;background-color:#eee;padding:2px;margin:0;font-size:12px;">
    <div style="background-color:#333;color:#fff;padding:5px;text-align:center;">
        <strong style="font-size:14px;">MiniChat</strong>
    </div>
    
    <div style="background-color:#fff;padding:3px;margin:2px;border:1px solid #ccc;">
        <ul style="list-style-type:none;padding:0;margin:0;">
            {% if not messages %}
                <li style="color:#999;text-align:center;">Sin mensajes.</li>
            {% endif %}
            {% for msg in messages %}
                <li style="border-bottom:1px solid #eee;padding:4px 0;word-wrap:break-word;">
                    <span style="color:#666;">&raquo;</span> {{ msg }}
                </li>
            {% endfor %}
        </ul>
    </div>

    <form method="POST" action="/" style="margin:5px 2px;text-align:center;">
        <input name="msg" type="text" style="width:70%;font-size:12px;" maxlength="100" />
        <input type="submit" value="Ok" style="font-size:12px;padding:2px 5px;" />
    </form>
    
    <div style="font-size:10px;color:#999;text-align:center;margin-top:5px;">
        Recarga: 15s | Límite: 10
    </div>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.form.get('msg', '').strip()
        if msg:
            # Añadir mensaje al inicio de la lista
            messages.insert(0, msg)
            # Limitar a los últimos 10 mensajes
            while len(messages) > 10:
                messages.pop()
    
    return render_template_string(HTML_TEMPLATE, messages=messages)

if __name__ == '__main__':
    # host='0.0.0.0' permite el acceso desde otros dispositivos en la red local
    app.run(debug=True, host='0.0.0.0', port=5000)

