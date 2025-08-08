.PHONY: up down logs migrate makemigration test lint fmt

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f api worker

makemigration:
	docker compose exec api alembic revision --autogenerate -m "$(m)"

migrate:
	docker compose exec api alembic upgrade head

test:
	pytest -q

lint:
	ruff check vg-backend/app

fmt:
	black vg-backend/app