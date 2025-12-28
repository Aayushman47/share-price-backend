import axios from "axios";

export async function fetchWatchlist(symbols) {
  const res = await axios.post(
    "http://127.0.0.1:8000/watchlist",
    symbols
  );
  return res.data;
}
