import sys
from urllib.parse import urlparse, parse_qs

def get_youtube_vid_ids(query_pharase):
    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")
        sys.exit(1)

    # Search for YouTube videos about cryptocurrency
    query = f"{query_pharase} site:youtube.com"

    video_ids = []
    for j in search(query, tld="com", num=10, stop=10, pause=2):
        # Parse the URL to extract the video ID
        url_data = urlparse(j)
        if url_data.hostname and 'youtube.com' in url_data.hostname and '/watch' in url_data.path:
            query_parameters = parse_qs(url_data.query)
            video_id = query_parameters.get('v')
            if video_id:
                video_ids.append(video_id[0])
    return video_ids
