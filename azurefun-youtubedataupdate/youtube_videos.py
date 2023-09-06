import re


def videos_request(max_results, country_code, api_key):
    return f"https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet,contentDetails,status&chart=mostPopular&maxResults={max_results}&regionCode={country_code}&key={api_key}"


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
            'DefaultLanguage': item['snippet']['defaultLanguage'] if 'defaultLanguage' in item['snippet'] else None,
            'DurationInMin': convert_to_minutes(item['contentDetails']['duration']),
            'HdOrSd': item['contentDetails']['definition'],
            'HasCaption': item['contentDetails']['caption'],
            'IsLicensed': item['contentDetails']['licensedContent'],
            'IsEmbeddable': item['status']['embeddable'],
            'IsForKids': item['status']['madeForKids'] if 'madeForKids' in item['status'] else None
        }
        for item in videos_response['items']]


def statistic_rows(videos_response, datetime, country_code):
    return [
        {
            'TableName': 'VideoStatistic',
            'VideoId': item['id'],
            'Datetime': datetime,
            'ViewCount': item['statistics']['viewCount'],
            'LikeCount': item['statistics']['likeCount'],
            'FavoriteCount': item['statistics']['favoriteCount'],
            'CommentCount': item['statistics']['commentCount'],
            'StatisticInCountry': country_code
        }
        for item in videos_response['items']]   
    

def convert_to_minutes(you_tube_duration):
    numbers = [int(s) for s in re.findall(r'\d+', you_tube_duration)]
    numbers.reverse()
    minutes_1 = 1 if numbers[0] > 0 else 0
    minutes_2 = numbers[1] if len(numbers) > 1 else 0
    minutes_3 = numbers[2] * 60 if len(numbers) > 2 else 0
    minutes_4 = numbers[3] * 24 * 60 if len(numbers) > 3 else 0
    return minutes_1 + minutes_2 + minutes_3 + minutes_4
