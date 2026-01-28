"""
Export service for generating PDF, Markdown, and JSON outputs
"""
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any
from core.config import settings
from core.logger import logger
from core.exceptions import ExportException
from models.schemas import AnalysisResults, ExportFormat


class ExportService:
    """Service for exporting analysis results in different formats"""
    
    def __init__(self):
        """Initialize export service"""
        self.results_dir = Path(settings.ANALYSIS_RESULTS_DIR)
        self.results_dir.mkdir(parents=True, exist_ok=True)
    
    async def export_to_json(self, analysis_id: str, results: AnalysisResults) -> Path:
        """
        Export analysis results to JSON
        
        Args:
            analysis_id: Analysis ID
            results: Analysis results
            
        Returns:
            Path to exported file
        """
        try:
            output_path = self.results_dir / f"{analysis_id}.json"
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(results.model_dump(), f, indent=2, default=str)
            
            logger.info(f"Exported results to JSON: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to export to JSON: {e}")
            raise ExportException(f"Failed to export to JSON: {str(e)}")
    
    async def export_to_markdown(
        self,
        analysis_id: str,
        results: AnalysisResults,
        include_diagrams: bool = True
    ) -> Path:
        """
        Export analysis results to Markdown
        
        Args:
            analysis_id: Analysis ID
            results: Analysis results
            include_diagrams: Whether to include diagrams
            
        Returns:
            Path to exported file
        """
        try:
            output_path = self.results_dir / f"{analysis_id}.md"
            
            markdown_content = self._generate_markdown(results, include_diagrams)
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            
            logger.info(f"Exported results to Markdown: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to export to Markdown: {e}")
            raise ExportException(f"Failed to export to Markdown: {str(e)}")
    
    async def export_to_pdf(
        self,
        analysis_id: str,
        results: AnalysisResults,
        include_diagrams: bool = True
    ) -> Path:
        """
        Export analysis results to PDF
        
        Args:
            analysis_id: Analysis ID
            results: Analysis results
            include_diagrams: Whether to include diagrams
            
        Returns:
            Path to exported file
        """
        try:
            # First generate markdown
            markdown_path = await self.export_to_markdown(analysis_id, results, include_diagrams)
            
            output_path = self.results_dir / f"{analysis_id}.pdf"
            
            # Convert markdown to PDF using markdown2pdf or weasyprint
            # This is a simplified version - in production, use proper PDF generation library
            try:
                import markdown
                from weasyprint import HTML, CSS
                
                with open(markdown_path, "r", encoding="utf-8") as f:
                    md_content = f.read()
                
                # Convert markdown to HTML
                html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
                
                # Add CSS styling
                styled_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
                        h2 {{ color: #34495e; margin-top: 30px; }}
                        h3 {{ color: #7f8c8d; }}
                        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
                        pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
                        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                        th {{ background-color: #3498db; color: white; }}
                    </style>
                </head>
                <body>
                    {html_content}
                </body>
                </html>
                """
                
                # Generate PDF
                HTML(string=styled_html).write_pdf(output_path)
                
            except ImportError:
                logger.warning("PDF generation libraries not installed. Creating placeholder PDF.")
                # Fallback: copy markdown as text file with .pdf extension (not ideal but works)
                import shutil
                shutil.copy(markdown_path, output_path)
            
            logger.info(f"Exported results to PDF: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to export to PDF: {e}")
            raise ExportException(f"Failed to export to PDF: {str(e)}")
    
    def _generate_markdown(self, results: AnalysisResults, include_diagrams: bool) -> str:
        """Generate markdown content from analysis results"""
        
        md_parts = []
        
        # Header
        md_parts.append(f"# GitAnalyzer Pro - Analysis Report\n")
        md_parts.append(f"**Repository:** {results.repository_url}\n")
        md_parts.append(f"**Analyzed At:** {results.analyzed_at}\n")
        md_parts.append(f"**Analysis ID:** {results.analysis_id}\n\n")
        md_parts.append("---\n\n")
        
        # Scope Document
        if results.scope_document:
            md_parts.append("## 📋 Project Scope Document\n\n")
            scope = results.scope_document
            md_parts.append(f"### Project Overview\n{scope.project_overview}\n\n")
            md_parts.append(f"### Objectives\n")
            for obj in scope.objectives:
                md_parts.append(f"- {obj}\n")
            md_parts.append("\n")
            
            md_parts.append(f"### In Scope\n")
            for item in scope.scope_in:
                md_parts.append(f"- ✅ {item}\n")
            md_parts.append("\n")
            
            md_parts.append(f"### Out of Scope\n")
            for item in scope.scope_out:
                md_parts.append(f"- ❌ {item}\n")
            md_parts.append("\n")
        
        # Architecture
        if results.architecture:
            md_parts.append("## 🏗️ System Architecture\n\n")
            arch = results.architecture
            md_parts.append(f"{arch.system_architecture}\n\n")
            
            md_parts.append("### Technology Stack\n\n")
            for category, techs in arch.technology_stack.items():
                md_parts.append(f"**{category.title()}:**\n")
                for tech in techs:
                    md_parts.append(f"- {tech}\n")
                md_parts.append("\n")
            
            if include_diagrams:
                if arch.component_diagram:
                    md_parts.append("### Component Diagram\n\n")
                    md_parts.append(f"```plantuml\n{arch.component_diagram}\n```\n\n")
        
        # Requirements
        if results.requirements:
            md_parts.append("## 📝 Requirements\n\n")
            reqs = results.requirements
            
            md_parts.append("### Functional Requirements\n\n")
            for idx, req in enumerate(reqs.functional_requirements, 1):
                md_parts.append(f"{idx}. **{req.get('title', 'Requirement')}**\n")
                md_parts.append(f"   {req.get('description', '')}\n\n")
            
            md_parts.append("### User Stories\n\n")
            for story in reqs.user_stories:
                md_parts.append(f"- As a **{story.get('role', 'user')}**, ")
                md_parts.append(f"I want to **{story.get('action', '')}**, ")
                md_parts.append(f"so that **{story.get('benefit', '')}**\n")
        
        # Business Analysis
        if results.business_analysis:
            md_parts.append("## 💼 Business Analysis\n\n")
            biz = results.business_analysis
            
            if biz.swot_analysis:
                md_parts.append("### SWOT Analysis\n\n")
                for category, items in biz.swot_analysis.items():
                    md_parts.append(f"**{category}:**\n")
                    for item in items:
                        md_parts.append(f"- {item}\n")
                    md_parts.append("\n")
        
        # Reports
        if results.reports:
            md_parts.append("## 📊 Code Quality Report\n\n")
            report = results.reports
            
            md_parts.append(f"### Quality Score: {report.code_quality_score}/100\n\n")
            
            if report.recommendations:
                md_parts.append("### Recommendations\n\n")
                for idx, rec in enumerate(report.recommendations, 1):
                    md_parts.append(f"{idx}. {rec}\n")
        
        md_parts.append("\n---\n")
        md_parts.append(f"\n*Generated by GitAnalyzer Pro on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        return "".join(md_parts)
    
    def get_file_size(self, file_path: Path) -> int:
        """Get file size in bytes"""
        return file_path.stat().st_size if file_path.exists() else 0
    
    def generate_download_url(self, analysis_id: str, format: ExportFormat) -> str:
        """Generate download URL for exported file"""
        return f"/api/download/{analysis_id}/{format.value}"
