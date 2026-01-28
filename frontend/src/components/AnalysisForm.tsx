// Analysis Form Component
import React, { useState } from 'react';
import { GitBranch, Loader2 } from 'lucide-react';
import { apiService } from '@/services/api';
import { useAppStore } from '@/store';
import type { AnalyzerType } from '@/types';

const availableAnalyzers: { value: AnalyzerType; label: string }[] = [
  { value: 'scope' as AnalyzerType, label: 'Project Scope' },
  { value: 'uml' as AnalyzerType, label: 'UML Diagrams' },
  { value: 'bpmn' as AnalyzerType, label: 'BPMN Diagrams' },
  { value: 'flow' as AnalyzerType, label: 'Flow Diagrams' },
  { value: 'business' as AnalyzerType, label: 'Business Analysis' },
  { value: 'requirements' as AnalyzerType, label: 'Requirements' },
  { value: 'architecture' as AnalyzerType, label: 'Architecture' },
  { value: 'reports' as AnalyzerType, label: 'Code Quality Reports' },
];

export const AnalysisForm: React.FC = () => {
  const [repositoryUrl, setRepositoryUrl] = useState('');
  const [githubToken, setGithubToken] = useState('');
  const [aiProvider, setAiProvider] = useState('anthropic');
  const [selectedAnalyzers, setSelectedAnalyzers] = useState<AnalyzerType[]>([]);

  const { setCurrentAnalysis, setIsSubmitting, setError, isSubmitting } = useAppStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      const response = await apiService.startAnalysis({
        repository_url: repositoryUrl,
        github_token: githubToken,
        analyzers: selectedAnalyzers.length > 0 ? selectedAnalyzers : undefined,
        ai_provider: aiProvider,
      });

      setCurrentAnalysis(response);
    } catch (error: any) {
      setError(error.response?.data?.message || 'Failed to start analysis');
    } finally {
      setIsSubmitting(false);
    }
  };

  const toggleAnalyzer = (analyzer: AnalyzerType) => {
    setSelectedAnalyzers((prev) =>
      prev.includes(analyzer)
        ? prev.filter((a) => a !== analyzer)
        : [...prev, analyzer]
    );
  };

  return (
    <div className="card max-w-3xl mx-auto">
      <div className="flex items-center gap-3 mb-6">
        <GitBranch className="w-8 h-8 text-primary-600" />
        <h2 className="text-2xl font-bold text-gray-800">
          Start Repository Analysis
        </h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Repository URL */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            GitHub Repository URL *
          </label>
          <input
            type="url"
            value={repositoryUrl}
            onChange={(e) => setRepositoryUrl(e.target.value)}
            placeholder="https://github.com/owner/repo"
            className="input"
            required
          />
        </div>

        {/* GitHub Token */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            GitHub Access Token *
          </label>
          <input
            type="password"
            value={githubToken}
            onChange={(e) => setGithubToken(e.target.value)}
            placeholder="ghp_xxxxxxxxxxxxx"
            className="input"
            required
          />
          <p className="mt-1 text-xs text-gray-500">
            Your token is only used for this analysis and not stored.
          </p>
        </div>

        {/* AI Provider */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            AI Provider
          </label>
          <select
            value={aiProvider}
            onChange={(e) => setAiProvider(e.target.value)}
            className="input"
          >
            <option value="anthropic">Anthropic Claude</option>
            <option value="openai">OpenAI GPT</option>
          </select>
        </div>

        {/* Analyzers Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Analyzers (optional - leave empty for all)
          </label>
          <div className="grid grid-cols-2 gap-3">
            {availableAnalyzers.map((analyzer) => (
              <label
                key={analyzer.value}
                className="flex items-center gap-2 cursor-pointer"
              >
                <input
                  type="checkbox"
                  checked={selectedAnalyzers.includes(analyzer.value)}
                  onChange={() => toggleAnalyzer(analyzer.value)}
                  className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
                />
                <span className="text-sm text-gray-700">{analyzer.label}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isSubmitting}
          className="btn btn-primary w-full flex items-center justify-center gap-2"
        >
          {isSubmitting ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Starting Analysis...
            </>
          ) : (
            'Start Analysis'
          )}
        </button>
      </form>
    </div>
  );
};
