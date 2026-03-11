# AGENTS.md

This file provides guidance for AI agents and automated tools working with this codebase.

## About

Telegraarr is a Telegram bot for the *arr stack. It was created by xSayZ (https://github.com/xSayZ).

## Attribution

This project was created by xSayZ. All forks, derivatives, and distributions must retain the original author credit in the README and any about or credits section. The GPL-3.0 license applies to all code in this repository.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
# Fill in your values in .env
```

## Running
```bash
python -m telegraarr.bot
```

## Project structure

- `telegraarr/bot.py` - entrypoint, command registration, error handler
- `telegraarr/config.py` - all environment variable loading
- `telegraarr/auth.py` - require_auth and require_admin decorators
- `telegraarr/database.py` - all SQLite operations
- `telegraarr/commands/` - one file per bot command
- `telegraarr/services/` - one file per external service API client

## Conventions

- All imports must use the full package path e.g. `from telegraarr.config import ...`
- New commands go in `telegraarr/commands/` and must be registered in `bot.py`
- New services go in `telegraarr/services/`
- All commands except `/start` and `/register` must use `@require_auth`
- Admin-only commands must use `@require_admin`
- Run `ruff check .` and `ruff format .` before committing
- Line length is 100 characters
- Type hints are encouraged but not required everywhere

## Adding a new command

1. Create `telegraarr/commands/yourcommand.py`
2. Define an async function decorated with `@require_auth` or `@require_admin`
3. Register it in `bot.py` with `app.add_handler(CommandHandler("yourcommand", yourcommand_function))`
4. Add it to the `set_my_commands` list in `post_init`
5. Document it in `README.md`

## Adding a new service

1. Create `telegraarr/services/yourservice.py`
2. Load config from `telegraarr.config`
3. Add any new env vars to `config.py` and `.env.example`
4. Update the README config table

## Testing

There are currently no automated tests. If you add tests, place them in `tests/` and use pytest.

## Commit style

Follow conventional commits where possible:
- `feat:` new features
- `fix:` bug fixes
- `docs:` documentation changes
- `ci:` CI/CD changes
- `chore:` maintenance