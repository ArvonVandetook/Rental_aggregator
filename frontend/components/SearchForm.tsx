'use client';
import { useState } from 'react';
import { startSearch } from '../lib/api';

export default function SearchForm({ onSearched }: { onSearched: () => void }) {
  const [location, setLocation] = useState('sfbay');
  const [minPrice, setMinPrice] = useState<number | undefined>(1500);
  const [maxPrice, setMaxPrice] = useState<number | undefined>(3500);
  const [beds, setBeds] = useState<number | undefined>(1);
  const [keywords, setKeywords] = useState<string>('');

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    await startSearch({ location, min_price: minPrice, max_price: maxPrice, beds, keywords });
    onSearched();
  };

  return (
    <form onSubmit={submit} className="grid grid-cols-2 md:grid-cols-6 gap-3 bg-white p-4 rounded-2xl shadow">
      <div className="col-span-2">
        <label className="text-xs text-gray-500">Craigslist Region</label>
        <input className="w-full border rounded px-2 py-1" value={location} onChange={e=>setLocation(e.target.value)} placeholder="sfbay" />
      </div>
      <div>
        <label className="text-xs text-gray-500">Min $</label>
        <input type="number" className="w-full border rounded px-2 py-1" value={minPrice ?? ''} onChange={e=>setMinPrice(e.target.value ? Number(e.target.value) : undefined)} />
      </div>
      <div>
        <label className="text-xs text-gray-500">Max $</label>
        <input type="number" className="w-full border rounded px-2 py-1" value={maxPrice ?? ''} onChange={e=>setMaxPrice(e.target.value ? Number(e.target.value) : undefined)} />
      </div>
      <div>
        <label className="text-xs text-gray-500">Beds</label>
        <input type="number" className="w-full border rounded px-2 py-1" value={beds ?? ''} onChange={e=>setBeds(e.target.value ? Number(e.target.value) : undefined)} />
      </div>
      <div className="col-span-2 md:col-span-1">
        <label className="text-xs text-gray-500">Keywords</label>
        <input className="w-full border rounded px-2 py-1" value={keywords} onChange={e=>setKeywords(e.target.value)} placeholder="dog friendly, yard..." />
      </div>
      <div className="col-span-2 md:col-span-1 flex items-end">
        <button type="submit" className="w-full bg-black text-white rounded px-3 py-2">Search</button>
      </div>
    </form>
  )
}
