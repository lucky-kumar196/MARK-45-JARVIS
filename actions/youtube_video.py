"""
actions/youtube_video.py — YouTube search and playback action.
"""
import urllib.parse
import webbrowser

def youtube_action(parameters: dict, player=None, session_memory=None) -> str:
    query = parameters.get("query") or parameters.get("video_name") or parameters.get("search", "")
    if not query or not str(query).strip():
        return "Sir, please provide the name of the video or song you would like to play."

    query = str(query).strip()
    
    # Direct video URL or search query
    if query.startswith("http://") or query.startswith("https://"):
        url = query
    else:
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(query)}"

    try:
        webbrowser.open(url)
    except Exception as e:
        return f"Sir, failed to open YouTube: {e}"

    msg = f"Playing '{query}' on YouTube, sir."
    if player and hasattr(player, "write_log"):
        player.write_log(f"MEDIA: {msg}")
    return msg

TOOL = {
    "name": "youtube_video",
    "description": "Searches and plays a video or music on YouTube.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "query": {
                "type": "STRING",
                "description": "The video title, topic, or song to play on YouTube"
            }
        },
        "required": ["query"]
    },
    "handler": youtube_action,
}
