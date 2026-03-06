import React from 'react';
import { Table } from 'lucide-react';

export default function RetrievedContextTable({ result }) {
  if (!result || !result.supporting_rows) return null;

  const displayData = result.supporting_rows.slice(0, 5);

  return (
    <div className="bg-card border-glass rounded-xl p-6">
      <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
        <Table className="text-blue-400" size={20} />
        Retrieved Context ({result.supporting_rows.length} sources)
      </h3>
      
      <div className="space-y-3">
        {displayData.map((row, index) => (
          <div
            key={index}
            className="p-4 bg-zinc-900/50 rounded-lg border border-white/5 hover:border-violet-500/30 transition-colors"
          >
            <div className="flex items-start justify-between mb-2">
              <span className="text-xs font-mono text-violet-400">{row.row_id}</span>
              <span className="text-xs text-zinc-500">
                Similarity: {(result.similarity_scores[index] * 100).toFixed(1)}%
              </span>
            </div>
            <p className="text-sm text-zinc-300 font-mono">{row.text}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
