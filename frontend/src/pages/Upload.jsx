import React, { useState, useRef } from 'react';
import { Upload as UploadIcon, FileText, CheckCircle, XCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { datasetService } from '@/services/datasetService';
import { toast } from 'sonner';
import { useNavigate } from 'react-router-dom';

export default function Upload() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (!selectedFile.name.match(/\.(xlsx|xls|xlsm)$/)) {
        toast.error('Please select a valid Excel file (.xlsx, .xls, .xlsm)');
        return;
      }
      setFile(selectedFile);
      setUploadResult(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      toast.error('Please select a file first');
      return;
    }

    setUploading(true);
    try {
      const result = await datasetService.uploadDataset(file);
      setUploadResult(result);
      toast.success('Dataset uploaded and indexed successfully!');
      setFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Upload failed');
      setUploadResult(null);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div data-testid="upload-page" className="p-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Upload Dataset</h1>
          <p className="text-zinc-400">Upload Excel files to create searchable knowledge bases</p>
        </div>

        <div className="bg-card border-glass rounded-xl p-8">
          <div
            className="border-2 border-dashed border-white/10 rounded-xl p-12 text-center hover:border-violet-500/50 transition-all duration-300 cursor-pointer group"
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              data-testid="file-input"
              type="file"
              accept=".xlsx,.xls,.xlsm"
              onChange={handleFileChange}
              className="hidden"
            />
            <UploadIcon className="mx-auto mb-4 text-violet-400 group-hover:scale-110 transition-transform" size={48} />
            <p className="text-lg font-medium mb-2">Click to select Excel file</p>
            <p className="text-sm text-zinc-500">Supported formats: .xlsx, .xls, .xlsm</p>
          </div>

          {file && (
            <div className="mt-6 p-4 bg-zinc-900/50 rounded-lg border border-white/5">
              <div className="flex items-center gap-3">
                <FileText className="text-violet-400" size={24} />
                <div className="flex-1">
                  <p className="text-sm font-medium">{file.name}</p>
                  <p className="text-xs text-zinc-500">{(file.size / 1024).toFixed(2)} KB</p>
                </div>
                <button
                  onClick={() => {
                    setFile(null);
                    if (fileInputRef.current) fileInputRef.current.value = '';
                  }}
                  className="text-zinc-400 hover:text-red-400"
                >
                  <XCircle size={20} />
                </button>
              </div>
            </div>
          )}

          <Button
            data-testid="upload-button"
            onClick={handleUpload}
            disabled={!file || uploading}
            className="w-full mt-6 bg-violet-600 hover:bg-violet-700 shadow-[0_0_15px_-3px_rgba(124,58,237,0.4)]"
          >
            {uploading ? 'Processing...' : 'Upload & Index Dataset'}
          </Button>
        </div>

        {uploadResult && (
          <div className="mt-6 bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-6">
            <div className="flex items-start gap-3">
              <CheckCircle className="text-emerald-400 mt-1" size={24} />
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-emerald-400 mb-2">Upload Successful!</h3>
                <div className="space-y-1 text-sm text-zinc-300">
                  <p><span className="text-zinc-500">Dataset ID:</span> {uploadResult.dataset_id}</p>
                  <p><span className="text-zinc-500">Filename:</span> {uploadResult.filename}</p>
                  <p><span className="text-zinc-500">Rows:</span> {uploadResult.num_rows}</p>
                  <p><span className="text-zinc-500">Columns:</span> {uploadResult.num_columns}</p>
                </div>
                <Button
                  onClick={() => navigate('/query')}
                  className="mt-4 bg-emerald-600 hover:bg-emerald-700"
                  size="sm"
                >
                  Start Querying
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}