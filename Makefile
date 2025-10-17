.PHONY: help install migrate run shell test clean collectstatic tailwind-watch tailwind-build superuser backup reset

help:
	@echo "Available commands:"
	@echo "  make install          - Install Python dependencies"
	@echo "  make migrate          - Run database migrations"
	@echo "  make run              - Start Django development server"
	@echo "  make shell            - Open Django shell"
	@echo "  make test             - Run tests"
	@echo "  make clean            - Remove Python cache files"
	@echo "  make collectstatic    - Collect static files"
	@echo "  make tailwind-watch   - Watch and compile Tailwind CSS"
	@echo "  make tailwind-build   - Build Tailwind CSS for production"
	@echo "  make superuser        - Create Django superuser"
	@echo "  make backup           - Backup database"
	@echo "  make reset            - Reset project (delete db, migrations, cache)"

install:
	pip install -r requirements.txt

migrate:
	python manage.py makemigrations
	python manage.py migrate

run:
	python manage.py runserver

shell:
	python manage.py shell

test:
	python manage.py test

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

collectstatic:
	python manage.py collectstatic --noinput

tailwind-watch:
	python manage.py tailwind start

tailwind-build:
	python manage.py tailwind build

superuser:
	python manage.py createsuperuser

backup:
	@mkdir -p backups
	@echo "Backing up database..."
	@cp db.sqlite3 backups/db_backup_$$(date +%Y%m%d_%H%M%S).sqlite3
	@echo "Backup completed: backups/db_backup_$$(date +%Y%m%d_%H%M%S).sqlite3"

reset:
	@echo "🧹 Resetting Django project..."
	@echo "Deleting database..."
	@rm -f db.sqlite3
	@echo "Deleting migration files..."
	@find apps -path "*/migrations/*.py" -not -name "__init__.py" -delete 2>/dev/null || true
	@echo "Cleaning cache files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Reset complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. make migrate    - Recreate database and migrations"
	@echo "  2. make superuser  - Create admin user"
