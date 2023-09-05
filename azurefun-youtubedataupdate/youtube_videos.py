import re


videos_request = "videos?part=id,statistics,snippet,contentDetails,status&chart=mostPopular"


def videos_rows(videos_response):
    return [
        { 
            'TableName': 'Video',
            'VideoId': item['id'],
            'PublishDate': item['snippet']['publishedAt'],
            'ChannelId': item['snippet']['channelId'],
            'Title': item['snippet']['title'],
            'Tags': ",".join(item['snippet']['tags']) if 'tags' in item['snippet'] else None,
            'CategoryId': item['snippet']['categoryId'],
            'DefaultLanguage': item['snippet']['defaultLanguage'],
            'DurationInMin': convert_to_minutes(item['contentDetails']['duration']),
            'HdOrSd': item['contentDetails']['definition'],
            'HasCaption': item['contentDetails']['caption'],
            'IsLicensed': item['contentDetails']['licensedContent'],
            'IsEmbeddable': item['status']['embeddable'],
            'IsForKids': item['status']['madeForKids'],
        }
        for item in videos_response['items']]


def statistic_rows(videos_response, datetime):
    return [
        {
            'TableName': 'VideoStatistic',
            'VideoId': item['id'],
            'Datetime': datetime,
            'ViewCount': item['statistics']['viewCount'],
            'LikeCount': item['statistics']['likeCount'],
            'FavoriteCount': item['statistics']['favoriteCount'],
            'CommentCount': item['statistics']['commentCount']
        }
        for item in videos_response['items']]   
    

def convert_to_minutes(you_tube_duration):
    numbers = [int(s) for s in re.findall(r'\d+', you_tube_duration)]
    numbers.reverse()
    minutes_1 = 1 if numbers[0] > 0 else 0
    minutes_2 = numbers[1]
    minutes_3 = numbers[2] * 60 if len(numbers) > 2 else 0
    minutes_4 = numbers[3] * 24 * 60 if len(numbers) > 3 else 0
    return minutes_1 + minutes_2 + minutes_3 + minutes_4
