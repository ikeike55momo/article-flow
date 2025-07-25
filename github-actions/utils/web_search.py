"""Web search utilities using Bing Search API"""
import os
import requests
import time
from typing import List, Dict, Any, Optional
from urllib.parse import quote
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


class BingSearchAPI:
    """Wrapper for Bing Search API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("BING_SEARCH_KEY")
        if not self.api_key:
            raise ValueError("BING_SEARCH_KEY not found")
        
        self.endpoint = "https://api.bing.microsoft.com/v7.0/search"
        self.headers = {"Ocp-Apim-Subscription-Key": self.api_key}
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def search(
        self,
        query: str,
        count: int = 10,
        offset: int = 0,
        market: str = "ja-JP",
        safe_search: str = "Moderate"
    ) -> Dict[str, Any]:
        """Perform web search"""
        params = {
            "q": query,
            "count": count,
            "offset": offset,
            "mkt": market,
            "safeSearch": safe_search
        }
        
        try:
            response = requests.get(
                self.endpoint,
                headers=self.headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Bing Search API error: {e}")
            raise
    
    def search_with_priority(
        self,
        query: str,
        priority_domains: Optional[List[str]] = None,
        count: int = 20
    ) -> List[Dict[str, Any]]:
        """Search with domain priority filtering"""
        
        # Default priority domains
        if priority_domains is None:
            priority_domains = {
                "very_high": [".go.jp", ".gov"],
                "high": [".ac.jp", ".edu", "医学会", "学会"],
                "medium_high": ["協会", "団体", "nhk.or.jp", "日経"]
            }
        
        # Perform search
        results = self.search(query, count=count)
        
        # Process and rank results
        ranked_results = []
        
        if "webPages" in results and "value" in results["webPages"]:
            for result in results["webPages"]["value"]:
                url = result.get("url", "")
                priority = self._get_domain_priority(url, priority_domains)
                
                ranked_results.append({
                    "url": url,
                    "title": result.get("name", ""),
                    "snippet": result.get("snippet", ""),
                    "priority": priority,
                    "display_url": result.get("displayUrl", "")
                })
        
        # Sort by priority
        ranked_results.sort(key=lambda x: self._priority_to_score(x["priority"]), reverse=True)
        
        return ranked_results
    
    def _get_domain_priority(self, url: str, priority_domains: Dict[str, List[str]]) -> str:
        """Get priority level for a URL"""
        url_lower = url.lower()
        
        for priority, domains in priority_domains.items():
            for domain in domains:
                if domain.lower() in url_lower:
                    return priority
        
        return "medium"
    
    def _priority_to_score(self, priority: str) -> int:
        """Convert priority to numeric score"""
        scores = {
            "very_high": 4,
            "high": 3,
            "medium_high": 2,
            "medium": 1,
            "low": 0
        }
        return scores.get(priority, 1)


class ParallelSearcher:
    """Parallel search execution"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.searcher = BingSearchAPI(api_key)
    
    async def search_parallel(
        self,
        queries: List[str],
        batch_size: int = 5
    ) -> List[List[Dict[str, Any]]]:
        """Execute searches in parallel batches"""
        # For now, implement sequential search
        # TODO: Implement proper async parallel search
        
        results = []
        for i in range(0, len(queries), batch_size):
            batch = queries[i:i + batch_size]
            batch_results = []
            
            for query in batch:
                logger.info(f"Searching: {query}")
                try:
                    search_results = self.searcher.search_with_priority(query)
                    batch_results.append(search_results)
                except Exception as e:
                    logger.error(f"Search failed for '{query}': {e}")
                    batch_results.append([])
                
                # Rate limiting
                time.sleep(0.5)
            
            results.extend(batch_results)
        
        return results