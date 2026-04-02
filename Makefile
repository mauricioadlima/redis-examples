ENV_NAME=redis-examples

setup:
	@colima start || true
	@docker context use colima
	@docker-compose up -d
	@if [ ! -d "$(ENV_NAME)" ]; then python3 -m venv $(ENV_NAME); fi
	@. $(ENV_NAME)/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

stop:
	@docker-compose down || true
	@colima stop || true

run:
	@. $(ENV_NAME)/bin/activate && pytest