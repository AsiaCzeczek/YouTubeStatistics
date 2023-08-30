TABLE_NAME = 'TableName'

videos_request = (f"videos?part=id,statistics,snippet,contentDetails,"
            f"liveStreamingDetails,localizations,player,recordingDetails,status,"
            f"topicDetails&chart=mostPopular") 

def videos_rows(videos_response):
    return [
        { 
            TABLE_NAME: 'Video',
            'VideoId' : item['id'],
            'PublishDate' : item['snippet']['publishedAt'],
            'ChannelId' : item['snippet']['channelId'],
            'Title': item['snippet']['title'],
            'Tags': ",".join(item['snippet']['tags']) if 'tags' in item['snippet'] else None,
            'CategoryId': item['snippet']['categoryId']
        } 
        for item in videos_response['items']]

def statistic_rows(videos_response, datetime):
    return [
        {
            TABLE_NAME: 'VideoStatistic',
            'VideoId': item['id'],
            'Datetime': datetime,
            'ViewCount': item['statistics']['viewCount'],
            'LikeCount': item['statistics']['likeCount'],
            'FavoriteCount': item['statistics']['favoriteCount'],
            'CommentCount': item['statistics']['commentCount']
        }
        for item in videos_response['items']]   
    
