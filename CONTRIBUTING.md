# Contributing to Telegraarr

First of all — thank you for even considering contributing. This project started as a fun vibe-coded weekend thing and I'd love to see it grow beyond just my use case.

There are no strict rules here. If you want to contribute, just do it. That said, here are some loose guidelines to make things smoother for everyone.

---

## The spirit of this project

This is a homelab tool. The people using it are running their own servers, managing their own stacks, and generally comfortable figuring things out. That means:

- Simplicity is valued over cleverness
- A working rough solution is better than a perfect one that never ships
- If something works for your setup, it's probably worth sharing even if it's not generalised

---

## Ways to contribute

- **Bug reports** — something broken? Open an issue. The more detail the better — what happened, what you expected, what your setup looks like
- **Feature requests** — have an idea? Open an issue and describe what you want and why. No need to implement it yourself
- **Bug fixes** — spot a bug and know how to fix it? Just open a PR
- **New features** — want to add something? Open an issue first so we can discuss before you spend time on it
- **Documentation** — README unclear? Setup steps wrong? Fix it. Docs PRs are always welcome
- **New service integrations** — running Prowlarr, Bazarr, Lidarr, or something else? Adding support is very welcome
- **Tests** — there are none right now. If you want to add them, please do
- **Code cleanup** — see something that could be simpler or cleaner? Go for it

---

## Getting started locally
```bash
# Clone the repo
git clone https://github.com/<your-username>/telegraarr.git
cd telegraarr

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Set up your environment
cp .env.example .env
# Fill in your values in .env

# Run the bot
python -m telegraarr.bot
```

---

## Code style

- We use [Ruff](https://github.com/astral-sh/ruff) for linting and formatting
- Run `ruff check .` and `ruff format .` before submitting a PR
- Line length is 100 characters
- Type hints are encouraged but not required everywhere

---

## Pull requests

- Keep PRs focused — one thing per PR is easier to review
- Write a clear description of what you changed and why
- If your PR fixes an issue, reference it with `Fixes #123`
- Don't worry about a perfect commit history — squashing is fine

---

## Adding a new service

If you want to add support for a new service (e.g. Lidarr, Bazarr, Prowlarr):

1. Add a new client in `telegraarr/services/`
2. Add any new config variables to `config.py` with sensible defaults
3. Add the new variables to `.env.example` with comments
4. Wire it into the relevant commands or add new ones
5. Update the README config table

---

## Questions

Not sure about something? Open an issue and just ask. There are no stupid questions here.