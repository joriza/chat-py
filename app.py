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
    <div style="{{ width }};margin:0 auto;">
        <div style="background-color:#333;color:#fff;padding:5px;text-align:center;">
            <strong style="font-size:14px;">MiniChat [{{ ua_info }}]</strong>
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
    </div>
</body>
</html>
"""



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.form.get('msg', '').strip()
        if msg:
            messages.insert(0, msg)
            while len(messages) > 10:
                messages.pop()
    
    # Detección simple de dispositivo basada en User-Agent
    ua = request.headers.get('User-Agent', '')
    
    # Identificadores comunes de feature phones o navegadores antiguos
    # Si no se puede determinar o es sospechoso, asumimos feature phone
    is_feature_phone = True
    
    # Si contiene identificadores modernos, lo tratamos como moderno
    modern_indicators = ['Mozilla/5.0', 'Chrome/', 'Safari/', 'Firefox/', 'Edge/']
    if any(ind in ua for ind in modern_indicators):
        # Incluso siendo Mozilla/5.0, algunos moviles antiguos lo usan. 
        # Pero para este ejercicio, si es Mozilla/5.0 asumimos que puede ser moderno
        is_feature_phone = False
        
    # Ancho dinámico
    width = "240px" if is_feature_phone else "max-width:600px; width:100%;"
    
    # Fragmento del UA para la cabecera (primeros 15 caracteres o algo relevante)
    ua_info = ua[:20] + "..." if len(ua) > 20 else ua
    if not ua:
        ua_info = "Desconocido"

    return render_template_string(HTML_TEMPLATE, messages=messages, width=width, ua_info=ua_info)

if __name__ == '__main__':
    # host='0.0.0.0' permite el acceso desde otros dispositivos en la red local
    app.run(debug=True, host='0.0.0.0', port=5000)


