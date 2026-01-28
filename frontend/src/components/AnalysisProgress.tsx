// Analysis Progress Component
import React, { useEffect } from 'react';
import { Loader2, CheckCircle, XCircle } from 'lucide-react';
import { useAppStore } from '@/store';
import { apiService } from '@/services/api';
import { AnalysisStatus } from '@/types';

export const AnalysisProgress: React.FC = () => {
  const {
    currentAnalysis,
    analysisStatus,
    setAnalysisStatus,
  } = useAppStore();

  useEffect(() => {
    if (!currentAnalysis) return;

    const pollStatus = async () => {
      try {
        const status = await apiService.getAnalysisStatus(
          currentAnalysis.analysis_id
        );
        setAnalysisStatus(status);

        // Continue polling if still processing
        if (
          status.status === AnalysisStatus.PROCESSING ||
          status.status === AnalysisStatus.PENDING
        ) {
          setTimeout(pollStatus, 3000); // Poll every 3 seconds
        }
      } catch (error) {
        console.error('Failed to fetch status:', error);
      }
    };

    pollStatus();
  }, [currentAnalysis]);

  if (!analysisStatus) return null;

  const getStatusIcon = () => {
    switch (analysisStatus.status) {
      case AnalysisStatus.COMPLETED:
        return <CheckCircle className="w-12 h-12 text-green-500" />;
      case AnalysisStatus.FAILED:
        return <XCircle className="w-12 h-12 text-red-500" />;
      default:
        return <Loader2 className="w-12 h-12 text-primary-600 animate-spin" />;
    }
  };

  const getStatusText = () => {
    switch (analysisStatus.status) {
      case AnalysisStatus.COMPLETED:
        return 'Analysis Completed!';
      case AnalysisStatus.FAILED:
        return 'Analysis Failed';
      case AnalysisStatus.PROCESSING:
        return 'Analysis in Progress...';
      default:
        return 'Analysis Pending...';
    }
  };

  return (
    <div className="card max-w-2xl mx-auto">
      <div className="flex flex-col items-center gap-4">
        {getStatusIcon()}
        
        <h3 className="text-xl font-semibold text-gray-800">{getStatusText()}</h3>
        
        {/* Progress Bar */}
        <div className="w-full">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>{analysisStatus.current_step || 'Initializing...'}</span>
            <span>{analysisStatus.progress_percentage}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-primary-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${analysisStatus.progress_percentage}%` }}
            />
          </div>
        </div>

        {/* Error Message */}
        {analysisStatus.error_message && (
          <div className="w-full p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-sm text-red-800">{analysisStatus.error_message}</p>
          </div>
        )}

        {/* Repository Info */}
        <div className="w-full p-4 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-600">
            <strong>Repository:</strong> {currentAnalysis?.repository_url}
          </p>
          <p className="text-sm text-gray-600">
            <strong>Analysis ID:</strong> {analysisStatus.analysis_id}
          </p>
        </div>
      </div>
    </div>
  );
};
