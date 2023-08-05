from emforceapisdk.youtube import Youtube

youtube = Youtube(developer_key="AIzaSyBfANAzt25PT8GQPzmnmZKXtLeaZB8D59s")

# search_data = youtube.search("백종원", max_result=50)
# print("search_data videos count : ", len(search_data['videos']))
# print("search_data channels count : ", len(search_data['channels']))
# print("search_data playlists count : ", len(search_data['playlists']))
#
# print(search_data['channels'])

data = youtube.most_popular_video_list()
print(data)