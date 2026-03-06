import React from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { TrendingUp } from 'lucide-react';

export default function VisualChart({ result }) {
  if (!result || !result.supporting_rows) return null;

  // Try to detect numerical data from supporting rows
  const detectChartData = () => {
    const rows = result.supporting_rows;
    if (rows.length === 0) return null;

    // Get all numerical columns
    const firstRow = rows[0].data;
    const numericalColumns = Object.keys(firstRow).filter(key => {
      const value = firstRow[key];
      return typeof value === 'number' || !isNaN(parseFloat(value));
    });

    if (numericalColumns.length === 0) return null;

    // Create chart data
    const chartData = rows.slice(0, 10).map((row, index) => {
      const dataPoint = { name: `Row ${index + 1}` };
      numericalColumns.forEach(col => {
        dataPoint[col] = parseFloat(row.data[col]) || 0;
      });
      return dataPoint;
    });

    return {
      data: chartData,
      columns: numericalColumns
    };
  };

  const chartInfo = detectChartData();
  if (!chartInfo) return null;

  const COLORS = ['#7c3aed', '#3b82f6', '#10b981', '#f59e0b', '#ef4444'];

  return (
    <div className="bg-card border-glass rounded-xl p-6">
      <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
        <TrendingUp className="text-emerald-400" size={20} />
        Visual Insights
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Bar Chart */}
        <div className="bg-zinc-900/30 rounded-lg p-4">
          <p className="text-xs text-zinc-500 mb-3">Distribution</p>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={chartInfo.data}>
              <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
              <XAxis dataKey="name" stroke="#71717a" fontSize={10} />
              <YAxis stroke="#71717a" fontSize={10} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#18181b',
                  border: '1px solid rgba(255,255,255,0.1)',
                  borderRadius: '8px'
                }}
              />
              {chartInfo.columns.slice(0, 3).map((col, index) => (
                <Bar
                  key={col}
                  dataKey={col}
                  fill={COLORS[index % COLORS.length]}
                  radius={[4, 4, 0, 0]}
                />
              ))}
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Line Chart */}
        <div className="bg-zinc-900/30 rounded-lg p-4">
          <p className="text-xs text-zinc-500 mb-3">Trends</p>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={chartInfo.data}>
              <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
              <XAxis dataKey="name" stroke="#71717a" fontSize={10} />
              <YAxis stroke="#71717a" fontSize={10} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#18181b',
                  border: '1px solid rgba(255,255,255,0.1)',
                  borderRadius: '8px'
                }}
              />
              {chartInfo.columns.slice(0, 3).map((col, index) => (
                <Line
                  key={col}
                  type="monotone"
                  dataKey={col}
                  stroke={COLORS[index % COLORS.length]}
                  strokeWidth={2}
                  dot={{ fill: COLORS[index % COLORS.length], r: 3 }}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}