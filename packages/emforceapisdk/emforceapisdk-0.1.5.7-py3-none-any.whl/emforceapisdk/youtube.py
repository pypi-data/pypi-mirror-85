#!/usr/bin/python
from apiclient import discovery


class Youtube:
    def __init__(self, developer_key=None):
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"
        self.youtube = discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=developer_key)

    def channel_detail(self, channel_id):
        channel_detail = self.youtube.channels().list(
            id=channel_id,
            part='id,snippet,statistics,topicDetails'
        ).execute()

        check_data = channel_detail.get('items', None)

        return_data = {}

        if check_data:
            check_data = check_data[0]
            country = check_data['snippet'].get('country')

            return_data["id"] = check_data['id']
            return_data["title"] = check_data['snippet']['title']
            return_data["description"] = check_data['snippet']['description']
            return_data["publishedAt"] = check_data['snippet']['publishedAt']
            return_data["thumbnails"] = check_data['snippet']['thumbnails']
            return_data["localized"] = check_data['snippet']['localized']
            return_data["country"] = country
            return_data["viewCount"] = check_data['statistics']['viewCount']
            return_data["subscriberCount"] = check_data['statistics']['subscriberCount']
            return_data["videoCount"] = check_data['statistics']['videoCount']
            # return_data["commentCount"] = check_data['statistics']['commentCount']
            if check_data.get('topicDetails'):
                return_data["topicIds"] = check_data['topicDetails'].get('topicIds')
                return_data["topicCategories"] = check_data['topicDetails'].get('topicCategories')
            else:
                return_data["topicIds"] = []
                return_data["topicCategories"] = []


        return return_data

    def video_category_list(self, hl='ko_KR', region_code="KR"):
        res = self.youtube.videoCategories().list(
            part="id,snippet",
            hl=hl,
            regionCode=region_code
        ).execute()

        return_data = []

        items = res.get('items', None)
        for item in items:
            return_data.append({
                "id": item.get("id"),
                "etag": item.get("etag"),
                "title": item.get('snippet').get('title'),
                # "channelId": item.get('snippet').get('channelId')
            })

        return return_data

    def most_popular_video_list(self, category_id=None, max_result=50, page_token=None):
        video_list = self.youtube.videos().list(
            part='id,snippet, statistics',
            chart='mostPopular',
            regionCode='KR',
            videoCategoryId=category_id,
            pageToken=page_token,
            maxResults=max_result
        ).execute()

        return_data = []
        return_dic = {}

        pageInfo = video_list.get('pageInfo')
        prevPageToken = video_list.get('prevPageToken')
        nextPageToken = video_list.get('nextPageToken')
        pageInfo['prevPageToken'] = prevPageToken
        pageInfo['nextPageToken'] = nextPageToken

        return_dic['page_info'] = pageInfo

        for video in video_list.get("items", []):
            return_data.append({
                "id": video['id'],
                "publishedAt": video['snippet']['publishedAt'],
                "channelId": video['snippet']['channelId'],
                "channelTitle": video['snippet']['channelTitle'],
                "title": video['snippet'].get('title'),
                "description": video['snippet'].get('description'),
                "thumbnails": video['snippet'].get('thumbnails'),
                "tags": video['snippet'].get('tags'),
                "categoryId": video['snippet'].get('categoryId'),
                "liveBroadcastContent": video['snippet'].get('liveBroadcastContent'),
                "defaultAudioLanguage": video['snippet'].get('defaultAudioLanguage'),
                "viewCount": video['statistics'].get('viewCount', 0),
                "likeCount": video['statistics'].get('likeCount', 0),
                "dislikeCount": video['statistics'].get('dislikeCount', 0),
                "favoriteCount": video['statistics'].get('favoriteCount', 0),
                "commentCount": video['statistics'].get('commentCount', 0),
            })
        return_dic['data'] = return_data

        return return_dic

    def search(self, keyword, max_result=50, page_token=None):
        search_response = self.youtube.search().list(
            q=keyword,
            part="id,snippet",
            pageToken=page_token,
            maxResults=max_result
        ).execute()

        videos = []
        channels = []
        playlists = []

        pageInfo = search_response.get('pageInfo')
        prevPageToken = search_response.get('prevPageToken')
        nextPageToken = search_response.get('nextPageToken')
        pageInfo['prevPageToken'] = prevPageToken
        pageInfo['nextPageToken'] = nextPageToken

        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                videos.append({
                    "etag": search_result['etag'],
                    "vedioId": search_result["id"]["videoId"],
                    "publishedAt": search_result["snippet"]["publishedAt"],
                    "channelId": search_result["snippet"]["channelId"],
                    "title": search_result["snippet"]["title"],
                    "description": search_result["snippet"]["description"],
                    "thumbnails": search_result["snippet"]["thumbnails"],
                    "title": search_result["snippet"]["title"],
                    "thumbnails": search_result["snippet"]["thumbnails"],
                    "channelTitle": search_result["snippet"]["channelTitle"],
                    "liveBroadcastContent": search_result["snippet"]["liveBroadcastContent"],
                    "publishTime": search_result["snippet"]["publishTime"],

                })
            elif search_result["id"]["kind"] == "youtube#channel":
                channels.append({
                    "etag": search_result['etag'],
                    "channelId": search_result["id"]["channelId"],
                    "publishedAt": search_result["snippet"]["publishedAt"],
                    "title": search_result["snippet"]["title"],
                    "description": search_result["snippet"]["description"],
                    "thumbnails": search_result["snippet"]["thumbnails"],
                    "channelTitle": search_result["snippet"]["channelTitle"],
                    "liveBroadcastContent": search_result["snippet"]["liveBroadcastContent"],
                    "publishTime": search_result["snippet"]["publishTime"],
                })
            elif search_result["id"]["kind"] == "youtube#playlist":
                playlists.append({
                    "etag": search_result['etag'],
                    "playlistId": search_result["id"]["playlistId"],
                    "publishedAt": search_result["snippet"]["publishedAt"],
                    "channelId": search_result["snippet"]["channelId"],
                    "title": search_result["snippet"]["title"],
                    "description": search_result["snippet"]["description"],
                    "thumbnails": search_result["snippet"]["thumbnails"],
                    "channelTitle": search_result["snippet"]["channelTitle"],
                    "liveBroadcastContent": search_result["snippet"]["liveBroadcastContent"],
                    "publishTime": search_result["snippet"]["publishTime"],
                })

        return_data = {
            "page_info": pageInfo,
            "videos": videos,
            "channels": channels,
            "playlists": playlists
        }

        return return_data
