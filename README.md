# VG Backend

## Quickstart

- Copy `.env.example` to `.env` and adjust values.
- Start services:

```bash
make up
```

- Apply migrations:

```bash
make migrate
```

- API at `http://localhost:8000` (docs at `/docs`).

## Endpoints

- GET `/api/v1/health`
- Inventory:
  - GET `/api/v1/inventory/stock`
  - POST `/api/v1/inventory/movements`
