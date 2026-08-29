# TaskFlow API

Base de la API TaskFlow: FastAPI administrado con `uv` en Python 3.12.

## Recorrido

```bash
# 1. Instalar dependencias exactas (usa uv.lock)
uv sync --locked

# 2. Ejecutar pruebas
uv run pytest -q

# 3. Analizar el código
uv run ruff check .

# 4. Levantar la base de datos
docker compose up -d

# 5. Ejecutar la API
uv run uvicorn app.main:app --reload

# 6. Al terminar, apagar la base de datos
docker compose down
```

`GET /health` responde `200` con `{"status": "ok"}`.

Copia `.env.example` a `.env` para personalizar las credenciales locales de
PostgreSQL; `docker compose` funciona también sin `.env`, usando los valores
por defecto definidos en `compose.yaml`.
