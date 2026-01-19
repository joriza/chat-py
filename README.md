# MiniChat POC

Aplicación de chat simple para pruebas internas con manejo mínimo de usuarios.

## Instalación

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

### Desarrollo (con debug)
```bash
python app.py
```
Accede a http://localhost:5000

### Producción (recomendado para POC)
```bash
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

## Características
- Mensajes en memoria (se pierden al reiniciar).
- Detección de dispositivo para ancho responsive.
- Campo usuario opcional.
- Protección CSRF básica.
- Historial limitado a 10 mensajes.

## Notas para POC
- Cambia `SECRET_KEY` en `app.py` antes de usar en entornos reales.
- No apto para producción sin persistencia y seguridad adicional.
