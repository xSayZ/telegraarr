# Telegraarr 🤖

A Telegram bot for your \*arr stack. Query requests, check downloads, and search your library - all from Telegram.

Built because I wanted a quick and fun way to let friends and family know what's downloading and what's available on my home server without giving everyone access to Jellyseerr or Sonarr.

---

## Honest disclaimer

This project is fully vibe coded. I built it because I wanted something that worked for my setup, and because it was a fun excuse to try building a Telegram bot. It works for me, but it's rough around the edges and there's almost certainly a better way to do half of it.

That said - contributions are **very much welcomed**. If you spot something that's wrong, overcomplicated, inefficient, or just plain silly, please open an issue or a PR. I mean that genuinely. You don't need to ask permission, you don't need to write a perfect solution, and you don't need to be an expert. If you have an idea or a fix, just go for it.

---

## What it does

- `/start` - introduction and shows your Telegram ID
- `/register <email>` - request access using your Jellyseerr email
- `/requests <query>` - search all Jellyseerr requests by title
- `/queue` - view the active download queue across Sonarr, Radarr, and Sonarr Anime
- `/available <title>` - check if something is already in your Jellyfin library
- `/status` - server overview: downloads, requests, library counts, recently added, disk space

Admin commands:
- `/approve <telegram_id>` - approve a registration request
- `/deny <telegram_id>` - deny a registration request
- `/unblock <telegram_id>` - unblock a user after too many failed registration attempts

---

## Image
```bash
docker pull ghcr.io/xsayz/telegraarr:latest
```

---

## Requirements

- A running \*arr stack (Sonarr, Radarr, Jellyseerr, Jellyfin)
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- Docker or Podman

---

## Quick start

### 1. Create a Telegram bot

Message [@BotFather](https://t.me/BotFather) on Telegram and run `/newbot`. Save the token it gives you.

### 2. Get your Telegram ID

Start a chat with your bot and send any message, then visit:
```
https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
```
Your ID is in the `from.id` field.

### 3. Configure
```bash
cp .env.example .env
```

Fill in your values. See `.env.example` for all available options.

### 4. Run with Docker
```bash
docker build -t telegraarr .
docker run -d \
  --name telegraarr \
  --env-file .env \
  -v ./config:/config \
  telegraarr
```

### 5. Run with Podman Quadlet

Copy `telegraarr.container` to `~/.config/containers/systemd/`, fill in your env file, then:
```bash
systemctl --user daemon-reload
systemctl --user start telegraarr
```

---

## Configuration

All configuration is done via environment variables. See `.env.example` for the full list.

| Variable | Required | Default | Description |
|---|---|---|---|
| `BOT_TOKEN` | ✅ | - | Telegram bot token from BotFather |
| `ADMIN_TELEGRAM_ID` | ✅ | - | Your Telegram ID |
| `JELLYSEERR_URL` | ✅ | `http://jellyseerr:5055` | Jellyseerr base URL |
| `JELLYSEERR_API_KEY` | ✅ | - | Jellyseerr API key |
| `SONARR_URL` | ✅ | `http://sonarr:8989` | Sonarr base URL |
| `SONARR_API_KEY` | ✅ | - | Sonarr API key |
| `SONARR_ANIME_URL` | ➖ | - | Second Sonarr instance for anime |
| `SONARR_ANIME_API_KEY` | ➖ | - | API key for anime Sonarr |
| `RADARR_URL` | ✅ | `http://radarr:7878` | Radarr base URL |
| `RADARR_API_KEY` | ✅ | - | Radarr API key |
| `JELLYFIN_URL` | ✅ | `http://jellyfin:8096` | Jellyfin base URL |
| `JELLYFIN_API_KEY` | ✅ | - | Jellyfin API key |
| `DB_PATH` | ➖ | `/config/telegraarr.db` | Path to SQLite database |

---

## Project structure
```
telegraarr/
├── telegraarr/
│   ├── bot.py              # entrypoint, command registration
│   ├── config.py           # environment variable loading
│   ├── auth.py             # authentication decorators
│   ├── database.py         # SQLite operations
│   ├── commands/
│   │   ├── register.py     # /register
│   │   ├── admin.py        # /approve, /deny, /unblock
│   │   ├── requests.py     # /requests
│   │   ├── queue.py        # /queue
│   │   ├── available.py    # /available
│   │   └── status.py       # /status
│   └── services/
│       ├── jellyseerr.py   # Jellyseerr API client
│       ├── arr.py          # Sonarr + Radarr API clients
│       └── jellyfin.py     # Jellyfin API client
├── .env.example
├── Dockerfile
├── telegraarr.container    # Podman Quadlet unit
└── pyproject.toml
```

---

## Contributing

Contributions are very welcome - seriously. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

If something doesn't work, open an issue. If you want to add a feature or fix something, open a PR. No contribution is too small.

---

## License

GPL-3.0 - see [LICENSE](LICENSE).