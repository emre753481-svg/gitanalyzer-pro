// TypeScript types for GitAnalyzer Pro

export enum AnalysisStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed',
}

export enum ExportFormat {
  PDF = 'pdf',
  MARKDOWN = 'markdown',
  JSON = 'json',
}

export enum AnalyzerType {
  SCOPE = 'scope',
  UML = 'uml',
  BPMN = 'bpmn',
  FLOW = 'flow',
  BUSINESS = 'business',
  REQUIREMENTS = 'requirements',
  ARCHITECTURE = 'architecture',
  REPORTS = 'reports',
}

export interface AnalysisRequest {
  repository_url: string;
  github_token: string;
  analyzers?: AnalyzerType[];
  ai_provider?: string;
}

export interface AnalysisResponse {
  analysis_id: string;
  status: AnalysisStatus;
  created_at: string;
  repository_url: string;
}

export interface AnalysisStatusResponse {
  analysis_id: string;
  status: AnalysisStatus;
  progress_percentage: number;
  current_step: string | null;
  started_at: string | null;
  completed_at: string | null;
  error_message: string | null;
}

export interface ScopeDocument {
  project_overview: string;
  objectives: string[];
  scope_in: string[];
  scope_out: string[];
  assumptions: string[];
  constraints: string[];
  deliverables: string[];
}

export interface UMLDiagrams {
  use_case_diagram: string;
  class_diagram: string;
  sequence_diagrams: Array<{ name: string; diagram: string }>;
  activity_diagrams: Array<{ name: string; diagram: string }>;
}

export interface BPMNDiagrams {
  business_processes: Array<{
    name: string;
    description: string;
    steps: string[];
  }>;
  process_flows: string[];
}

export interface FlowDiagrams {
  user_journey_maps: Array<{
    persona: string;
    journey: string;
    touchpoints: string[];
    pain_points: string[];
    opportunities: string[];
  }>;
  data_flow_diagrams: string[];
  system_flow: string;
}

export interface BusinessAnalysis {
  swot_analysis: {
    [key: string]: string[];
  };
  roi_analysis: Record<string, any>;
  stakeholder_analysis: Array<Record<string, string>>;
  market_analysis: Record<string, any>;
}

export interface Requirements {
  functional_requirements: Array<Record<string, string>>;
  non_functional_requirements: Array<Record<string, string>>;
  user_stories: Array<Record<string, string>>;
  acceptance_criteria: Array<Record<string, string>>;
}

export interface Architecture {
  system_architecture: string;
  component_diagram: string;
  deployment_diagram: string;
  erd_diagram: string;
  api_documentation: Record<string, any>;
  technology_stack: {
    [key: string]: string[];
  };
}

export interface Reports {
  code_quality_score: number;
  code_metrics: Record<string, any>;
  technical_debt: Record<string, any>;
  security_issues: Array<Record<string, string>>;
  performance_analysis: Record<string, any>;
  recommendations: string[];
}

export interface AnalysisResults {
  analysis_id: string;
  repository_url: string;
  analyzed_at: string;
  scope_document?: ScopeDocument;
  uml_diagrams?: UMLDiagrams;
  bpmn_diagrams?: BPMNDiagrams;
  flow_diagrams?: FlowDiagrams;
  business_analysis?: BusinessAnalysis;
  requirements?: Requirements;
  architecture?: Architecture;
  reports?: Reports;
}

export interface ExportResponse {
  download_url: string;
  file_size_bytes: number;
  format: ExportFormat;
  expires_at: string;
}
