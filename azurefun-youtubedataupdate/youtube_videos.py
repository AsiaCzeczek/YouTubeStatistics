import re


def videos_request(max_results, country_code, api_key):
    return f"https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet,contentDetails,status&chart=mostPopular&maxResults={max_results}&regionCode={country_code}&key={api_key}"


def videos_rows(videos_response):
    return [
        { 
            'TableName': 'Video',
            'VideoId': item['id'],
            'PublishDate': item['snippet']['publishedAt'],
            'ChannelId': item['snippet']['channelId'] if 'channelId' in item['snippet'] else None,
            'Title': item['snippet']['title'],
            'Tags': ",".join(item['snippet']['tags']) if 'tags' in item['snippet'] else None,
            'CategoryId': item['snippet']['categoryId'] if 'categoryId' in item['snippet'] else None,
            'DefaultLanguage': item['snippet']['defaultLanguage'] if 'defaultLanguage' in item['snippet'] else None,
            'DurationInMin': convert_to_minutes(item['contentDetails']['duration']),
            'HdOrSd': item['contentDetails']['definition'] if 'definition' in item['contentDetails'] else None,
            'HasCaption': item['contentDetails']['caption'] if 'caption' in item['contentDetails'] else None,
            'IsLicensed': item['contentDetails']['licensedContent'] if 'licensedContent' in item['contentDetails'] else None,
            'IsEmbeddable': item['status']['embeddable'] if 'embeddable' in item['status'] else None,
            'IsForKids': item['status']['madeForKids'] if 'madeForKids' in item['status'] else None
        }
        for item in videos_response['items']]


def statistic_rows(videos_response, datetime, country_code):
    return [
        {
            'TableName': 'VideoStatistic',
            'VideoId': item['id'],
            'Datetime': datetime,
            'ViewCount': item['statistics']['viewCount'] if 'viewCount' in item['statistics'] else None,
            'LikeCount': item['statistics']['likeCount'] if 'likeCount' in item['statistics'] else None,
            'FavoriteCount': item['statistics']['favoriteCount'] if 'favoriteCount' in item['statistics'] else None,
            'CommentCount': item['statistics']['commentCount'] if 'commentCount' in item['statistics'] else None,
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
