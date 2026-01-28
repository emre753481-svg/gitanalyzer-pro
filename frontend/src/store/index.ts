// Zustand store for state management
import { create } from 'zustand';
import type {
  AnalysisResponse,
  AnalysisStatusResponse,
  AnalysisResults,
} from '@/types';

interface AppState {
  // Current analysis
  currentAnalysis: AnalysisResponse | null;
  analysisStatus: AnalysisStatusResponse | null;
  analysisResults: AnalysisResults | null;

  // Loading states
  isSubmitting: boolean;
  isLoadingStatus: boolean;
  isLoadingResults: boolean;

  // Error state
  error: string | null;

  // Actions
  setCurrentAnalysis: (analysis: AnalysisResponse | null) => void;
  setAnalysisStatus: (status: AnalysisStatusResponse | null) => void;
  setAnalysisResults: (results: AnalysisResults | null) => void;
  setIsSubmitting: (value: boolean) => void;
  setIsLoadingStatus: (value: boolean) => void;
  setIsLoadingResults: (value: boolean) => void;
  setError: (error: string | null) => void;
  resetState: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  // Initial state
  currentAnalysis: null,
  analysisStatus: null,
  analysisResults: null,
  isSubmitting: false,
  isLoadingStatus: false,
  isLoadingResults: false,
  error: null,

  // Actions
  setCurrentAnalysis: (analysis) => set({ currentAnalysis: analysis }),
  setAnalysisStatus: (status) => set({ analysisStatus: status }),
  setAnalysisResults: (results) => set({ analysisResults: results }),
  setIsSubmitting: (value) => set({ isSubmitting: value }),
  setIsLoadingStatus: (value) => set({ isLoadingStatus: value }),
  setIsLoadingResults: (value) => set({ isLoadingResults: value }),
  setError: (error) => set({ error }),
  resetState: () =>
    set({
      currentAnalysis: null,
      analysisStatus: null,
      analysisResults: null,
      isSubmitting: false,
      isLoadingStatus: false,
      isLoadingResults: false,
      error: null,
    }),
}));
