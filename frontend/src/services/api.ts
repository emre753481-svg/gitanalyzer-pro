// API service for GitAnalyzer Pro
import axios from 'axios';
import type {
  AnalysisRequest,
  AnalysisResponse,
  AnalysisStatusResponse,
  AnalysisResults,
  ExportFormat,
  ExportResponse,
} from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Start analysis
  async startAnalysis(data: AnalysisRequest): Promise<AnalysisResponse> {
    const response = await api.post<AnalysisResponse>('/api/analyze', data);
    return response.data;
  },

  // Get analysis status
  async getAnalysisStatus(analysisId: string): Promise<AnalysisStatusResponse> {
    const response = await api.get<AnalysisStatusResponse>(
      `/api/analysis/${analysisId}/status`
    );
    return response.data;
  },

  // Get analysis results
  async getAnalysisResults(analysisId: string): Promise<AnalysisResults> {
    const response = await api.get<AnalysisResults>(
      `/api/analysis/${analysisId}/results`
    );
    return response.data;
  },

  // Export analysis
  async exportAnalysis(
    analysisId: string,
    format: ExportFormat,
    includeDiagrams = true
  ): Promise<ExportResponse> {
    const response = await api.post<ExportResponse>(
      `/api/export/${analysisId}/${format}`,
      null,
      {
        params: { include_diagrams: includeDiagrams },
      }
    );
    return response.data;
  },

  // Get download URL
  getDownloadUrl(analysisId: string, format: ExportFormat): string {
    return `${API_BASE_URL}/api/download/${analysisId}/${format}`;
  },
};
