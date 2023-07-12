import requests
import os
from pyyoutube import Api
import random
import pandas as pd
import sqlalchemy as db

class TrendingVideos:

    def __init__(self, api_key):
        self.api = Api(api_key=f"{api_key}")
        self.chartedVideos = []
        self.engine = db.create_engine('sqlite:///youtube_most_popular.db')
        self.random_regions = []

    def get_channel_statistics(self, channel_id):
        info = self.api.get_channel_info(channel_id=f"{channel_id}")
        return info.items[0].to_dict()
    
    def get_video_information(self):
        video_list = []
        for video in self.chartedVideos:
            info = {}
            info["title"] = video.snippet.localized.title
            info["channel"] = video.snippet.channelTitle	
            info["description"] = video.snippet.localized.description
            info["viewCount"] = video.statistics.viewCount
            info["link"] = video.id
            video_list.append(info)
        return video_list
    
    def display_chart(self, videos):
        print("Trending Videos:")
        print("----------------")
        for i, video in enumerate(videos):
            info = self.get_video_information(video)
            print(f"Video {i+1}:")
            print(f"Title: {info['title']}")
            print(f"Channel: {info['channel']}")
            print(f"Description: {info['description']}")
            print(f"View Count: {info['viewCount']}")
            print(f"Region: {info['region']}")
            print(f"Link: {info['link']}")
            print("-" * 50)
    
    def store_video_information(self):
        video_data = []
        for video in self.chartedVideos:
            info = self.get_video_information(video)
            video_data.append(info)
        df = pd.DataFrame(video_data)
        df.to_sql('video_information', con=self.engine, if_exists='replace', index=False)
        with self.engine.connect() as connection:
            query_result = connection.execute(db.text("SELECT * FROM video_information;")).fetchall()
            print(pd.DataFrame(query_result))
    
    def get_most_popular_specific(self,country,num):
        video_by_chart = self.api.get_videos_by_chart(chart="mostPopular", region_code="US", count=num)
        for video in video_by_chart.items:
            self.chartedVideos.append(video)
        return self.chartedVideos
    
    def get_most_popular_random(self, num_videos):
        response = self.api.get_i18n_regions(parts=['snippet']).items
        regions = []
        for region in response:
            regions.append(region.snippet.gl)
        i = 0
        while i < num_videos:
            choice = random.choices(regions, k=1)
            if choice in self.random_regions:
                continue
            else:
                self.random_regions.append(choice)
                i += 1
        if "LY" not in self.random_regions:
            self.random_regions[len(self.random_regions)-1] = ["LY"]
        for region in self.random_regions:
            video_by_chart = self.api.get_videos_by_chart(chart="mostPopular", region_code=region, count=1)
            self.chartedVideos.append(video_by_chart.items[0])
        return self.chartedVideos

