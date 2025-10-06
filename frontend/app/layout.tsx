import "./globals.css";

export const metadata = {
  title: "Rental Aggregator",
  description: "AI-aided rental search",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen">
        <div className="max-w-5xl mx-auto p-6">
          <header className="mb-6">
            <h1 className="text-2xl font-semibold">Rental Aggregator</h1>
            <p className="text-sm text-gray-600">Search multiple sources with one query.</p>
          </header>
          {children}
        </div>
      </body>
    </html>
  );
}
