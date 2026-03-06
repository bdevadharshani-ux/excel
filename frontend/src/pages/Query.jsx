import React, { useState, useEffect } from 'react';
import { datasetService } from '@/services/datasetService';
import { toast } from 'sonner';
import { Send, Sparkles, TrendingUp, Database, Download, History, Lightbulb } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Checkbox } from '@/components/ui/checkbox';
import RetrievedContextTable from '@/components/Retrieval/RetrievedContextTable';
import AnswerPanel from '@/components/AIResults/AnswerPanel';
import VisualChart from '@/components/AIResults/VisualChart';
import QueryHistory from '@/components/Query/QueryHistory';

export default function Query() {
  const [datasets, setDatasets] = useState([]);
  const [selectedDatasets, setSelectedDatasets] = useState([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    loadDatasets();
    loadHistory();
  }, []);

  const loadDatasets = async () => {
    try {
      const data = await datasetService.listDatasets();
      setDatasets(data);
      if (data.length > 0) {
        setSelectedDatasets([data[0].dataset_id]);
        setSuggestions(data[0].suggestions || []);
      }
    } catch (error) {
      toast.error('Failed to load datasets');
    }
  };

  const loadHistory = async () => {
    try {
      const data = await datasetService.getQueryHistory();
      setHistory(data.history || []);
    } catch (error) {
      console.error('Failed to load history');
    }
  };

  const toggleDataset = (datasetId) => {
    setSelectedDatasets(prev => {
      if (prev.includes(datasetId)) {
        return prev.filter(id => id !== datasetId);
      } else {
        return [...prev, datasetId];
      }
    });
    
    // Update suggestions based on selected datasets
    const selected = datasets.filter(d => selectedDatasets.includes(d.dataset_id) || d.dataset_id === datasetId);
    const allSuggestions = selected.flatMap(d => d.suggestions || []);
    setSuggestions([...new Set(allSuggestions)].slice(0, 10));
  };

  const handleQuery = async () => {
    if (!query.trim()) {
      toast.error('Please enter a query');
      return;
    }
    if (selectedDatasets.length === 0) {
      toast.error('Please select at least one dataset');
      return;
    }

    setLoading(true);
    try {
      const response = await datasetService.queryDataset(
        selectedDatasets.length === 1 ? selectedDatasets[0] : null,
        query,
        selectedDatasets.length > 1 ? selectedDatasets : null
      );
      setResult(response);
      loadHistory(); // Refresh history
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Query failed');
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    if (!result || !result.query_id) {
      toast.error('No query result to export');
      return;
    }
    
    try {
      await datasetService.exportQueryResult(result.query_id);
      toast.success('Query result exported successfully!');
    } catch (error) {
      toast.error('Export failed');
    }
  };

  const applySuggestion = (suggestion) => {
    setQuery(suggestion);
  };

  const loadHistoryQuery = (historyItem) => {
    setQuery(historyItem.query);
    setResult(historyItem);
  };

  return (
    <div data-testid="query-page" className="p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold mb-2">Query Interface</h1>
            <p className="text-zinc-400">Ask questions about your datasets using natural language</p>
          </div>
          <Button
            onClick={() => setShowHistory(!showHistory)}
            variant="outline"
            className="border-white/10"
          >
            <History size={18} className="mr-2" />
            {showHistory ? 'Hide' : 'Show'} History
          </Button>
        </div>

        <div className="grid grid-cols-12 gap-6">
          <div className="col-span-12 lg:col-span-8 space-y-6">
            <div className="bg-card border-glass rounded-xl p-6">
              <label className="text-sm font-medium text-zinc-300 block mb-3">Select Dataset(s)</label>
              {datasets.length === 0 ? (
                <div className="text-center py-8 text-zinc-500">
                  <Database className="mx-auto mb-3 text-zinc-600" size={48} />
                  <p>No datasets available. Please upload a dataset first.</p>
                </div>
              ) : (
                <div className="space-y-2">
                  {datasets.map((dataset) => (
                    <div key={dataset.dataset_id} className="flex items-center space-x-3 p-3 bg-zinc-900/30 rounded-lg hover:bg-zinc-900/50">
                      <Checkbox
                        checked={selectedDatasets.includes(dataset.dataset_id)}
                        onCheckedChange={() => toggleDataset(dataset.dataset_id)}
                      />
                      <div className="flex-1">
                        <p className="text-sm font-medium">{dataset.filename}</p>
                        <p className="text-xs text-zinc-500">{dataset.num_rows} rows, {dataset.num_columns} columns</p>
                      </div>
                    </div>
                  ))}
                  {selectedDatasets.length > 1 && (
                    <p className="text-xs text-violet-400 mt-2">✓ Multi-dataset querying enabled ({selectedDatasets.length} datasets)</p>
                  )}
                </div>
              )}
            </div>

            {suggestions.length > 0 && (
              <div className="bg-card border-glass rounded-xl p-6">
                <h3 className="text-sm font-medium text-zinc-300 mb-3 flex items-center gap-2">
                  <Lightbulb className="text-yellow-400" size={18} />
                  Suggested Questions
                </h3>
                <div className="flex flex-wrap gap-2">
                  {suggestions.slice(0, 6).map((suggestion, index) => (
                    <button
                      key={index}
                      onClick={() => applySuggestion(suggestion)}
                      className="px-3 py-1.5 text-xs bg-violet-500/10 hover:bg-violet-500/20 text-violet-300 rounded-lg border border-violet-500/20 transition-colors"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              </div>
            )}

            <div className="bg-card border-glass rounded-xl p-6">
              <label className="text-sm font-medium text-zinc-300 block mb-3 flex items-center gap-2">
                <Sparkles className="text-violet-400" size={18} />
                Ask a Question
              </label>
              <div className="flex gap-3">
                <Input
                  data-testid="query-input"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleQuery()}
                  placeholder="e.g., What is the average value in column X?"
                  className="bg-zinc-900/50 border-white/10 focus:border-violet-500"
                  disabled={loading || selectedDatasets.length === 0}
                />
                <Button
                  data-testid="query-submit-button"
                  onClick={handleQuery}
                  disabled={loading || selectedDatasets.length === 0}
                  className="bg-violet-600 hover:bg-violet-700 shadow-[0_0_15px_-3px_rgba(124,58,237,0.4)]"
                >
                  {loading ? 'Processing...' : <Send size={18} />}
                </Button>
              </div>
            </div>

            {result && (
              <>
                <div className="flex justify-end">
                  <Button
                    onClick={handleExport}
                    variant="outline"
                    className="border-white/10"
                  >
                    <Download size={16} className="mr-2" />
                    Export to Excel
                  </Button>
                </div>
                <AnswerPanel result={result} />
                <VisualChart result={result} />
                <RetrievedContextTable result={result} />
              </>
            )}
          </div>

          <div className="col-span-12 lg:col-span-4">
            {showHistory && history.length > 0 && (
              <QueryHistory history={history} onSelect={loadHistoryQuery} />
            )}
            
            {result && (
              <div className="bg-card border-glass rounded-xl p-6 sticky top-8">
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <TrendingUp className="text-blue-400" size={20} />
                  Metrics
                </h3>
                <div className="space-y-4">
                  <div>
                    <p className="text-xs text-zinc-500 mb-1">Confidence Score</p>
                    <div className="flex items-center gap-2">
                      <div className="flex-1 h-2 bg-zinc-800 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-violet-500 to-blue-500"
                          style={{ width: `${result.confidence_score * 100}%` }}
                        />
                      </div>
                      <span className="text-sm font-medium">{(result.confidence_score * 100).toFixed(1)}%</span>
                    </div>
                  </div>
                  
                  <div className="pt-4 border-t border-white/5">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p className="text-xs text-zinc-500 mb-1">Latency</p>
                        <p className="text-lg font-semibold">{result.latency_ms.toFixed(0)}ms</p>
                      </div>
                      <div>
                        <p className="text-xs text-zinc-500 mb-1">Sources</p>
                        <p className="text-lg font-semibold">{result.supporting_rows.length}</p>
                      </div>
                    </div>
                  </div>

                  {result.cached && (
                    <div className="pt-4 border-t border-white/5">
                      <p className="text-xs text-emerald-400">✓ Retrieved from cache</p>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}