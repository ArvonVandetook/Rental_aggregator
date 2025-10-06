# Frontend (Next.js on Vercel)

## Dev
```
cd frontend
npm i
npm run dev
# ensure backend is running on :8000
```
Set `.env.local`:
```
NEXT_PUBLIC_BACKEND_URL=http://127.0.0.1:8000
```

## Deploy (Vercel)
- New Project → Import this `frontend` folder
- Set Environment Variable `NEXT_PUBLIC_BACKEND_URL` to your backend URL (Fly.io/Render/etc).
- Build & deploy.
