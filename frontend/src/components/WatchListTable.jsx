import { useState } from "react";

export default function WatchlistTable({ data, onRemove }) {
  const [expanded, setExpanded] = useState(null);

  if (!data?.length) {
    return <p className="text-zinc-400">No data available.</p>;
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead className="bg-zinc-800 text-zinc-300">
          <tr>
            <th className="p-3 text-left">Symbol</th>
            <th>Price</th>
            <th>Day %</th>
            <th>Status</th>
            <th>Momentum</th>
            <th>Daily</th>
            <th>Intraday</th>
            <th>Action</th>
            <th></th>
          </tr>
        </thead>

        <tbody>
          {data.map((row) => {
            const snap = row.snapshot;
            const daily = row.daily;
            const intraday = row.intraday;
            const open = expanded === row.symbol;

            return (
              <>
                <tr
                  key={row.symbol}
                  onClick={() =>
                    setExpanded(open ? null : row.symbol)
                  }
                  className="border-b border-zinc-800 hover:bg-zinc-800/70
                             transition cursor-pointer"
                >
                  <td className="p-3 font-semibold">{row.symbol}</td>
                  <td>{snap?.current_price?.toFixed(2) ?? "—"}</td>

                  <td
                    className={
                      snap?.day_change_pct >= 0
                        ? "text-green-400"
                        : "text-red-400"
                    }
                  >
                    {snap
                      ? `${snap.day_change_pct.toFixed(2)}%`
                      : "—"}
                  </td>

                  <td>
                    <span className="px-2 py-1 rounded-full bg-zinc-700 text-xs">
                      {snap?.status ?? "—"}
                    </span>
                  </td>

                  <td>
                    <span className="px-2 py-1 rounded-full bg-zinc-700 text-xs">
                      {snap?.momentum ?? "—"}
                    </span>
                  </td>

                  <td>{daily?.predicted_move_pct ?? "—"}%</td>
                  <td>{intraday?.predicted_move_pct ?? "—"}%</td>

                  <td>
                    <span className="px-2 py-1 rounded-full bg-blue-600/20 text-blue-400 text-xs">
                      {daily?.trade_intensity ?? "—"}
                    </span>
                  </td>

                  <td>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onRemove(row.symbol);
                      }}
                      className="text-red-400 hover:text-red-300"
                    >
                      ✕
                    </button>
                  </td>
                </tr>

                {open && (
                  <tr className="bg-zinc-800 animate-fadeIn">
                    <td colSpan="9" className="p-4 space-y-4">
                      <div className="flex gap-6 text-sm">
                        <span>
                          <strong>Regime:</strong>{" "}
                          {daily?.regime ?? "—"}
                        </span>
                        <span>
                          <strong>Confidence:</strong>{" "}
                          {daily
                            ? `${(daily.confidence * 100).toFixed(
                                1
                              )}%`
                            : "—"}
                        </span>
                        <span>
                          <strong>Intraday:</strong>{" "}
                          {intraday?.time_ist ?? "—"}
                        </span>
                      </div>

                      

                      {row.error && (
                        <div className="text-red-400">
                          Error: {row.error}
                        </div>
                      )}
                    </td>
                  </tr>
                )}
              </>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
