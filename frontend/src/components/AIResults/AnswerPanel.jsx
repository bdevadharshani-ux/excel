import React from 'react';
import { Sparkles, CheckCircle } from 'lucide-react';

export default function AnswerPanel({ result }) {
  if (!result) return null;

  return (
    <div className="bg-card border-glass rounded-xl p-6">
      <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
        <Sparkles className="text-violet-400" size={20} />
        AI-Generated Answer
      </h3>
      
      <div className="bg-gradient-to-br from-violet-900/20 via-background to-background p-6 rounded-lg border border-violet-500/20">
        <p className="text-zinc-200 leading-relaxed">{result.answer}</p>
      </div>

      <div className="mt-4 flex items-center gap-2 text-sm text-zinc-500">
        <CheckCircle className="text-emerald-400" size={16} />
        <span>Grounded in {result.supporting_rows.length} data sources</span>
      </div>
    </div>
  );
}