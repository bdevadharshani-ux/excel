import React, { useEffect, useState } from 'react';
import { Database, FileText, MessageSquare, TrendingUp } from 'lucide-react';
import { datasetService } from '@/services/datasetService';
import { toast } from 'sonner';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const [systemMetrics, datasets] = await Promise.all([
        datasetService.getSystemMetrics(),
        datasetService.listDatasets()
      ]);
      
      setStats({
        ...systemMetrics,
        datasets_count: datasets.length
      });
    } catch (error) {
      toast.error('Failed to load dashboard stats');
    } finally {
      setLoading(false);
    }
  };

  const statCards = [
    {
      label: 'Total Datasets',
      value: stats?.total_datasets || 0,
      icon: Database,
      color: 'violet'
    },
    {
      label: 'Total Queries',
      value: stats?.total_queries || 0,
      icon: MessageSquare,
      color: 'blue'
    },
    {
      label: 'Recent Activity',
      value: stats?.recent_queries?.length || 0,
      icon: TrendingUp,
      color: 'emerald'
    },
  ];

  return (
    <div data-testid="dashboard-page" className="p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Dashboard</h1>
          <p className="text-zinc-400">Welcome to your RAG System overview</p>
        </div>

        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-violet-500"></div>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              {statCards.map((stat, index) => {
                const Icon = stat.icon;
                return (
                  <div
                    key={index}
                    className="bg-card border-glass rounded-xl p-6 hover:border-violet-500/50 transition-all duration-300 group"
                  >
                    <div className="flex items-center justify-between mb-4">
                      <div className={`p-3 rounded-lg bg-${stat.color}-500/10`}>
                        <Icon className={`text-${stat.color}-400`} size={24} />
                      </div>
                    </div>
                    <div className="text-3xl font-bold mb-1">{stat.value}</div>
                    <div className="text-sm text-zinc-400">{stat.label}</div>
                  </div>
                );
              })}
            </div>

            <div className="bg-card border-glass rounded-xl p-6">
              <h2 className="text-2xl font-semibold mb-4 flex items-center gap-2">
                <FileText className="text-violet-400" size={24} />
                Recent Queries
              </h2>
              {stats?.recent_queries && stats.recent_queries.length > 0 ? (
                <div className="space-y-3">
                  {stats.recent_queries.slice(0, 5).map((query, index) => (
                    <div
                      key={index}
                      className="p-4 bg-zinc-900/50 rounded-lg border border-white/5 hover:border-violet-500/30 transition-colors"
                    >
                      <p className="text-sm text-zinc-300 mb-2">{query.query}</p>
                      <div className="flex items-center gap-4 text-xs text-zinc-500">
                        <span>Confidence: {(query.confidence_score * 100).toFixed(1)}%</span>
                        <span>Latency: {query.latency_ms.toFixed(0)}ms</span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-zinc-500 text-center py-8">No queries yet. Start by uploading a dataset and querying it!</p>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}