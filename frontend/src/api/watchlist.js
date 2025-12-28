const API_BASE = import.meta.env.VITE_API_BASE_URL;

export async function fetchWatchlist(symbols) {
  const res = await fetch(`${API_BASE}/watchlist`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(symbols),
  });

  return res.json();
}
