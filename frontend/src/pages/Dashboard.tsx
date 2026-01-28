// Dashboard Page
import React from 'react';
import { useAppStore } from '@/store';
import { AnalysisForm } from '@/components/AnalysisForm';
import { AnalysisProgress } from '@/components/AnalysisProgress';
import { ResultsView } from '@/components/ResultsView';
import { AnalysisStatus } from '@/types';

export const Dashboard: React.FC = () => {
  const { currentAnalysis, analysisStatus, error, resetState } = useAppStore();

  const renderContent = () => {
    // Show error if exists
    if (error) {
      return (
        <div className="max-w-2xl mx-auto">
          <div className="card bg-red-50 border border-red-200">
            <h3 className="text-lg font-semibold text-red-800 mb-2">Error</h3>
            <p className="text-red-700">{error}</p>
            <button
              onClick={resetState}
              className="btn btn-primary mt-4"
            >
              Start New Analysis
            </button>
          </div>
        </div>
      );
    }

    // Show results if completed
    if (analysisStatus?.status === AnalysisStatus.COMPLETED) {
      return (
        <>
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-800">Analysis Results</h2>
            <button
              onClick={resetState}
              className="btn btn-secondary"
            >
              New Analysis
            </button>
          </div>
          <ResultsView />
        </>
      );
    }

    // Show progress if processing
    if (currentAnalysis && analysisStatus) {
      return <AnalysisProgress />;
    }

    // Show form by default
    return <AnalysisForm />;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">G</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-800">GitAnalyzer Pro</h1>
              <p className="text-sm text-gray-600">
                AI-Powered Repository Documentation
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {renderContent()}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="container mx-auto px-4 py-6 text-center text-sm text-gray-600">
          <p>GitAnalyzer Pro &copy; 2024 - Enterprise Repository Analysis Platform</p>
        </div>
      </footer>
    </div>
  );
};
