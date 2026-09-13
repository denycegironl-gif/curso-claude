# Plan: Persistencia en PostgreSQL

Secuencia de incrementos para conectar TaskFlow a PostgreSQL, en la rama
`feature/persistencia`. Alcance limitado a las secciones Salud y Estados de
`docs/contrato-api.md`.

Fuera de alcance: proyectos, tareas, filtros, `due_at`, skills, hooks y CI.

Cada incremento se confirma solo y espera aprobación antes de encadenar el
siguiente.

## Incremento 1 — Config y conexión a PostgreSQL (sin endpoints nuevos)

Agregar SQLAlchemy async, `asyncpg` y `pydantic-settings`; módulo `app/db.py`
con configuración leída de variables de entorno y un engine/sesión async, sin
efectos al importar. `GET /health` no cambia.

**Comprobación**: `uv run ruff check .` limpio; `uv run pytest -q` en verde;
arranque manual con `docker compose up -d` + `uv run uvicorn app.main:app
--reload` sin errores de import/conexión.

**Estado**: completado. Dependencias agregadas, `app/db.py` creado, ruff y
pytest en verde, conexión real verificada contra el Postgres de
`compose.yaml`, `GET /health` intacto.

## Incremento 2 — Alembic inicializado, sin modelos de negocio todavía

Agregar Alembic como dependencia de dev, configurar `alembic.ini`/`env.py`
para leer la URL de conexión desde la misma fuente que la app, y generar la
migración inicial para validar `upgrade`/`downgrade` contra el Postgres del
`compose.yaml`.

**Comprobación**: `uv run alembic upgrade head` corre sin error contra base
vacía; `uv run alembic downgrade base` corre limpio; ruff y pytest en verde.

**Estado**: completado. Alembic agregado como dependencia de dev,
`migrations/env.py` lee la URL desde `app.db.get_settings()`, migración
inicial vacía generada; `upgrade`/`downgrade` verificados contra el Postgres
de `compose.yaml`, ruff y pytest en verde.

## Incremento 3 — Modelo y migración del catálogo de estados

Modelo/tabla `states` (`id`, `code`, campo de orden); migración que crea la
tabla y siembra `PENDIENTE`, `EN_CURSO`, `BLOQUEADA`, `HECHA` de forma
idempotente; `downgrade` que revierte limpio.

**Comprobación**: `upgrade` desde vacío puebla las 4 filas; correr `upgrade`
dos veces no duplica; `downgrade` elimina sin error.

**Estado**: completado. Modelo `State` (`id`, `code`, `sort_order`) y
migración que crea `states` y siembra el catálogo con
`ON CONFLICT DO NOTHING`; verificado que el seed no duplica y que
`downgrade` limpia la tabla sin error.

## Incremento 4 — `GET /states` contra la base real

Endpoint según contrato: `200` con lista ordenada por campo de orden y `id`
como desempate; esquema exacto `{"id": ..., "code": ...}`.

**Comprobación**: test nuevo que falla antes del incremento y pasa después;
`uv run pytest -q` completo en verde; ruff limpio.

**Estado**: completado. Endpoint implementado contra la base real, ordenado
por `sort_order` e `id` como desempate, esquema exacto `{"id", "code"}`; test
verificado en rojo antes y en verde después, pytest y ruff en verde.
