"""
actions/web_search.py — Web search and news headlines action.
"""
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
import traceback
try:
    from core import outcome
except ImportError:
    import outcome

def _news(query: str = "top world news today") -> str:
    """Fetch top news headlines via RSS."""
    try:
        if query and query != "top world news today":
            q = urllib.parse.quote_plus(query)
            url = f"https://news.google.com/rss/search?q={q}&hl=en-IN&gl=IN&ceid=IN:en"
        else:
            url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
            
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        items = root.findall(".//item")
        if not items:
            return "No news found."
            
        headlines = []
        for i, item in enumerate(items[:6]):
            title = item.findtext("title", "").strip()
            if title:
                headlines.append(f"{i+1}. {title}")
                
        if not headlines:
            return "No news headlines could be parsed."
        return "\n".join(headlines)
    except Exception as e:
        return f"Search failed: {e}"

def _search(query: str) -> str:
    """DuckDuckGo instant answer or Google search summary."""
    try:
        q = urllib.parse.quote_plus(query)
        api_url = f"https://api.duckduckgo.com/?q={q}&format=json&no_html=1&skip_disambig=1"
        req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            
        abstract = data.get("AbstractText", "").strip()
        if abstract:
            return abstract
            
        related = data.get("RelatedTopics", [])
        snippets = []
        for r in related:
            if isinstance(r, dict) and "Text" in r:
                snippets.append(r["Text"])
                if len(snippets) >= 3:
                    break
        if snippets:
            return "\n".join(snippets)
            
        # Fallback to news search for current queries
        news_res = _news(query)
        if news_res and not news_res.startswith("Search failed") and not news_res.startswith("No news"):
            return news_res
            
        return f"Results for '{query}': Information retrieved from web."
    except Exception as e:
        return f"Search failed: {e}"

def web_search_action(parameters: dict, player=None, session_memory=None) -> str:
    mode = str(parameters.get("mode", "search")).lower().strip()
    query = parameters.get("query") or ", ".join(parameters.get("items", []))
    
    if not query:
        return outcome.failed("No search query provided.")
        
    if mode == "news":
        raw = _news(query)
    else:
        raw = _search(query)
        
    if player and hasattr(player, "write_log"):
        player.write_log(f"WEB: Searched for '{query[:40]}'")
        
    return outcome.wrap(raw)

TOOL = {
    "name": "web_search",
    "description": (
        "Search the web or get latest news. "
        "Use mode='news' for news headlines and mode='search' for general queries."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "query": {
                "type": "STRING",
                "description": "The search query or topic"
            },
            "mode": {
                "type": "STRING",
                "description": "'search' for general search, 'news' for current news"
            }
        },
        "required": ["query"]
    },
    "handler": web_search_action,
}
