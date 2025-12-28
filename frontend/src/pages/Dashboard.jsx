import { useEffect, useState } from "react";
import Header from "../components/Header";
import WatchlistTable from "../components/WatchListTable";
import { fetchWatchlist } from "../api/watchlist";

const DEFAULT_SYMBOLS = [
  "RELIANCE.NS",
  "TCS.NS",
  "NIFTY.NS",
  "HDFCBANK.NS",
];

export default function Dashboard() {
  const [symbols, setSymbols] = useState(() => {
    const saved = localStorage.getItem("watchlist");
    return saved ? JSON.parse(saved) : DEFAULT_SYMBOLS;
  });

  const [data, setData] = useState([]);
  const [newSymbol, setNewSymbol] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    localStorage.setItem("watchlist", JSON.stringify(symbols));
    loadData();
    // eslint-disable-next-line
  }, [symbols]);

  async function loadData() {
    setLoading(true);
    try {
      const res = await fetchWatchlist(symbols);
      setData(res);
    } finally {
      setLoading(false);
    }
  }

  function addSymbol() {
    const sym = newSymbol.trim().toUpperCase();
    if (!sym || symbols.includes(sym)) return;
    setSymbols([...symbols, sym]);
    setNewSymbol("");
  }

  function removeSymbol(sym) {
    setSymbols(symbols.filter((s) => s !== sym));
  }

  return (
    <>
      <Header />

      <div className="max-w-7xl mx-auto px-6 py-6 space-y-6">
        {/* Add symbol */}
        <div className="flex gap-3">
          <input
            value={newSymbol}
            onChange={(e) => setNewSymbol(e.target.value)}
            placeholder="Add symbol (e.g. INFY.NS)"
            className="flex-1 px-4 py-2 rounded-lg bg-zinc-800 border border-zinc-700
                       focus:outline-none focus:ring-2 focus:ring-blue-500
                       transition"
          />
          <button
            onClick={addSymbol}
            className="px-5 py-2 rounded-lg bg-blue-600 hover:bg-blue-500
                       active:scale-95 transition font-semibold"
          >
            Add
          </button>
        </div>

        {loading && (
          <p className="text-zinc-400">Loading market data…</p>
        )}

        <WatchlistTable
          data={data}
          onRemove={removeSymbol}
        />
      </div>
    </>
  );
}
