import unittest
from unittest import mock
from unittest.mock import MagicMock
import pandas as pd
from sqlalchemy import create_engine
from youtube_api import TrendingVideos

class TestTrendingVideos(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #create a mock API object
        cls.api_mock = MagicMock()
        #set up the mock response for get_channel_info
        channel_info_mock = MagicMock()
        channel_info_mock.items[0].to_dict.return_value = {
            'title': 'Channel Title',
            'subscribers': 1000
        }
        cls.api_mock.get_channel_info.return_value = channel_info_mock

    def setUp(self):
        #create an instance of TrendingVideos with the mock API
        self.trending_videos = TrendingVideos(api_key='your_api_key')
        self.trending_videos.api = self.api_mock

    def test_get_channel_statistics(self):
        #mock the API response
        channel_id = 'your_channel_id'
        expected_info = {
            'title': 'Channel Title',
            'subscribers': 1000
        }
        info = self.trending_videos.get_channel_statistics(channel_id)
        self.assertEqual(info, expected_info)
        self.api_mock.get_channel_info.assert_called_once_with(channel_id=channel_id)

    def test_get_video_information(self):
        #create mock video objects
        video_mock_1 = MagicMock()
        video_mock_1.snippet.localized.title = 'Video 1'
        video_mock_1.snippet.channelTitle = 'Channel 1'
        video_mock_1.snippet.localized.description = 'Description 1'
        video_mock_1.statistics.viewCount = 100
        video_mock_1.id = 'video_id_1'
        video_mock_2 = MagicMock()
        video_mock_2.snippet.localized.title = 'Video 2'
        video_mock_2.snippet.channelTitle = 'Channel 2'
        video_mock_2.snippet.localized.description = 'Description 2'
        video_mock_2.statistics.viewCount = 200
        video_mock_2.id = 'video_id_2'
        #set the chartedVideos list with mock videos
        self.trending_videos.chartedVideos = [video_mock_1, video_mock_2]
        #call the method under test
        video_list = self.trending_videos.get_video_information()
        #verify the results
        expected_video_list = [
            {
                'title': 'Video 1',
                'channel': 'Channel 1',
                'description': 'Description 1',
                'viewCount': 100,
                'link': 'video_id_1'
            },
            {
                'title': 'Video 2',
                'channel': 'Channel 2',
                'description': 'Description 2',
                'viewCount': 200,
                'link': 'video_id_2'
            }
        ]
        self.assertEqual(video_list, expected_video_list)

    @mock.patch('your_module.print')
    def test_display_chart(self, print_mock):
        # Create mock video objects
        video_mock_1 = MagicMock()
        video_mock_1.snippet.localized.title = 'Video 1'
        video_mock_1.snippet.channelTitle = 'Channel 1'
        video_mock_1.snippet.localized.description = 'Description 1'
        video_mock_1.statistics.viewCount = 100
        video_mock_1.id = 'video_id_1'

        video_mock_2 = MagicMock()
        video_mock_2.snippet.localized.title = 'Video 2'
        video_mock_2.snippet.channelTitle = 'Channel 2'
        video_mock_2.snippet.localized.description = 'Description 2'
        video_mock_2.statistics.viewCount = 200
        video_mock_2.id = 'video_id_2'

        # Set the chartedVideos list with mock videos
        self.trending_videos.chartedVideos = [video_mock_1, video_mock_2]

        # Call the method under test
        self.trending_videos.display_chart(self.trending_videos.chartedVideos)

        # Verify the print calls
        expected_calls = [
            mock.call('Trending Videos:'),
            mock.call('----------------'),
            mock.call("Video 1:"),
            mock.call("Title: Video 1"),
            mock.call("Channel: Channel 1"),
            mock.call("Description: Description 1"),
            mock.call("View Count: 100"),
            mock.call("Region: None"),
            mock.call("Link: video_id_1"),
            mock.call('--------------------------------------------------'),
            mock.call("Video 2:"),
            mock.call("Title: Video 2"),
            mock.call("Channel: Channel 2"),
            mock.call("Description: Description 2"),
            mock.call("View Count: 200"),
            mock.call("Region: None"),
            mock.call("Link: video_id_2"),
            mock.call('--------------------------------------------------')
        ]
        print_mock.assert_has_calls(expected_calls)

    @mock.patch('pandas.DataFrame')
    @mock.patch('sqlalchemy.create_engine')
    def test_store_video_information(self, engine_mock, dataframe_mock):
        dataframe_instance_mock = MagicMock()
        dataframe_mock.return_value = dataframe_instance_mock
        connection_mock = MagicMock()
        engine_instance_mock = MagicMock()
        engine_instance_mock.connect.return_value = connection_mock
        engine_mock.return_value = engine_instance_mock
        video_mock_1 = MagicMock()
        video_mock_1.snippet.localized.title = 'Video 1'
        video_mock_1.snippet.channelTitle = 'Channel 1'
        video_mock_1.snippet.localized.description = 'Description 1'
        video_mock_1.statistics.viewCount = 100
        video_mock_1.id = 'video_id_1'
        self.trending_videos.chartedVideos = [video_mock_1]
        self.trending_videos.store_video_information()
        dataframe_mock.assert_called_once_with([
            {
                'title': 'Video 1',
                'channel': 'Channel 1',
                'description': 'Description 1',
                'viewCount': 100,
                'link': 'video_id_1'
            }
        ])
        engine_mock.assert_called_once_with('sqlite:///youtube_most_popular.db')
        dataframe_instance_mock.to_sql.assert_called_once_with('video_information', con=engine_instance_mock, if_exists='replace', index=False)
        connection_mock.execute.assert_called_once_with(db.text("SELECT * FROM video_information;"))
        pd.DataFrame.assert_called_once_with(connection_mock.execute.return_value.fetchall())

    @mock.patch('random.choices')
    def test_get_most_popular_random(self, choices_mock):
        regions_mock = MagicMock()
        regions_mock.snippet.gl = 'US'
        self.api_mock.get_i18n_regions.return_value = regions_mock
        video_mock = MagicMock()
        video_mock.items[0] = MagicMock()
        self.api_mock.get_videos_by_chart.return_value = video_mock
        choices_mock.return_value = ['US']
        self.trending_videos.get_most_popular_random(num_videos=1)
        self.api_mock.get_i18n_regions.assert_called_once_with(parts=['snippet'])
        choices_mock.assert_called_once_with(['US'], k=1)
        self.api_mock.get_videos_by_chart.assert_called_once_with(chart='mostPopular', region_code='US', count=1)
        self.assertEqual(self.trending_videos.chartedVideos, [video_mock.items[0]])

if __name__ == '__main__':
    unittest.main()
