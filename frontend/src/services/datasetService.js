import api from './api';

export const datasetService = {
  async uploadDataset(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  async listDatasets() {
    const response = await api.get('/upload/datasets');
    return response.data.datasets;
  },

  async queryDataset(datasetId, query, datasetIds = null) {
    const payload = {
      query: query,
      use_cache: true,
    };
    
    if (datasetIds && datasetIds.length > 1) {
      payload.dataset_id = datasetIds[0];
      payload.dataset_ids = datasetIds;
    } else {
      payload.dataset_id = datasetId;
    }
    
    const response = await api.post('/query', payload);
    return response.data;
  },

  async getQueryHistory(limit = 20) {
    const response = await api.get(`/query/history?limit=${limit}`);
    return response.data;
  },

  async exportQueryResult(queryId) {
    const response = await api.get(`/query/export/${queryId}`, {
      responseType: 'blob',
    });
    
    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `query_result_${queryId.substring(0, 8)}.xlsx`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  },

  async getPerformanceStats() {
    const response = await api.get('/monitoring/performance');
    return response.data;
  },

  async getSystemMetrics() {
    const response = await api.get('/monitoring/system');
    return response.data;
  },
};