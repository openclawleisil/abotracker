# AboTracker (MVP)

Ein kleines, einfaches Web‑Tool zum Tracken monatlicher Abokosten.

Tech: Flask + SQLite + Bootstrap + Docker Compose

Start:

```bash
# build & run
docker compose up --build -d

# Stop + cleanup
docker compose down --rmi all --volumes
```

Ziel: schnell testbar, leicht zu löschen (alles im Projekt‑Ordner / Docker Volumes).