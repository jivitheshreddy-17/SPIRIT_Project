import webbrowser
import urllib.parse

def perform_web_search(command_text):
    """Searches Google for the requested query or opens a specific website."""
    
    words = command_text.split()
    
    # ACTION 1: Open a specific website
    if "open" in command_text:
        # Pre-configured fast-launch sites
        websites = {
            "github": "https://github.com",
            "leetcode": "https://leetcode.com",
            "codeforces": "https://codeforces.com",
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com"
        }
        
        # Check if the requested site is in our fast-launch dictionary
        for site, url in websites.items():
            if site in command_text:
                webbrowser.open(url)
                return f"Opening {site}."
        
        # Fallback: If it's a site not in the dictionary, try to guess the .com
        if "open" in words:
            idx = words.index("open")
            if idx + 1 < len(words):
                site_name = words[idx+1]
                webbrowser.open(f"https://www.{site_name}.com")
                return f"Opening {site_name}."

    # ACTION 2: Perform a Google Search
    elif "search" in command_text:
        # Strip out the command words to isolate the actual search query
        query = command_text.replace("search", "").replace("google", "").replace("for", "").strip()
        
        if query:
            # Format the string so it works safely in a URL (e.g., handles spaces)
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            webbrowser.open(search_url)
            return f"Here is what I found for {query}."
        else:
            return "What would you like me to search for?"
            
    return "I couldn't process that web request."