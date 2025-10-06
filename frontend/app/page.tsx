import SearchForm from '../components/SearchForm';
import { fetchListings } from '../lib/api';

export default async function Page() {
  const { items } = await fetchListings({ limit: 30, offset: 0 });

  return (
    <div className="space-y-4">
      <SearchForm onSearched={async () => {}} />
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {items.map(l => (
          <a key={l.id} href={l.source_url} target="_blank" className="bg-white rounded-2xl shadow overflow-hidden hover:shadow-lg transition">
            {l.photo ? <img src={l.photo} alt={l.title} className="w-full h-40 object-cover" /> : <div className="w-full h-40 bg-gray-200" />}
            <div className="p-3">
              <div className="text-sm text-gray-500">{l.source} • {l.city}</div>
              <div className="font-medium line-clamp-2">{l.title}</div>
              <div className="text-lg">${'{'}l.price ?? '—'{'}'}</div>
            </div>
          </a>
        ))}
      </div>
    </div>
  );
}
