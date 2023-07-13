import requests
import pandas as pd
import sqlalchemy as db

df = pd.DataFrame(columns=[
    'Name',
    'Alt Spellings',
    'Region',
    'Subregion',
    'Capital',
    'Currency',
    'Languages',
    'Provinces',
    'Timezones'
])

def added_to_database(data_frame):
    engine = db.create_engine('sqlite:///seocountryinfo.db')
    data_frame.to_sql("country_info", con=engine, if_exists="append", index=False)
    
    with engine.connect() as connection:
        query_result = connection.execute(db.text("SELECT Region, COUNT(*) as reg FROM country_info GROUP BY Region ORDER BY COUNT(*) DESC LIMIT 1;")).fetchall()
        print(pd.DataFrame(query_result)['Region'][0])

data = {
    'Name': ['Country 1', 'Country 2'],
    'Alt Spellings': ['Alt 1', 'Alt 2'],
    'Region': ['Region 1', 'Region 2'],
    'Subregion': ['Subregion 1', 'Subregion 2'],
    'Capital': ['Capital 1', 'Capital 2'],
    'Currency': ['Currency 1', 'Currency 2'],
    'Languages': ['Language 1', 'Language 2'],
    'Provinces': ['Province 1', 'Province 2'],
    'Timezones': ['Timezone 1', 'Timezone 2']
}

