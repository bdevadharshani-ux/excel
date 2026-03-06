import React, { useEffect, useState } from 'react';
import { datasetService } from '@/services/datasetService';
import { toast } from 'sonner';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { Activity, Clock, TrendingUp } from 'lucide-react';

export default function Monitoring() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
    const interval = setInterval(loadStats, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadStats = async () => {
    try {
      const data = await datasetService.getPerformanceStats();
      setStats(data);
    } catch (error) {
      toast.error('Failed to load monitoring stats');
    } finally {
      setLoading(false);
    }
  };

  const latencyData = stats?.recent_queries?.map((q, i) => ({
    name: `Q${i + 1}`,
    latency: q.latency_ms
  })) || [];

  return (
    <div data-testid="monitoring-page" className="p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">System Monitoring</h1>
          <p className="text-zinc-400">Real-time performance metrics and analytics</p>
        </div>

        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-violet-500"></div>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="bg-card border-glass rounded-xl p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-3 rounded-lg bg-violet-500/10">
                    <Activity className="text-violet-400" size={24} />
                  </div>
                  <div>
                    <p className="text-sm text-zinc-500">Total Queries</p>
                    <p className="text-2xl font-bold">{stats?.total_queries || 0}</p>
                  </div>
                </div>
              </div>

              <div className="bg-card border-glass rounded-xl p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-3 rounded-lg bg-blue-500/10">
                    <Clock className="text-blue-400" size={24} />
                  </div>
                  <div>
                    <p className="text-sm text-zinc-500">Avg Latency</p>
                    <p className="text-2xl font-bold">{stats?.avg_latency_ms?.toFixed(0) || 0}ms</p>
                  </div>
                </div>
              </div>

              <div className="bg-card border-glass rounded-xl p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-3 rounded-lg bg-emerald-500/10">
                    <TrendingUp className="text-emerald-400" size={24} />
                  </div>
                  <div>
                    <p className="text-sm text-zinc-500">Peak Latency</p>
                    <p className="text-2xl font-bold">{stats?.max_latency_ms?.toFixed(0) || 0}ms</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-card border-glass rounded-xl p-6 mb-6">
              <h2 className="text-xl font-semibold mb-6">Query Latency Trend</h2>
              {latencyData.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={latencyData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
                    <XAxis dataKey="name" stroke="#71717a" />
                    <YAxis stroke="#71717a" />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#18181b',
                        border: '1px solid rgba(255,255,255,0.1)',
                        borderRadius: '8px'
                      }}
                    />
                    <Line
                      type="monotone"
                      dataKey="latency"
                      stroke="#7c3aed"
                      strokeWidth={2}
                      dot={{ fill: '#7c3aed', r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <p className="text-zinc-500 text-center py-12">No query data available yet</p>
              )}
            </div>

            <div className="bg-card border-glass rounded-xl p-6">
              <h2 className="text-xl font-semibold mb-6">Performance Distribution</h2>
              {latencyData.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={latencyData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
                    <XAxis dataKey="name" stroke="#71717a" />
                    <YAxis stroke="#71717a" />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#18181b',
                        border: '1px solid rgba(255,255,255,0.1)',
                        borderRadius: '8px'
                      }}
                    />
                    <Bar dataKey="latency" fill="#3b82f6" radius={[8, 8, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <p className="text-zinc-500 text-center py-12">No performance data available yet</p>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}