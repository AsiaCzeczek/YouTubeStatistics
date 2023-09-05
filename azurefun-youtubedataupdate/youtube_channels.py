
def channels_request(channels_ids, max_results, api_key):
    comma_separated_ids = ','.join(channels_ids)
    return f"https://www.googleapis.com/youtube/v3/channels?part=id,statistics,snippet,status&id={comma_separated_ids}&maxResults={max_results}&key={api_key}"


def channels_rows(channels_response):
    return [
        { 
            'TableName': 'Channel',
            'ChannelId': item['id'],
            'Title': item['snippet']['title'],
            'CreatedDate': item['snippet']['publishedAt'],
            'DefaultLanguage': item['snippet']['defaultLanguage'] if 'defaultLanguage' in item['snippet'] else None,
            'Country': item['snippet']['country'] if 'country' in item['snippet'] else None,
            'IsForKids': item['status']['madeForKids'] if 'madeForKids' in item['status'] else None
        }
        for item in channels_response['items']]


def channels_statistic_rows(channels_response, datetime):
    return [
        {
            'TableName': 'ChannelStatistic',
            'ChannelId': item['id'],
            'Datetime': datetime,
            'ViewCount': item['statistics']['viewCount'],
            'CommentCount': item['statistics']['commentCount'] if 'commentCount' in item['statistics'] else None,
            'SubscriberCount': item['statistics']['subscriberCount'],
            'VideoCount': item['statistics']['videoCount']
        }
        for item in channels_response['items']]
    




