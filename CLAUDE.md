# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Qué es esto

TaskFlow API: proyecto de curso que implementa progresivamente una API FastAPI para gestionar
proyectos y tareas, con PostgreSQL como base de datos. El estado actual del código es mínimo
(solo `GET /health` en `app/main.py`); el comportamiento objetivo completo está especificado en
`docs/contrato-api.md`, no en el código.

## Comandos

```bash
# Instalar dependencias exactas (usa uv.lock)
uv sync --locked

# Ejecutar pruebas
uv run pytest -q

# Ejecutar una sola prueba
uv run pytest tests/test_health.py::test_health_returns_ok

# Analizar el código (lint)
uv run ruff check .

# Base de datos (PostgreSQL vía Docker)
docker compose up -d
docker compose down

# Ejecutar la API en modo desarrollo
uv run uvicorn app.main:app --reload
```

No existe `.env` con secretos reales: `.env.example` trae valores de desarrollo local que también
son los defaults en `compose.yaml`, así que `docker compose` funciona sin `.env`.

## El contrato de la API es la fuente de verdad

`docs/contrato-api.md` es un documento normativo, no descriptivo: fija comportamiento observable
que los tests de la sesión 10 del curso verifican contra la implementación. Antes de construir o
modificar cualquier endpoint, leer ese documento — no inferir el comportamiento desde el código
existente, porque buena parte todavía no está implementada. Puntos que no son obvios y que rompen
implementaciones "razonables" pero incorrectas:

- **Normalización de `title`**: se recorta espacio en los extremos y se rechaza con `422` si no
  queda ningún carácter visible. `strip()` no basta — hay invisibles Unicode (p. ej. `U+200B`)
  que lo atraviesan; la comprobación es por categoría Unicode (`Cc`, `Cf`, `Zl`, `Zp`, `Zs`).
- **Orden estable de listas**: `GET /states` por campo de orden del catálogo con `id` como
  desempate; `GET /projects` y `GET /tasks` por `id` ascendente (también con filtros aplicados).
  Dos llamadas idénticas deben devolver los ids en la misma posición.
- **Catálogo de estados** (`PENDIENTE`, `EN_CURSO`, `BLOQUEADA`, `HECHA`): no tiene endpoints de
  creación/borrado. Se siembra vía migración (no vía script de init de Docker), porque la
  migración corre en cada `upgrade` en cualquier entorno y el script de Docker solo corre al crear
  el volumen — quien ya tenía el volumen nunca recibiría el catálogo. El seed debe ser
  [idempotente](docs/glosario.md#idempotente).
- **Borrado de proyecto con tareas**: `409`, nunca cascada implícita.
- **Referencias a recursos inexistentes** (proyecto o estado al crear una tarea): nunca se crean
  implícitamente.
- **`due_at` (tareas v2)**: opcional; se normaliza a UTC; una fecha sin zona horaria se rechaza
  con `422` (es ambigua, no se asume ninguna). Se serializa siempre en UTC con sufijo `Z`, sin
  microsegundos (`2026-03-01T09:00:00Z`), nunca con offset `+00:00`. `GET /tasks?overdue=true`
  excluye tareas sin `due_at` y tareas en estado `HECHA`.
- **Esquemas de respuesta exactos**: ni campos de más ni de menos. Un campo opcional ausente se
  serializa como `null`, nunca se omite. Las colecciones devuelven una lista JSON en la raíz, sin
  objeto envolvente.
- **Errores**: forma estable `{"detail": "<mensaje>"}`; `404` recurso inexistente, `409`
  conflicto, `422` entrada inválida.

Los tests pueden agregar casos, pero no pueden debilitar estas invariantes — son lo que la
revisión de la sesión 10 compara contra el contrato.

## Arquitectura

La estructura interna (capas, ORM, herramienta de migraciones, módulos) queda abierta — el
contrato solo fija comportamiento observable — salvo por estas restricciones ya decididas:

- El catálogo de estados se siembra por migración, no por script de Docker (ver arriba).
- PostgreSQL corre en contenedor aparte (`compose.yaml`), separado del proceso de la API.
