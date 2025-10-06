# Rental Aggregator — Full-Stack Starter

- **Frontend:** Next.js 14 (TS, Tailwind-ready) — deploy on **Vercel**
- **Backend:** FastAPI — deploy on **Fly.io** or **Render** (supports Playwright later)
- **DB:** SQLite for dev (swap to Postgres/Neon in prod)
- **Dev:** `docker compose up` to boot both on localhost

## Local Dev (docker compose)
```
docker compose up
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000/docs
```

## Deploy
- **Frontend (Vercel):**
  - Set env `NEXT_PUBLIC_BACKEND_URL` to your backend public URL.
- **Backend (Fly.io/Render):**
  - Build from `backend` folder.
  - Set env `DATABASE_URL` (e.g., Neon Postgres).
