import React from 'react';
import { Clock } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

export default function QueryHistory({ history, onSelect }) {
  return (
    <div className="bg-card border-glass rounded-xl p-6 mb-6">
      <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
        <Clock className="text-blue-400" size={20} />
        Recent Queries
      </h3>
      
      <div className="space-y-2 max-h-96 overflow-y-auto">
        {history.map((item, index) => (
          <button
            key={index}
            onClick={() => onSelect(item)}
            className="w-full text-left p-3 bg-zinc-900/30 hover:bg-zinc-900/50 rounded-lg border border-white/5 hover:border-violet-500/30 transition-all group"
          >
            <p className="text-sm text-zinc-300 mb-1 line-clamp-2 group-hover:text-white">
              {item.query}
            </p>
            <div className="flex items-center justify-between">
              <span className="text-xs text-zinc-500">
                {formatDistanceToNow(new Date(item.timestamp * 1000), { addSuffix: true })}
              </span>
              <span className="text-xs text-violet-400">
                {(item.confidence_score * 100).toFixed(0)}% confident
              </span>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}