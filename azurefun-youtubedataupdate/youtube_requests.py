def videos_request(videos_count):
    return (f"videos?part=id,statistics,snippet,contentDetails,"
            f"liveStreamingDetails,localizations,player,recordingDetails,status,"
            f"topicDetails&chart=mostPopular&maxResults={videos_count}") 

def videos_dictionaries(response):
    return [{ 
            'TableName': 'Videos',
            'Name': response["items"][0]["snippet"]["title"][:50],
            'Likes': response["items"][0]["statistics"]["likeCount"]
        }]