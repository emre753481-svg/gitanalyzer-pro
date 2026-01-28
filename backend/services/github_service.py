"""
GitHub API service for repository analysis
"""
import httpx
from typing import Dict, Any, List, Optional
from core.config import settings
from core.logger import logger
from core.exceptions import GitHubAPIException


class GitHubService:
    """Service for interacting with GitHub API"""
    
    def __init__(self, token: str):
        """
        Initialize GitHub service
        
        Args:
            token: GitHub personal access token
        """
        self.token = token
        self.base_url = settings.GITHUB_API_URL
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
    
    async def get_repository_info(self, owner: str, repo: str) -> Dict[str, Any]:
        """
        Get basic repository information
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            Repository information dictionary
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}",
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch repository info: {e}")
            raise GitHubAPIException(f"Failed to fetch repository: {str(e)}")
    
    async def get_repository_tree(self, owner: str, repo: str, branch: str = "main") -> List[Dict[str, Any]]:
        """
        Get repository file tree
        
        Args:
            owner: Repository owner
            repo: Repository name
            branch: Branch name (default: main)
            
        Returns:
            List of files and directories
        """
        try:
            async with httpx.AsyncClient() as client:
                # Get the latest commit SHA
                response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}/git/ref/heads/{branch}",
                    headers=self.headers,
                    timeout=30.0
                )
                
                if response.status_code == 404:
                    # Try master branch if main doesn't exist
                    response = await client.get(
                        f"{self.base_url}/repos/{owner}/{repo}/git/ref/heads/master",
                        headers=self.headers,
                        timeout=30.0
                    )
                
                response.raise_for_status()
                commit_sha = response.json()["object"]["sha"]
                
                # Get the tree
                response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}/git/trees/{commit_sha}?recursive=1",
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()["tree"]
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch repository tree: {e}")
            raise GitHubAPIException(f"Failed to fetch repository tree: {str(e)}")
    
    async def get_file_content(self, owner: str, repo: str, path: str) -> str:
        """
        Get file content from repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            path: File path
            
        Returns:
            File content as string
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}/contents/{path}",
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                
                import base64
                content = response.json()["content"]
                return base64.b64decode(content).decode("utf-8")
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch file content: {e}")
            raise GitHubAPIException(f"Failed to fetch file content: {str(e)}")
        except Exception as e:
            logger.error(f"Failed to decode file content: {e}")
            raise GitHubAPIException(f"Failed to decode file content: {str(e)}")
    
    async def get_readme(self, owner: str, repo: str) -> Optional[str]:
        """
        Get repository README content
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            README content or None
        """
        readme_files = ["README.md", "readme.md", "README", "README.txt"]
        
        for readme_file in readme_files:
            try:
                return await self.get_file_content(owner, repo, readme_file)
            except GitHubAPIException:
                continue
        
        return None
    
    async def get_languages(self, owner: str, repo: str) -> Dict[str, int]:
        """
        Get repository languages
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            Dictionary of languages and their bytes count
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}/languages",
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch languages: {e}")
            raise GitHubAPIException(f"Failed to fetch languages: {str(e)}")
    
    async def get_commits(self, owner: str, repo: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get repository commits
        
        Args:
            owner: Repository owner
            repo: Repository name
            limit: Number of commits to fetch
            
        Returns:
            List of commits
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}/commits",
                    headers=self.headers,
                    params={"per_page": limit},
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch commits: {e}")
            raise GitHubAPIException(f"Failed to fetch commits: {str(e)}")
    
    async def get_contributors(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        """
        Get repository contributors
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            List of contributors
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}/contributors",
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch contributors: {e}")
            raise GitHubAPIException(f"Failed to fetch contributors: {str(e)}")
    
    async def analyze_repository(self, owner: str, repo: str) -> Dict[str, Any]:
        """
        Comprehensive repository analysis
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            Complete repository analysis data
        """
        logger.info(f"Starting comprehensive analysis for {owner}/{repo}")
        
        try:
            # Gather all information concurrently
            repo_info = await self.get_repository_info(owner, repo)
            file_tree = await self.get_repository_tree(owner, repo)
            languages = await self.get_languages(owner, repo)
            readme = await self.get_readme(owner, repo)
            commits = await self.get_commits(owner, repo, limit=50)
            contributors = await self.get_contributors(owner, repo)
            
            analysis_data = {
                "repository": repo_info,
                "file_tree": file_tree,
                "languages": languages,
                "readme": readme,
                "commits": commits[:10],  # Last 10 commits
                "contributors": contributors,
                "statistics": {
                    "total_files": len([f for f in file_tree if f["type"] == "blob"]),
                    "total_dirs": len([f for f in file_tree if f["type"] == "tree"]),
                    "total_commits": len(commits),
                    "total_contributors": len(contributors),
                    "stars": repo_info.get("stargazers_count", 0),
                    "forks": repo_info.get("forks_count", 0),
                    "open_issues": repo_info.get("open_issues_count", 0),
                }
            }
            
            logger.info(f"Successfully analyzed {owner}/{repo}")
            return analysis_data
            
        except Exception as e:
            logger.error(f"Failed to analyze repository: {e}")
            raise GitHubAPIException(f"Failed to analyze repository: {str(e)}")


def parse_github_url(url: str) -> tuple[str, str]:
    """
    Parse GitHub URL to extract owner and repo
    
    Args:
        url: GitHub repository URL
        
    Returns:
        Tuple of (owner, repo)
    """
    # Remove trailing slash and .git
    url = url.rstrip("/").rstrip(".git")
    
    # Extract owner and repo from URL
    parts = url.split("/")
    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL format")
    
    repo = parts[-1]
    owner = parts[-2]
    
    return owner, repo
