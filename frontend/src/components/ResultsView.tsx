// Results View Component
import React, { useEffect, useState } from 'react';
import { FileText, FileJson, FileCode } from 'lucide-react';
import { useAppStore } from '@/store';
import { apiService } from '@/services/api';
import { ExportFormat } from '@/types';

export const ResultsView: React.FC = () => {
  const { currentAnalysis, analysisResults, setAnalysisResults } = useAppStore();
  const [activeTab, setActiveTab] = useState('scope');
  const [exporting, setExporting] = useState<ExportFormat | null>(null);

  useEffect(() => {
    if (!currentAnalysis) return;

    const fetchResults = async () => {
      try {
        const results = await apiService.getAnalysisResults(
          currentAnalysis.analysis_id
        );
        setAnalysisResults(results);
      } catch (error) {
        console.error('Failed to fetch results:', error);
      }
    };

    fetchResults();
  }, [currentAnalysis]);

  const handleExport = async (format: ExportFormat) => {
    if (!currentAnalysis) return;

    setExporting(format);
    try {
      await apiService.exportAnalysis(
        currentAnalysis.analysis_id,
        format
      );
      
      // Download file
      const downloadUrl = apiService.getDownloadUrl(
        currentAnalysis.analysis_id,
        format
      );
      window.open(downloadUrl, '_blank');
    } catch (error) {
      console.error('Export failed:', error);
    } finally {
      setExporting(null);
    }
  };

  if (!analysisResults) {
    return <div className="text-center py-8">Loading results...</div>;
  }

  const tabs = [
    { id: 'scope', label: 'Scope', visible: !!analysisResults.scope_document },
    { id: 'architecture', label: 'Architecture', visible: !!analysisResults.architecture },
    { id: 'requirements', label: 'Requirements', visible: !!analysisResults.requirements },
    { id: 'business', label: 'Business', visible: !!analysisResults.business_analysis },
    { id: 'reports', label: 'Reports', visible: !!analysisResults.reports },
  ].filter(tab => tab.visible);

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Export Buttons */}
      <div className="card">
        <h3 className="text-lg font-semibold mb-4">Export Results</h3>
        <div className="flex gap-3">
          <button
            onClick={() => handleExport(ExportFormat.PDF)}
            disabled={exporting === ExportFormat.PDF}
            className="btn btn-primary flex items-center gap-2"
          >
            <FileText className="w-4 h-4" />
            {exporting === ExportFormat.PDF ? 'Exporting...' : 'Export PDF'}
          </button>
          <button
            onClick={() => handleExport(ExportFormat.MARKDOWN)}
            disabled={exporting === ExportFormat.MARKDOWN}
            className="btn btn-secondary flex items-center gap-2"
          >
            <FileCode className="w-4 h-4" />
            {exporting === ExportFormat.MARKDOWN ? 'Exporting...' : 'Export Markdown'}
          </button>
          <button
            onClick={() => handleExport(ExportFormat.JSON)}
            disabled={exporting === ExportFormat.JSON}
            className="btn btn-secondary flex items-center gap-2"
          >
            <FileJson className="w-4 h-4" />
            {exporting === ExportFormat.JSON ? 'Exporting...' : 'Export JSON'}
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="card">
        <div className="border-b border-gray-200">
          <div className="flex gap-4">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-2 font-medium transition-colors ${
                  activeTab === tab.id
                    ? 'border-b-2 border-primary-600 text-primary-600'
                    : 'text-gray-600 hover:text-gray-800'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Tab Content */}
        <div className="mt-6">
          {activeTab === 'scope' && analysisResults.scope_document && (
            <div className="space-y-4">
              <h3 className="text-xl font-bold">Project Scope</h3>
              <div>
                <h4 className="font-semibold mb-2">Overview</h4>
                <p className="text-gray-700">{analysisResults.scope_document.project_overview}</p>
              </div>
              <div>
                <h4 className="font-semibold mb-2">Objectives</h4>
                <ul className="list-disc pl-5 space-y-1">
                  {analysisResults.scope_document.objectives.map((obj, idx) => (
                    <li key={idx} className="text-gray-700">{obj}</li>
                  ))}
                </ul>
              </div>
              <div>
                <h4 className="font-semibold mb-2">Deliverables</h4>
                <ul className="list-disc pl-5 space-y-1">
                  {analysisResults.scope_document.deliverables.map((del, idx) => (
                    <li key={idx} className="text-gray-700">{del}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {activeTab === 'architecture' && analysisResults.architecture && (
            <div className="space-y-4">
              <h3 className="text-xl font-bold">System Architecture</h3>
              <p className="text-gray-700">{analysisResults.architecture.system_architecture}</p>
              
              <div>
                <h4 className="font-semibold mb-2">Technology Stack</h4>
                {Object.entries(analysisResults.architecture.technology_stack).map(([category, techs]) => (
                  <div key={category} className="mb-3">
                    <h5 className="font-medium text-gray-800 capitalize">{category}:</h5>
                    <div className="flex flex-wrap gap-2 mt-1">
                      {techs.map((tech, idx) => (
                        <span key={idx} className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm">
                          {tech}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'requirements' && analysisResults.requirements && (
            <div className="space-y-4">
              <h3 className="text-xl font-bold">Requirements</h3>
              
              <div>
                <h4 className="font-semibold mb-3">Functional Requirements</h4>
                <div className="space-y-2">
                  {analysisResults.requirements.functional_requirements.map((req, idx) => (
                    <div key={idx} className="p-3 bg-gray-50 rounded-lg">
                      <p className="font-medium">{req.title}</p>
                      <p className="text-sm text-gray-600">{req.description}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <h4 className="font-semibold mb-3">User Stories</h4>
                <div className="space-y-2">
                  {analysisResults.requirements.user_stories.map((story, idx) => (
                    <div key={idx} className="p-3 bg-blue-50 rounded-lg">
                      <p className="text-sm">
                        As a <strong>{story.role}</strong>, I want to <strong>{story.action}</strong>,
                        so that <strong>{story.benefit}</strong>
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'business' && analysisResults.business_analysis && (
            <div className="space-y-4">
              <h3 className="text-xl font-bold">Business Analysis</h3>
              
              <div>
                <h4 className="font-semibold mb-3">SWOT Analysis</h4>
                <div className="grid grid-cols-2 gap-4">
                  {Object.entries(analysisResults.business_analysis.swot_analysis).map(([category, items]) => (
                    <div key={category} className="p-4 bg-gray-50 rounded-lg">
                      <h5 className="font-medium mb-2">{category}</h5>
                      <ul className="list-disc pl-5 space-y-1 text-sm">
                        {items.map((item, idx) => (
                          <li key={idx}>{item}</li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'reports' && analysisResults.reports && (
            <div className="space-y-4">
              <h3 className="text-xl font-bold">Code Quality Report</h3>
              
              <div className="p-6 bg-gradient-to-r from-primary-50 to-primary-100 rounded-lg">
                <div className="text-center">
                  <p className="text-sm text-gray-600">Quality Score</p>
                  <p className="text-5xl font-bold text-primary-700">
                    {analysisResults.reports.code_quality_score.toFixed(1)}
                  </p>
                  <p className="text-sm text-gray-600">out of 100</p>
                </div>
              </div>

              {analysisResults.reports.recommendations.length > 0 && (
                <div>
                  <h4 className="font-semibold mb-3">Recommendations</h4>
                  <ul className="space-y-2">
                    {analysisResults.reports.recommendations.map((rec, idx) => (
                      <li key={idx} className="flex gap-2">
                        <span className="text-primary-600">•</span>
                        <span className="text-gray-700">{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
