import requests
import os
from pyyoutube import Api
import random
import pandas as pd
import sqlalchemy as db
import wikipediaapi
#import translators as ts ts.google

class TrendingVideos:

    def __init__(self, api_key):
        self.api = Api(api_key=f"{api_key}")
        self.chartedVideos = []
        self.engine = db.create_engine('sqlite:///youtube_most_popular.db')
        self.wiki = wikipediaapi.Wikipedia('YoutubeApiProject (jcruz2@oberlin.edu)','en')
        self.random_regions = []
    
    def store_wiki_info(self):
        wiki_data = []
        for video in self.chartedVideos:
            channel_name = video.snippet.channelTitle
            page = self.wiki.page(channel_name)
            if page.exists():
                wiki_data.append({
                    'title': page.title,
                    'summary': page.summary
                })
            else:
                continue
        if wiki_data == []:
            return
        else:
            df = pd.DataFrame(wiki_data)
            df.to_sql('wiki_information', con=self.engine, if_exists='replace', index=False)

    def display_wiki_info(self, channel_name):
        with self.engine.connect() as connection:
            query_result = connection.execute(db.text(f"SELECT * FROM wiki_information WHERE title = '{channel_name}'")).fetchall()
            if query_result:
                df = pd.DataFrame(query_result, columns=['title', 'summary'])
                print()
                print(f"Wikipedia Information for {channel_name}:\n")
                for index, row in df.iterrows():
                    print(f"Title: {row['title']}")
                    print(f"Summary: {row['summary']}\n")
            else:
                print("No Wikipedia information available for the channel.")

    def get_channel_statistics(self, channel_id):
        info = self.api.get_channel_info(channel_id=f"{channel_id}")
        return info.items[0].to_dict()
    
    def get_video_information(self, video_object):
        info = {}
        info["title"] = video_object.snippet.localized.title
        info["channel"] = video_object.snippet.channelTitle	
        info["description"] = video_object.snippet.localized.description
        info["viewCount"] = video_object.statistics.viewCount
        info["region"] = self.random_regions[self.chartedVideos.index(video_object)][0]
        info["link"] = f'https://www.youtube.com/watch?v={video_object.id}'
        return info
    
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
    
    def get_most_popular(self, num_videos):
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


api_key = ''
trending = TrendingVideos(api_key)

num_videos = int(input("How many random videos from around the world would you like? (Enter a number, 0 to exit): "))
if num_videos == 0:
    print("Exiting the program...")
    quit()
videos = trending.get_most_popular(num_videos)
trending.display_chart(videos)
print()    
while True:
    show_wiki_info = input("Would you like to see the Wikipedia page for any of the channels? Enter the corresponding video number or 'N' to exit: ")
    if show_wiki_info.lower() == 'n':
        break        
    if show_wiki_info.isdigit():
        video_number = int(show_wiki_info) - 1
        if video_number < 0 or video_number >= len(videos):
            print("Invalid video number")
            continue
    else:
        print("Please type a number")
        continue
    channel_title = videos[video_number].snippet.channelTitle
    trending.store_wiki_info()
    trending.display_wiki_info(channel_title)


    # def display_chart(self, videos):
    #     print("Trending Videos:")
    #     print("----------------")
    #     for i, video in enumerate(videos):
    #         info = self.get_video_information(video)
    #         translated_info = self.translate_video_info(info)
    #         print(f"Video {i+1}:")
    #         print(f"Title: {translated_info['title']}")
    #         print(f"Channel: {translated_info['channel']}")
    #         print(f"Description: {translated_info['description']}")
    #         print(f"View Count: {translated_info['viewCount']}")
    #         print(f"Link: {translated_info['link']}")
    #         print("-" * 50)

    # def translate_video_info(self, info):
    #     translated_info = {}
    #     for key, value in info.items():
    #         translated_value = ts.google(value, to_language='en')
    #         translated_info[key] = translated_value
    #     return translated_info
