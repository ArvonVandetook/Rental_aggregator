export type Listing = {
  id: number;
  source: string;
  source_url: string;
  title: string;
  description: string;
  price: number | null;
  beds: number | null;
  baths: number | null;
  city: string;
  photo: string;
  posted_at: string | null;
  scraped_at: string | null;
};

const API_BASE = process.env.NEXT_PUBLIC_BACKEND_URL;

export async function startSearch(payload: {
  location: string;
  min_price?: number;
  max_price?: number;
  beds?: number;
  baths?: number;
  keywords?: string;
}) {
  const r = await fetch(`${API_BASE}/search`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
    cache: "no-store"
  });
  if (!r.ok) throw new Error(`Search failed: ${r.status}`);
  return r.json();
}

export async function fetchListings(params: { limit?: number; offset?: number }) {
  const qs = new URLSearchParams();
  if (params.limit) qs.set("limit", String(params.limit));
  if (params.offset) qs.set("offset", String(params.offset));
  const r = await fetch(`${API_BASE}/listings?${qs.toString()}`, { cache: "no-store" });
  if (!r.ok) throw new Error(`List failed: ${r.status}`);
  return r.json() as Promise<{ items: Listing[]; count: number }>;
}
