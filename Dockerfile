# Imagen oficial de Playwright: ya trae Python + los 3 navegadores + todas
# las librerías del SO preinstaladas. El tag DEBE coincidir con la versión
# exacta del paquete playwright (fijada en requirements.txt) — si no
# coinciden, los navegadores de la imagen no son compatibles con la
# librería y falla al lanzar (Playwright lo detecta y te lo dice en el
# error, con la versión exacta de imagen que necesitas).
FROM mcr.microsoft.com/playwright/python:v1.62.0-noble

WORKDIR /app

# Se copia SOLO requirements.txt primero, y se instala, antes de copiar el
# resto del código. Docker cachea cada instrucción como una capa: si luego
# solo cambias un test (no requirements.txt), este paso de `pip install`
# reutiliza la capa cacheada en vez de reinstalar todo de nuevo — mucho más
# rápido en rebuilds sucesivos.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Comando por defecto si no se especifica otro al hacer `docker run`.
# Se puede sobreescribir para correr solo una suite (ver README).
CMD ["pytest", "-v"]
